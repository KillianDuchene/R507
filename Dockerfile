FROM python:3.13
WORKDIR /usr/local/app

# Install the application dependencies
RUN pip install --no-cache-dir requests

# Setup an app user so the container doesn't run as the root user
RUN apt-get install openssh-client -y


CMD ["tail", "-f", "/dev/null"]