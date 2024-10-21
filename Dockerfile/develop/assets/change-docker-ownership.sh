#!/bin/bash

chmod -R g+rwx /var/run/docker.sock
chgrp -R ${DOCKER_GROUP_ID} /var/run/docker.sock