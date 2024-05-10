FROM python:slim

ARG PEPPER
ARG KEYCHAIN_NUMBER
ARG JWT_KEY

ENV PEPPER=$PEPPER
ENV KEYCHAIN_NUMBER=$KEYCHAIN_NUMBER
ENV JWT_KEY=$JWT_KEY

RUN apt-get update && \
    apt-get install -y \
    gcc && \
    python -m ensurepip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# copying the application to the image
COPY /src/ /backend/src

COPY requirements.txt /backend

COPY values.json /backend

COPY log_conf.yaml /backend

WORKDIR /backend

# updating python package manager
RUN pip3 install --upgrade pip

# installing python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

CMD [ "uvicorn","src.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config=log_conf.yaml"]
