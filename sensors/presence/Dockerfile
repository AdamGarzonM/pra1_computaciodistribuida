FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3-pip

COPY . .

RUN pip install paho-mqtt
#RUN chmod a+x run.sh
#CMD ./run.sh