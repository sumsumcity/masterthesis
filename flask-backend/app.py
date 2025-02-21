from flask import Flask, request, jsonify, Response  # type: ignore
from flask_cors import CORS  # type: ignore
from werkzeug.utils import secure_filename # type: ignore
import promptHandler
import chunker
import chromaLoader
import json
import dfdParser
import os
from langchain_ollama import OllamaLLM  # type: ignore
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = './uploads'  # temp store uploaded files
ALLOWED_EXTENSIONS = {'md'}
CHROMADB_HOST=os.getenv('CHROMADB_HOST', 'localhost')
CHROMADB_PORT=os.getenv('CHROMADB_PORT', '8000')
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.2')
VECTOR_STORE = chromaLoader.clientInit("aiThreatCollection", OLLAMA_URL, OLLAMA_MODEL, CHROMADB_HOST, CHROMADB_PORT)

@app.route('/evaluation_similaritySearch', methods=['POST'])
def similaritySearchOverDescription():
    try:
        print("Similarity Search Evaluation request received")
        
        # Decode the raw bytes into a string
        request_body = request.data.decode('utf-8')

        # Use the reusable function to get components
        dfd = process_xml(request_body)
        systemDescription = dfdParser.componentToText(dfd["components"])

        # Similarity search
        query = f"Identify threats for the following system: {systemDescription}"
        res = chromaLoader.similarity_search(VECTOR_STORE, query, 8)
        resultList = []
        for r in res:
            threat = list(r.metadata.values())[-1]
            cleaned_threat = re.sub(r'[\d.]', '', threat) # Remove all digits and '.'
            cleaned_threat = cleaned_threat.lstrip() # Remove the first space
            if "Sensitive data disclosure through use" in cleaned_threat:
                cleaned_threat = "Sensitive data output from model"
                if cleaned_threat not in resultList:
                    resultList.append(cleaned_threat)
                cleaned_threat = "Model inversion and membership inference"
                if cleaned_threat not in resultList:
                    resultList.append(cleaned_threat)
            if cleaned_threat not in resultList:
                resultList.append(cleaned_threat)
        print("similarity search conducted")


        print("The Output is: ")
        print(resultList)

        return jsonify({"message": "Threat detection processed successfully", "threats": resultList})
    except Exception as e:
        return Response(f"<error>{str(e)}</error>", status=400, content_type='application/xml')

@app.route('/evaluation_reranking', methods=['POST'])
def reranker():
    try:
        print("Reranking request received")
        
        # 1) Copy the similarity search which worked best
        # 2) Load the chunks which worked best (chunking strategy)
        # 3) Add https://python.langchain.com/docs/integrations/retrievers/flashrank-reranker/#doing-reranking-with-flashrank
        return jsonify({"message": "Threat detection processed successfully", "threats": "resultList"})
    except Exception as e:
        return Response(f"<error>{str(e)}</error>", status=400, content_type='application/xml')

@app.route('/queryLLM', methods=['POST'])
def test():
    print("QueryLLM request:")
    request_body = request.data.decode('utf-8')
    request_body = json.loads(request_body)
    print(request_body)
    prompt = request_body.get('prompt', '')

    # Pass the base_url parameter to OllamaLLM
    print("Ollama URL is: " + OLLAMA_URL)
    print("Prompt is: " + prompt)
    llm = OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_URL)
    
    # Call the model and get the output
    output = llm.invoke(prompt)
    print("Output of LLM is: " + output)

    return {"output": output}, 200


@app.route('/upload', methods=['POST'])
def upload_file():

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Check if the request has files
    if 'file' not in request.files:
        return jsonify({"error": "No files part in the request."}), 400

    # Get all files under the 'file' key (since it's being sent multiple times)
    files = request.files.getlist('file')

    # Check if at least one file is selected
    if not files:
        return jsonify({"error": "No files selected."}), 400

    uploaded_files = []
    failed_files = []

    for file in files:
        if file.filename == '':
            failed_files.append(file.filename)
            continue

        # Validate file type
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            try:
                # Process the file using mdDocumentChunker
                with open(filepath, 'r', encoding='utf-8') as f:
                    file_content = f.read()

                chunks = chunker.mdDocumentChunker(file_content)
                print(f"Number of chunks loaded from {filename}: {len(chunks)}")

                ### Evaluation - Summarization in document chunking
                # for i, chunk in enumerate(chunks):
                #     print("Summarize chunk " + str(i+1))

                #     prompt = f"Summarize the provided text in 1000 tokens, focusing primarily on describing the threat itself. Your summary should clearly explain the nature of the threat, how it operates, and how an attacker could potentially exploit it. Avoid focusing on mitigation strategies, controls, or defensive measures. Instead, emphasize the mechanisms of the threat, its potential impact, and the ways in which an attacker might leverage it to achieve their objectives. The text is: {chunk.page_content}" 
                #     llm = OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_URL)
                #     output = llm.invoke(prompt)
                #     print(output)
                #     chunk.page_content = output

                ### Evaluation - Recursive chunking
                # finalChunks = []
                # for i, chunk in enumerate(chunks):
                #     print("Recursive Chunking for Chunk: " + str(i+1))
                #     result = chunker.recursiveChunker(chunk, 512, 100)
                #     for doc in result:
                #         finalChunks.append(doc)
                # chunks = finalChunks

                # Store chunks in chromadb
                chromaLoader.addDocumentsToVectorstore(VECTOR_STORE, chunks, OLLAMA_URL, OLLAMA_MODEL)

                # Clean up the uploaded file
                os.remove(filepath)

                uploaded_files.append(filename)

            except Exception as e:
                failed_files.append(f"{filename}: {str(e)}")
        else:
            failed_files.append(f"{file.filename}: Invalid file type")

    if uploaded_files:
        return jsonify({"message": "Files uploaded and processed successfully.", "files": uploaded_files}), 200
    else:
        return jsonify({"error": "No valid files uploaded.", "failed": failed_files}), 400

    

@app.route('/threat_detection', methods=['POST'])
def threat_detection():
    try:
        print("Threat detection request received")
        
        # Decode the raw bytes into a string
        request_body = request.data.decode('utf-8')

        # Use the reusable function to get components
        dfd = process_xml(request_body)

        # For now, just print the components (or handle further logic)
        threats = promptHandler.detectThreats(dfd, VECTOR_STORE, 2, OLLAMA_MODEL, OLLAMA_URL)

        print("The Output is: ")
        print(threats)

        return jsonify({"message": "Threat detection processed successfully", "threats": threats})
    except Exception as e:
        return Response(f"<error>{str(e)}</error>", status=400, content_type='application/xml')

@app.route('/threat_validation', methods=['POST'])
def threat_validation():
    try:
        print("Threat validation request received")
        
        # Decode the raw bytes into a string
        request_body = request.data.decode('utf-8')

        # Use the reusable function to get components
        dfdXml = json.loads(request_body).get("dfd")
        dfd = process_xml(dfdXml)
        threats =  json.loads(request_body).get("threats")

        systemDescription = dfdParser.componentToText(dfd["components"])
        threats = promptHandler.validateThreats(systemDescription, threats, OLLAMA_MODEL, OLLAMA_URL)
        
        return jsonify({"message": "Threat validation processed successfully", "threats": threats})
    except Exception as e:
        return Response(f"<error>{str(e)}</error>", status=400, content_type='application/xml')

@app.route('/parse_dfd_to_components', methods=['POST'])
def parse_dfd_to_components():
    try:
        # Decode the raw bytes into a string
        request_body = request.data.decode('utf-8')

        # Get components using the reusable function
        result = process_xml(request_body)

        return jsonify(result)
    except Exception as e:
        return Response(f"<error>{str(e)}</error>", status=400, content_type='application/xml')

    
def process_xml(request_body):
    try:
        # If `dfdXml` is already a dictionary, skip json.loads
        if isinstance(request_body, dict):
            json_data = request_body
        else:
            # Otherwise, parse the JSON string into a Python dictionary
            json_data = json.loads(request_body)

        # Extract the XML string from the JSON structure
        dfd_xml = json_data.get('xml')

        # Pass the XML string to the parser function
        components = dfdParser.threatFinderAiDfdToComponentList(dfd_xml)

        return {"components": components}
    except Exception as e:
        raise ValueError(str(e))

# Check if the file has an allowed extension.
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
