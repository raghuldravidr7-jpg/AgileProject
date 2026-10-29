# Patient Records

Simple Flask + SQLite app to register, search and delete patient records.

## Run locally
    pip install -r requirements.txt
    python app.py
Open http://localhost:5000

## Docker
    docker build -t YOUR_DOCKERHUB_USERNAME/patient-records:v1 .
    docker run -p 5000:5000 YOUR_DOCKERHUB_USERNAME/patient-records:v1

## Kubernetes
    kubectl apply -f k8s/
