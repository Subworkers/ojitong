#!/bin/sh
pem_file_path=${PEM_FILE_PATH***REMOVED***

pip3 install jwt
jwt_token=$(python3 assets/generate_jwt_token.py ${PEM_FILE_PATH***REMOVED*** ${APP_ID***REMOVED******REMOVED***

registration_url="https://api.github.com/app/installations/${APP_ID***REMOVED***/access_tokens"
echo "Requesting registration URL at '${registration_url***REMOVED***'"

payload=$(curl --request POST \
--url ${registration_url***REMOVED*** \
--header "Accept: application/vnd.github+json" \
--header "Authorization: Bearer ${jwt_token***REMOVED***" \
--header "X-GitHub-Api-Version: 2022-11-28"***REMOVED***
export RUNNER_TOKEN=$(echo $payload | jq .token --raw-output***REMOVED***

./config.sh \
    --name ${RUNNER_NAME***REMOVED*** \
    --token ${RUNNER_TOKEN***REMOVED*** \
    --url https://github.com/${GITHUB_OWNER***REMOVED***/${GITHUB_REPOSITORY***REMOVED*** \
    --work ${RUNNER_WORKDIR***REMOVED*** \
    --unattended \
    --replace \
    --labels ${RUNNER_LABELS***REMOVED***

remove(***REMOVED*** {
    ./config.sh remove --unattended --token "${RUNNER_TOKEN***REMOVED***"
***REMOVED***

trap 'remove; exit 130' INT
trap 'remove; exit 143' TERM

./run.sh "$*" &

wait $!