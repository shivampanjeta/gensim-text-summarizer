# FROM ubuntu:18.04
FROM pytorch/pytorch:latest

RUN apt-get update && \
    apt-get install -y --no-install-recommends nginx git \
    apt-get install -y sudo \
    build-essential \
    curl \
    libcurl4-openssl-dev \
    libssl-dev \
    python3-dev \
    python3-pip \
    libxrender-dev \
    libxext6 \
    libsm6 \
    openssl \
    nginx \
    libgcc-5-dev \
#     ca-certificates \
    && apt-get clean all \
    && rm -r /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

# Set some environment variables. PYTHONUNBUFFERED keeps Python from buffering our standard
# output stream, which means that logs can be delivered to the user quickly. PYTHONDONTWRITEBYTECODE
# keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the train and serve programs are found when the container is invoked.

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

# Set up the program in the image
COPY plugreclassification /opt/program
COPY requirements.txt /opt/program
WORKDIR /opt/program

RUN pip3 install -r requirements.txt
