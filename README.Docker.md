### Building and running your application
docker build -t dockerimage .
docker run --name docker -d -i -t  -p 80:80 -v "E:\CleanMeetAI":/code dockerimage
docker exec -d docker touch /tmp/execWorks
docker exec -it docker sh
winpty docker exec -it docker sh


### inside the docker 
apt-get update
apt-get install -y libgtk-3-dev pkg-config

or 

sudo apt-get update
sudo apt-get install -y libqt5widgets5 libqt5gui5 libqt5core5a
pip install opencv-python opencv-python-headless opencv-contrib-python
