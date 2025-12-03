FROM python:3.13
WORKDIR /usr/local/app


RUN pip install --no-cache-dir requests

RUN apt-get install openssh-client -y


CMD ["tail", "-f", "/dev/null"]