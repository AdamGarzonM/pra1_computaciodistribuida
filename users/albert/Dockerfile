FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3

COPY . .

RUN chmod a+x run.sh
CMD ["run.sh"]