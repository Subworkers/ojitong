FROM ubuntu:22.04
FROM python:3.11-slim

# NOTE:
# - https://docs.github.com/en/actions/creating-actions/dockerfile-support-for-github-actions#user
# - Must be set only root user in github action
# USER root

ENV RUNNER_NAME "runner"
ENV RUNNER_WORKDIR "/actions-runner"
ENV DOTNET_SYSTEM_GLOBALIZATION_INVARIANT "1"

ENV USER_NAME "runner"
ARG DOCKER_GROUP_NAME
ARG DOCKER_GROUP_ID

RUN apt-get -y update
RUN apt-get install -y git
RUN apt-get install -y curl
RUN apt-get install -y jq
RUN apt-get install -y make
RUN apt-get install -y docker-compose
RUN apt-get install -y gh

# adduser "runner"
RUN adduser ${USER_NAME***REMOVED***

# Docker
RUN curl -fsSL https://get.docker.com -o get-docker.sh
RUN sh get-docker.sh
# dind docker group gid 수정
# RUN groupadd -f ${DOCKER_GROUP_NAME***REMOVED***
RUN groupmod -g ${DOCKER_GROUP_ID***REMOVED*** ${DOCKER_GROUP_NAME***REMOVED***
RUN usermod -aG ${DOCKER_GROUP_NAME***REMOVED*** root
RUN usermod -aG ${DOCKER_GROUP_NAME***REMOVED*** ${USER_NAME***REMOVED***
RUN newgrp ${DOCKER_GROUP_NAME***REMOVED***

WORKDIR ${RUNNER_WORKDIR***REMOVED***

COPY Dockerfile/develop/entrypoint.sh ${RUNNER_WORKDIR***REMOVED***/entrypoint.sh
RUN chmod -R a+w ${RUNNER_WORKDIR***REMOVED***

USER root
RUN curl -o actions-runner-linux-x64-2.302.1.tar.gz -L https://github.com/actions/runner/releases/download/v2.302.1/actions-runner-linux-x64-2.302.1.tar.gz
RUN tar xzf ./actions-runner-linux-x64-2.302.1.tar.gz
RUN ./bin/installdependencies.sh

USER ${USER_NAME***REMOVED***

ENTRYPOINT ["./entrypoint.sh"***REMOVED***