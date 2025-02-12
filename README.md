# Masterthesis

docker running:
1) Check if your GPU is ready to use by running:
`docker run --rm -it --gpus=all nvcr.io/nvidia/k8s/cuda-sample:nbody nbody -gpu -benchmark`
If the GPU is not available, update the Docker Compose YAML file accordingly. Otherwise, continue.
2) docker-compose up

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