set -e
[ "$(docker ps -q)" ] && docker stop $(docker ps -q) || true
[ "$(docker ps -aq)" ] && docker rm -f $(docker ps -aq) || true