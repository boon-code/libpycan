FROM ubuntu:22.04

RUN DEBIAN_FRONTEND=noninteractive apt-get update \
 && DEBIAN_FRONTEND=noninteractive \
    apt-get install -y \
        vim \
        build-essential \
        python3 \
        python3-venv \
        python3-pip \
        can-utils \
 && rm -rf /var/lib/apt/lists/*
