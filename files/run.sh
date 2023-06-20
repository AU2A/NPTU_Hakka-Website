#!/bin/bash

echo $psw > initFiles/psw

temp=$(md5sum initFiles/psw)
ans=$(cat initFiles/ans)

if [ "$temp" = "$ans" ]; then
    echo $domain > domainName
    # echo "test.corelab.dev" > domainName

    python3 init.py
    python3 openai/openai_whisper.py & python3 openai/openai_whisper.py & python3 openai/openai_whisper.py & python3 openai/delete.py & node website/server.js
else
    echo "Wrong Password. Bye Bye~"
fi