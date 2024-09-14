FROM debian

WORKDIR /usr/src

RUN apt-get update && \
    apt-get install -y python3 python3-pip
#installing python

RUN useradd --create-home appuser 
# runs as root user

COPY server.py .
#copies the code to the docker image

# ENV API_KEY=testuser
# pass as environment variable used for user authentication

EXPOSE 1234

CMD ["python3", "./server.py"]