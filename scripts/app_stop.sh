#!/usr/bin/env bash
#!/usr/bin/env bash
docker stop $(docker ps -aq) || true
docker rm -f $(docker ps -aq) || true
