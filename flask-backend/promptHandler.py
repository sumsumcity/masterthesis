import chromaLoader
from langchain_ollama import OllamaLLM  # type: ignore
import ast


def detectThreats(dfdJson, collection="aiThreatCollection", k=2):
    inputContext = ""
    assetname=[]
    assetlabel=[]
    vectorStore = chromaLoader.clientInit(collection)

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
    llm = OllamaLLM(model="llama3.2")
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
    

# Main logic - when the script is called directly
if __name__ == "__main__":

    vectorStore = chromaLoader.clientInit("aiThreatCollection")

    llm = OllamaLLM(model="llama3.2")
    input_text = f"Hello"
    print(llm.invoke(input_text))