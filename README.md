# Masterthesis

docker running:
1) docker-compose up

Local running:
1) docker-compose up --build chromadb
2) python -m venv venv
3) source venv/Scripts/activate
4) cd flask-backend
5) pip install -r requirements.txt
6) flask run
7) cd ../react-frontend
8) npm install
9) npm start

Change Model:
1) Change Model in docker-compose.yaml file
2) Add "ollama pull [modelname]" in the entrypoint.sh to download the desired model in ollama