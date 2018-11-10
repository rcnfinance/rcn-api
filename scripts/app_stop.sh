[ "$(docker ps -q)" ] && docker stop $(docker ps -q)
[ "$(docker ps -aq)" ] && docker rm -f $(docker ps -aq)