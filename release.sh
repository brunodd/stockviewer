#!/bin/zsh

docker buildx build --platform=linux/amd64,linux/arm64 --tag europe-west1-docker.pkg.dev/stockviewer-dev-dc0e/stockviewer-repo/stockviewer:latest --push .

gcloud run deploy stockviewer \
--image=europe-west1-docker.pkg.dev/stockviewer-dev-dc0e/stockviewer-repo/stockviewer:latest \
--platform=managed \
--project=stockviewer-dev-dc0e --region=europe-west1 \
--timeout=60 \
--concurrency=10 \
--cpu=1 \
--max-instances=4 \
--allow-unauthenticated
