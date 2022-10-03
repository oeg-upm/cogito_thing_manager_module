docker buildx build --platform=linux/amd64 -t thing_manager:latest-amd .
docker tag thing_manager:latest-amd salva5297/thing_manager:latest
docker push salva5297/thing_manager:latest