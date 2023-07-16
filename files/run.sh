#!/bin/bash

trap ctrl_c INT

function ctrl_c() {
    echo ""
    echo "GoodBye~"
    kill $(ps -ef | grep "python3 openai/openai_whisper.py" | grep -v "grep" | awk '{print $2}')
    kill $(ps -ef | grep "python3 openai/delete.py" | grep -v "grep" | awk '{print $2}')
    exit 0
}

echo $psw > initFiles/psw

temp=$(md5sum initFiles/psw)
ans=$(cat initFiles/ans)
echo ans
if [ "$temp" = "$ans" ]; then
    echo "Welcome. Starting server~"
    echo $domain > domainName
    # echo "test.corelab.dev" > domainName

    python3 init.py
    python3 openai/openai_whisper.py & python3 openai/delete.py & node website/server.js
else
    echo "Wrong Password. Bye Bye~"
fi