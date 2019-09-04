FROM python:3.7.4-slim

# Install required packages
RUN apt-get update && \
    apt-get install -y make

# Set workdir and install python requirements
WORKDIR /usr/src/love
COPY requirements.txt .
RUN pip install -r requirements.txt
