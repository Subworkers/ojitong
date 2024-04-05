FROM jupyter/base-notebook:python-3.11

ARG CURRENT_PATH

USER root

RUN apt-get -y update --fix-missing
RUN apt-get install -y git
RUN apt-get install -y curl
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