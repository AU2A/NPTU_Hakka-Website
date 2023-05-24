
from pytube import YouTube
import time
yt = YouTube('http://www.youtube.com/watch?v=mkggXE5e2yk')
time.sleep(1)
print(yt.title)