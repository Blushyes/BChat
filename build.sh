touch markedfile
touch api.ini
docker rm -f bill-chat-0.1.0
docker build . -t bill-chat:0.1.0
docker run -d --name bill-chat-0.1.0 -v ./tmp:/tmp -v ./markedfile:/app/markedfile -v ./api.ini:/app/api.ini bill-chat:0.1.0