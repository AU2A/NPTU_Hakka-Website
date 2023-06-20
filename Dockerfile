FROM ubuntu:20.04

MAINTAINER Aura <aura01221@gmail.com>

ENV TZ=Asia/Taipei
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
    ffmpeg \
    nodejs \
    npm \
    # nvidia-cuda-toolkit \
    sox \
    parallel \
    python3-pip

RUN pip3 install openai-whisper pytube ffmpeg-python yt-dlp

COPY ./* /Hakka_Website

WORKDIR /Hakka_Website/website

RUN npm install

WORKDIR /Hakka_Website

EXPOSE 443 5002

ENTRYPOINT ["./run.sh"]
