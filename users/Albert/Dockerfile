FROM ubunt:slim

RUN apt-get update
RUN apt-get install -y python3

COPY . /devices

RUN chmod a+x run.sh
CMD ["./run.sh"]