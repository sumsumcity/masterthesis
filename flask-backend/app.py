from flask import Flask, request, jsonify, Response  # type: ignore
from flask_cors import CORS  # type: ignore
from werkzeug.utils import secure_filename # type: ignore
import promptHandler
import chunker
import chromaLoader
import json
import dfdParser
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = './uploads'  # temp store uploaded files
ALLOWED_EXTENSIONS = {'md'}
VECTOR_STORE = chromaLoader.clientInit("aiThreatCollection")

@app.route('/upload', methods=['POST'])
def upload_file():

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Check if the request has a file part
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files['file']

    # Check if a file is selected
    if file.filename == '':
        return jsonify({"error": "No file selected."}), 400

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
            print("Number of chunks loaded: " + str(len(chunks)))

            # Store chunks in chromadb
            chromaLoader.addDocumentsToVectorstore(VECTOR_STORE, chunks)

            # Clean up the uploaded file
            os.remove(filepath)

            return jsonify({"message": "File uploaded and processed successfully."}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    else:
        return jsonify({"error": "Invalid file type. Only .md files are allowed."}), 400
    

@app.route('/threat_detection', methods=['POST'])
def threat_detection():
    try:
        print("Threat detection request received")
        
        # Decode the raw bytes into a string
        request_body = request.data.decode('utf-8')

        # Use the reusable function to get components
        dfd = process_xml(request_body)

        # For now, just print the components (or handle further logic)
        threats = promptHandler.detectThreats(dfd)

        return jsonify({"message": "Threat detection processed successfully", "threats": threats})
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
        # Parse the JSON string into a Python dictionary
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
