#!/bin/bash
i=1
while true; do
  echo "stream packet $i" | socat - UDP:172.16.123.3:300
  sleep 0.2    # 5 packets per second; adjust for desired rate
  i=$((i + 1))
done
