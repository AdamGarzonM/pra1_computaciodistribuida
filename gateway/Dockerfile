FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3-pip

COPY . .

RUN pip install -r requirements.txt
#RUN chmod a+x run.sh
#CMD ./run.sh