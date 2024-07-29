FROM jupyter/base-notebook:python-3.11

ARG CURRENT_PATH
ARG CHROME_VERSION=125.0.6422.141

USER root

RUN apt-get -y update

# google chrome
RUN apt-get install -y wget gnupg --no-install-recommends && \
rm -rf /var/lib/apt/lists/*
RUN wget -qO- https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
echo "deb [arch=amd64***REMOVED*** http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
apt-get update && \
apt-get install -y google-chrome-stable --no-install-recommends && \
rm -rf /var/lib/apt/lists/*

# google chrome driver
RUN apt-get -y update && apt-get upgrade -y && apt-get install -y unzip
RUN apt-get install -y libnss3
RUN wget https://storage.googleapis.com/chrome-for-testing-public/$CHROME_VERSION/linux64/chromedriver-linux64.zip && \
unzip chromedriver-linux64.zip && \ 
cp chromedriver-linux64/chromedriver /usr/local/bin/ && \ 
chmod +x /usr/local/bin/chromedriver

RUN apt-get install -y git
RUN apt-get install -y curl
RUN apt-get install -y jq
#only in windows & wsl env
#RUN apt-get install -y python3-pip

WORKDIR /workspace
RUN chmod -R a+w /workspace

# Application
RUN conda install -n base -c conda-forge ipywidgets -y
RUN conda install -n base -c conda-forge widgetsnbextension -y

# Deployment
RUN curl -fsSL https://get.docker.com -o get-docker.sh
RUN sh get-docker.sh

# Data
COPY data/requirements/base.txt /workspace/data-requirements.txt
RUN pip install -r data-requirements.txt

EXPOSE 8888

ENTRYPOINT jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --notebook-dir /