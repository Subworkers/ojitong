#!/bin/sh
pem_file_path=${PEM_FILE_PATH***REMOVED***
jwt_token=$(python3 generate_jwt_token.py ${PEM_FILE_PATH***REMOVED*** ${APP_ID***REMOVED******REMOVED***

registration_url="https://api.github.com/app/installations/${APP_ID***REMOVED***/access_tokens"
echo "Requesting registration URL at '${registration_url***REMOVED***'"

payload=$(curl -H "Authorization: Bearer ${jwt_token***REMOVED***" \
-H "Accept: application/vnd.github.v3+json" \
https://api.github.com/app/installations***REMOVED***
installation_id=$(echo $payload | jq '.[0***REMOVED***.id'***REMOVED***

payload=$(curl -X POST -H "Authorization: Bearer ${jwt_token***REMOVED***" \
-H "Accept: application/vnd.github+json" \
-H "X-GitHub-Api-Version: 2022-11-28" \
https://api.github.com/app/installations/${installation_id***REMOVED***/access_tokens***REMOVED***

registration_token=$(echo $payload | jq .token --raw-output***REMOVED***

payload=$(curl -L \
-X POST \
-H "Accept: application/vnd.github+json" \
-H "Authorization: token ${registration_token***REMOVED***" \
-H "X-GitHub-Api-Version: 2022-11-28" \
https://api.github.com/repos/subworkers/ojitong/actions/runners/registration-token***REMOVED***

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