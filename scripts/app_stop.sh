#!/usr/bin/env bash
#!/usr/bin/env bash
[ "$(docker ps -q)" ] && docker stop $(docker ps -aq) || true
[ "$(docker ps -aq)" ] && docker rm -f $(docker ps -aq) || true
