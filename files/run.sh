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
    
    if [ "$domain" != "" ]; then
        echo "domain: " $domain
        echo $domain > initFile
    else
        echo "domain: local.corelab.dev" 
        echo "local.corelab.dev" > initFile
    fi
    
    if [ "$port1" != "" ]; then
        echo "Port1: " $port1
        echo $port1 >> initFile
    else
        echo "Port1: 443" 
        echo "443" >> initFile
    fi
        
    if [ "$port2" != "" ]; then
        echo "Port2: " $port2
        echo $port2 >> initFile
    else
        echo "Port2: 5002" 
        echo "5002" >> initFile
    fi

    # echo "test.corelab.dev" > domainName

    python3 init.py
    python3 openai/openai_whisper.py & python3 openai/delete.py & node website/server.js
else
    echo "Wrong Password. Bye Bye~"
fi