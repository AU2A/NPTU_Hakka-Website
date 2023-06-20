#!/bin/bash

echo $domain > domainName
# echo "test.corelab.dev" > domainName

python3 init.py

# parallel ::: "node website/server.js" "python3 openai/delete.py" "python3 openai/openai_whisper.py" "python3 openai/openai_whisper.py" "python3 openai/openai_whisper.py"

python3 openai/openai_whisper.py & python3 openai/openai_whisper.py & python3 openai/openai_whisper.py & python3 openai/delete.py & node website/server.js