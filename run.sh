#!/bin/bash

node website/server.js &
python3 openai/openai_whisper.py
