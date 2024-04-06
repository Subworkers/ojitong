#!/bin/sh
pem_file_path=${PEM_FILE_PATH}
jwt_token=$(python3 generate_jwt_token.py ${PEM_FILE_PATH} ${APP_ID})

registration_url="https://api.github.com/app/installations/${APP_ID}/access_tokens"
echo "Requesting registration URL at '${registration_url}'"

payload=$(curl -H "Authorization: Bearer ${jwt_token}" \
-H "Accept: application/vnd.github.v3+json" \
https://api.github.com/app/installations)
installation_id=$(echo $payload | jq '.[0].id')

payload=$(curl -X POST -H "Authorization: Bearer ${jwt_token}" \
-H "Accept: application/vnd.github+json" \
-H "X-GitHub-Api-Version: 2022-11-28" \
https://api.github.com/app/installations/${installation_id}/access_tokens)

registration_token=$(echo $payload | jq .token --raw-output)

payload=$(curl -L \
-X POST \
-H "Accept: application/vnd.github+json" \
-H "Authorization: token ${registration_token}" \
-H "X-GitHub-Api-Version: 2022-11-28" \
https://api.github.com/repos/subworkers/ojitong/actions/runners/registration-token)

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