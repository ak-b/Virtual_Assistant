set -a; source ~/.env; set +a;
docker run -d -e BOT_NAME={$BOT_NAME} -e BOT_TOKEN={$BOT_TOKEN} -e BOT_USERNAME={$BOT_USERNAME} -e BOT_PASSWORD={$BOT_PASSWORD} -e ENABLE_PASSWORD={$ENABLE_PASSWORD}  -v $PWD/k8s/users.properties:/opt/wibot/users.properties registry-qa.webex.com/marvin:test7
