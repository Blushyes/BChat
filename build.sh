touch markedfile
touch api.ini
docker rm -f bill-chat
docker build . -t bill-chat
docker run -d --name bill-chat -v ./markedfile:/app/markedfile -v ./config.json:/app/config.json bill-chat