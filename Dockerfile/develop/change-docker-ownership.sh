#!/bin/bash

chmod -R g+rwx /var/run/docker.sock
chgrp -R ${DOCKER_GROUP_ID***REMOVED*** /var/run/docker.sock