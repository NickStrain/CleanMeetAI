### Building and running your application
docker build -t dockerimage .
docker run --name docker -d -i -t  -p 80:80 -v "E:\CleanMeetAI":/code dockerimage
docker exec -d docker touch /tmp/execWorks
docker exec -it mycontainer sh
winpty docker exec -it docker sh
