import chromaLoader
from langchain_ollama import OllamaLLM  # type: ignore
import ast
import json
import re


def detectThreats(dfdJson, VECTOR_STORE, k=2, OLLAMA_MODEL="llama3.2", OLLAMA_URL="localhost"):
    inputContext = ""
    assetname=[]
    assetlabel=[]
    vectorStore = VECTOR_STORE

    for component in dfdJson["components"]:
        if component["type"] == "asset":
            assetlabel.append(component["label"])
            assetname.append(component["assetname"])

    for i, an in enumerate(assetname):
        query = f"Identify threats for the following assets: {an} called {assetlabel[i]}"
        res = chromaLoader.similarity_search(vectorStore, query, k)
        for r in res:
            inputContext = inputContext + str(r.metadata)
        print(f"{i+1}/{len(assetname)} similarity search conducted")

    print("Input context is generated")
    print("Input context: " + inputContext)

    # Ask LLM
    llm = OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_URL)
    input_text = (
        f"Here is some context: {inputContext}. "
        "Please extract a list of all threats mentioned in the context. "
        "Do NOT add any additional information and do not invent any further threats that are not found in the context. "
        "If the threat identified is 'Sensitive data disclosure through use,' replace it with the following two threats: 'Sensitive data output from model' and 'Model inversion and membership inference.' Do not mention 'Sensitive data disclosure through use' in any context, and only refer to the other two threats."        "Follow these rules: "
        "1. Ignore all numbers and keys in the dictionaries. "
        "2. Exclude any uppercase values starting with a hashtag (e.g., #OBSCURECONFIDENCE). "
        "3. Do NOT add any threats not explicitly stated in the context. Do NOT infer, interpret, or invent any additional threats, even if they seem relevant. Only include threats that are verbatim or synonymous with those mentioned in the context. "
        "4. Provide the output in the exact format of a Python list. For example: [\"Threat 1\", \"Threat 2\"]."
    )
    output =  llm.invoke(input_text)
    resultList = ast.literal_eval(output)
    return resultList

def validateThreats(systemDescription, threatList, OLLAMA_MODEL="llama3.2", OLLAMA_URL="localhost"):

    # Ask LLM
    #print(f"Analyzes threat "+str(i+1)+"/"+str(len(threatList)))
    llm = OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_URL)
    threats = []
    for t in threatList:
        threats.append({"Threat": t["Threat"], "Description": t["Description"]})

    input_text_alternative = (
        "**Priming**: "
        "You are tasked with analyzing the provided system description and updating the descriptions of potential threats to explain why each threat is critical to this system. Each updated description should: "
        "1. Explain the threat's importance and relevance to the system based on the provided details (2-4 sentences). "
        "2. Include an example (1-2 sentences) showing how the threat could be exploited, using asset names and trust boundaries. "
        "3. Assign a **unique ranking** to each threat based on its importance (1 = most critical, larger numbers = less critical). Ensure no duplicate rankings by explicitly comparing and adjusting as needed. "        "**Style and Tone instructions:** "
        "Use concise, simple, and professional language. Focus only on the provided system description and threats. "
        "Do not add new threats, modify the provided threats, or introduce unrelated information. "
        "**Handling edge cases**: "
        "If a threat lacks sufficient context to its description, leave the original description unchanged and assign it the lowest ranking "
        "**Dynamic content**: "
        f"System Description: {systemDescription}. "
        f"Threats: {str(threats)}. "
        "**Output formatting**: "
        "Respond directly with a JSON-formatted list of threats. Each threat should include: "
        "- 'Threat': The name of the threat. "
        '- "Description": An updated description with the explanation and example. '
        '- "Ranking": The unique ranking of the threat.'
        'Example output: [{"Threat": "Direct Prompt Injection","Description": "This threat allows attackers to bypass safeguards, manipulating the model [assetname of system description] to produce harmful outputs. For example, malicious instructions embedded in inputs in the asset [assetname of system description] could expose sensitive data.","Ranking": 1}, {"Threat": "Open-box Evasion","Description": "This threat enables adversaries to bypass security by understanding the models [assetname of system description] internal workings. For instance, attackers might exploit architecture details in the trustboundary [trustboundary name of system description] to generate outputs that compromise sensitive data.","Ranking": 2}, ...]'
    )

    input_text = (
    "### Task Definition: "
    "Analyze the provided system description and update the descriptions of potential threats to explain why each threat is critical to this system. Each updated description should: "
    "1. Explain the threat's importance and relevance to the system based on the provided details (2-4 sentences). "
    "2. Include an example (1-2 sentences) showing how the threat could be exploited, using asset names and trust boundaries. "
    "3. Assign a unique ranking to each threat based on its importance (1 = most critical, larger numbers = less critical). Ensure no duplicate rankings by explicitly comparing and adjusting as needed. "
    
    "### Style and Tone: "
    "Use concise, simple, and professional language. Focus only on the provided system description and threats. "
    "Do not add new threats, modify the provided threats, or introduce unrelated information. "
    
    "### Handling Edge Cases: "
    "If a threat lacks sufficient context in its description, leave the original description unchanged and assign it the lowest ranking. "
    
    "### Input Details: "
    f"System Description: {systemDescription}. "
    f"Threats: {str(threats)}. "
    
    "### Output Requirements: "
    "Return only the JSON-formatted list of threats. Do not include any additional text, such as comments, explanations, or introductions, before or after the JSON output. The JSON should strictly adhere to this structure:"
    "- 'Threat': The name of the threat. "
    '- "Description": An updated description with the explanation and example. '
    '- "Ranking": The unique ranking of the threat. '
    
    "### Example Output: "
    '[{"Threat": "Threat Name Placeholder",'
    '"Description": "This threat impacts [assetname of system description] by [action placeholder], leading to [consequence placeholder]. For example, [example action placeholder] could exploit [trustboundary name of system description].",'
    '"Ranking": 1}, '
    '{"Threat": "[Another Threat Name Placeholder]",'
    '"Description": "This threat allows adversaries to [action placeholder] in [assetname of system description], causing [consequence placeholder]. For instance, [example action placeholder] might leverage [trustboundary name of system description] to compromise security.",'
    '"Ranking": 2}, ...]'
)

    print("These are all the threats received:")
    print(str(threats))
    print("LLM validates the threats. This can take a moment. Please wait...")
    output =  llm.invoke(input_text)
    print("Raw LLM Output:")
    print(output)
    print("---------------------------------------------------------------------------")
    try:
        output = json.loads(output)
        for o in output:
            for t in threatList:
                if o["Threat"] == t["Threat"]:
                    t["Description"] = o["Description"]
                    if o["Ranking"]==1:
                        t["Description"] = t["Description"] + " This is a Rank 1 threat, which means it is the most important to address. "
                        print(f"Rank 1 was given to Threat: {o['Threat']}.")
                    else:
                        t["Description"] = t["Description"] + f" This is a Rank {o['Ranking']} threat, less critical than Rank 1 but still highly important. "
                        print(f"Rank {o['Ranking']} was given to Threat: {o['Threat']}.")
                    break   
        
        print("Final output:")
        print(threatList)
        print("---------------------------------------------------------------------------")
        return threatList
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON directly: {e}")
        try:
            json_match = re.search(r"\[.*?\]", output, re.DOTALL)
            if json_match:
                json_string = json_match.group(0)
                print("Extracted JSON String:")
                print(json_string)  # Debugging: Zeigt den extrahierten JSON-String

                # Parst den extrahierten JSON-String
                output = json.loads(json_string)
                print("Parsed JSON Output:")
                print(output)

                for o in output:
                    for t in threatList:
                        if o["Threat"] == t["Threat"]:
                            t["Description"] = o["Description"]
                            if o["Ranking"] == 1:
                                t["Description"] += " This is a Rank 1 threat, which means it is the most important to address. "
                            else:
                                t["Description"] += f" This is a Rank {o['Ranking']} threat, less critical than Rank 1 but still highly important. "
                            break
                return threatList
            else:
                print("No valid JSON array found in output.")
        except json.JSONDecoder as e:
            print(f"After trying to find the first [ and the correspong ] there is still an error: {e}")
        return threatList


# Main logic - when the script is called directly
if __name__ == "__main__":

    vectorStore = chromaLoader.clientInit("aiThreatCollection")

    llm = OllamaLLM(model="llama3.2")
    input_text = f"Hello"
    print(llm.invoke(input_text))