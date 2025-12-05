FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    ssh-client \
    lsb-release

WORKDIR /app

COPY requet.py .
COPY requirements.txt .
COPY agent.py .
COPY sshconnect.py .

RUN pip install -r requirements.txt

CMD ["python","requet.py"]