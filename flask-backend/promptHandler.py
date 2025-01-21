import chromaLoader
from langchain_ollama import OllamaLLM  # type: ignore
import ast
import json


def detectThreats(dfdJson, VECTOR_STORE, k=2, OLLAMA_MODEL="llama3", OLLAMA_URL="localhost"):
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
        "3. Provide the output in the exact format of a Python list. For example: [\"Threat 1\", \"Threat 2\"]."
    )
    output =  llm.invoke(input_text)
    resultList = ast.literal_eval(output)
    return resultList

def validateThreats(systemDescription, threatList, OLLAMA_MODEL="llama3", OLLAMA_URL="localhost"):

    # Ask LLM
    #print(f"Analyzes threat "+str(i+1)+"/"+str(len(threatList)))
    llm = OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_URL)
    threats = []
    for t in threatList:
        threats.append({"Threat": t["Threat"], "Description": t["Description"]})

    input_text_alternative = (
    f"System Description: {systemDescription}. "
    f"Threats: {str(threats)}. "
    "**Task:**"
    "1. Update each threat's description to explain its importance and criticality to this system, using asset names and trust boundaries. "
    "2. Add a detailed explanation (2-4 sentences) tailored to the system, including an example (1-2 sentences) showing how the threat could be exploited in this system. "
    "3. Rank each threat uniquely by importance (1 = most critical, larger numbers = less critical). No ties. "
    "**Rules:**"
    "- Add a 'Ranking' key to each threat's dictionary. "
    "- Leave the description unchanged and rank lowest if context is insufficient. "
    "- Do not add new threats or extra information. "
    "- Output JSON with the updated structure, including the updated description and ranking. "
    "**Output Example:**"
    '[{"Threat": "Direct Prompt Injection","Description": "This threat allows attackers to bypass safeguards, manipulating the model to produce harmful outputs. For example, malicious instructions embedded in inputs could expose sensitive data.","Ranking": 1}, ...]'
)

    input_text = (
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

    print("LLM validates the threats. This can take a moment. Please wait...")
    output =  llm.invoke(input_text)
    print(output)
    try:
        output = json.loads(output)
        for o in output:
            for t in threatList:
                if o["Threat"] == t["Threat"]:
                    t["Description"] = o["Description"]
                    if o["Ranking"]==1:
                        t["Description"] = t["Description"] + " This is a Rank 1 threat, which means it is the most important to address. "
                        #t["Ranking"] = o["Ranking"]
                    else:
                        t["Description"] = t["Description"] + f" This is a Rank {o['Ranking']} threat, less critical than Rank 1 but still highly important. "
                        #t["Ranking"] = o["Ranking"]
                    break   

        return threatList
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return threatList


# Main logic - when the script is called directly
if __name__ == "__main__":

    vectorStore = chromaLoader.clientInit("aiThreatCollection")

    llm = OllamaLLM(model="llama3.2")
    input_text = f"Hello"
    print(llm.invoke(input_text))