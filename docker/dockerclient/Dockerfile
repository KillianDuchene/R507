FROM python:3.9-slim


RUN apt-get update && apt-get install -y \
    openssh-server \
    iputils-ping \
    lsb-release


RUN pip install requests


RUN echo 'root:kil' | chpasswd

RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
#https://gist.github.com/etigui/3c9f0158e8d164d761e7ddff8e8e1d47



WORKDIR /app

CMD ["/usr/sbin/sshd", "-D"]