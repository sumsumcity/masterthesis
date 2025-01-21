import chromadb # type: ignore
from langchain_chroma import Chroma # type: ignore
from langchain_ollama import OllamaEmbeddings # type: ignore
from langchain_core.documents import Document # type: ignore
from uuid import uuid4

# https://docs.trychroma.com/docs/overview/getting-started
# https://python.langchain.com/docs/integrations/vectorstores/chroma/#query-directly
# https://python.langchain.com/docs/integrations/text_embedding/


def clientInit(collectionName, ollamaURL, embeddingModel="llama3", host="localhost", port=8000):
    
    embeddings = OllamaEmbeddings(model=embeddingModel, base_url=ollamaURL)
    persistent_client = chromadb.HttpClient(host=host, port=port)

    vector_store_from_client = Chroma(
        client=persistent_client,
        collection_name=collectionName,
        embedding_function=embeddings,
    )
    return vector_store_from_client

def addDocumentsToVectorstore(vectorStore, documents):
    embeddings = OllamaEmbeddings(model="llama3")

    for i, doc in enumerate(documents):
        print(f"Calculating Embedding of chunk {i+1}/{len(documents)}")
        embedding = embeddings.embed_query(doc.page_content)
        print("Embedding is calculated")
        vectorStore.add_texts(
            texts=[doc.page_content],
            metadatas=[doc.metadata],
            ids=[str(uuid4())],
            embeddings=[embedding],
        )
        print(f"{i+1}/{len(documents)} chunks loaded in chromaDB...")

def deleteData(vectorStore, uuid):
    vectorStore.delete(ids=uuid)

def updateData(vectorStore, uuid, newDocument):
    vectorStore.update_document(document_id=uuid, document=newDocument)

def getData(vectorStore, includeEmbeddings=False):
    if includeEmbeddings:
        return vectorStore.get(include=['embeddings', 'documents', 'metadatas'])
    else:
        return vectorStore.get()
    
def similarity_search(vectorStore, prompt, numberOfResults):
    results = vectorStore.similarity_search(
        prompt,
        k=numberOfResults,
    )
    return results



# Main logic - when the script is called directly
if __name__ == "__main__":

    vectorStore = clientInit("aiThreatCollection")

    #deleteData(vectorStore, getData(vectorStore)["ids"])
    #addDocumentsToVectorstore(vectorStore, documents)

    #result = getData(vectorStore)
    #print(len(result["ids"]))

    # client = chromadb.HttpClient(host="localhost", port=8000)
    # collections = client.list_collections()
    # for collection in collections:
    #     print(collection)
    