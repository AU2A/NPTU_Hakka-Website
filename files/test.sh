#!/bin/bash

echo "domain" > domainName

trap ctrl_c INT

function ctrl_c() {
    echo ""
    echo "GoodBye~"
    kill $(ps -ef | grep "python3 openai/openai_whisper.py" | grep -v "grep" | awk '{print $2}')
    kill $(ps -ef | grep "python3 openai/delete.py" | grep -v "grep" | awk '{print $2}')
    exit 0
}

python3 init.py
python3 openai/openai_whisper.py & python3 openai/delete.py & node website/server.js