touch markedfile
touch api.ini
docker rm -f bill-chat
docker build . -t bill-chat
docker run -d --name bill-chat -v ./tmp:/tmp -v ./markedfile:/app/markedfile -v ./api.ini:/app/api.ini bill-chat