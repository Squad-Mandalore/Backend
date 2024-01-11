FROM python:slim

RUN apt-get update && \
    apt-get install -y \
    gcc && \
    python -m ensurepip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# copying the application to the image
COPY /main/ /scoring-service/main

COPY requirements.txt /scoring-service

WORKDIR /scoring-service

# updating python package manager
RUN pip3 install --upgrade pip

# installing python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

CMD [ "uvicorn","src.main:app","--reload"]