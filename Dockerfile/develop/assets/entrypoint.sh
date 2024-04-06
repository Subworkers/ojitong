#!/bin/sh
pem_file_path=${PEM_FILE_PATH}

pip3 install jwt
jwt_token=$(python3 assets/generate_jwt_token.py ${PEM_FILE_PATH} ${APP_ID})

registration_url="https://api.github.com/app/installations/${APP_ID}/access_tokens"
echo "Requesting registration URL at '${registration_url}'"

payload=$(curl --request POST \
--url ${registration_url} \
--header "Accept: application/vnd.github+json" \
--header "Authorization: Bearer ${jwt_token}" \
--header "X-GitHub-Api-Version: 2022-11-28")
export RUNNER_TOKEN=$(echo $payload | jq .token --raw-output)

./config.sh \
    --name ${RUNNER_NAME} \
    --token ${RUNNER_TOKEN} \
    --url https://github.com/${GITHUB_OWNER}/${GITHUB_REPOSITORY} \
    --work ${RUNNER_WORKDIR} \
    --unattended \
    --replace \
    --labels ${RUNNER_LABELS}

remove() {
    ./config.sh remove --unattended --token "${RUNNER_TOKEN}"
}

trap 'remove; exit 130' INT
trap 'remove; exit 143' TERM

./run.sh "$*" &

wait $!