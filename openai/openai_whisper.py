import whisper
import time
import os
import multiprocessing as mp
from pytube import YouTube
from datetime import timedelta



def decode():
    while True:
        while os.path.exists("/home/aura/hakka_web/openai/lock"):
            time.sleep(0.1)
        try:
            lock = open("/home/aura/hakka_web/openai/lock", "x")
            lock.close
        except:
            time.sleep(0.1)
        f = open('/home/aura/hakka_web/aidecodeList.txt', 'r')
        now=f.readlines()
        f.close()
        if len(now)>0:
            new_file = open("/home/aura/hakka_web/aidecodeList.txt", "w")
            for i in range(1,len(now)):
                new_file.write(now[i])
            new_file.close()
            os.remove("/home/aura/hakka_web/openai/lock")
            path=now[0].split('\n')[0]
            if(path.split('://')[0]=='https'):
                print(path)
                yt = YouTube(path.split('///')[0])
                if yt.length < 5400:
                    video = yt.streams.filter(only_audio=True).first()
                    out_file=video.download(output_path="upload/")
                    base, ext = os.path.splitext(out_file)
                    new_file = base+'.mp3'
                    os.rename(out_file, new_file)
                    if(path.split('///')[1]=='0'):
                        model = whisper.load_model('tiny')
                        print("tiny model loaded.")
                    elif(path.split('///')[1]=='1'):
                        model = whisper.load_model('base')
                        print("base model loaded.")
                    elif(path.split('///')[1]=='2'):
                        model = whisper.load_model('small')
                        print("small model loaded.")
                    elif(path.split('///')[1]=='3'):
                        model = whisper.load_model('medium')
                        print("medium model loaded.")
                    elif(path.split('///')[1]=='4'):
                        model = whisper.load_model('/home/aura/openai/model/whisper-base-hakka-au2a.pt')
                        print("hakka model loaded.")
                    transcribe = model.transcribe(audio=new_file)
                    segments = transcribe['segments']
                    output_file=open('decode/'+path.split('watch?v=')[1].split('///')[0]+'.srt','w',encoding='utf8')
                    # print(segments)
                    for segment in segments:
                        start = int(segment['start'])
                        end = int(segment['end'])
                        startm, starts = divmod(start, 60)
                        starth, startm = divmod(startm, 60)
                        endm, ends = divmod(end, 60)
                        endh, endm = divmod(endm, 60)
                        (start//3600)
                        # output_file.write(str(segment['id']+1)+'\n'+'{:02d}:{:02d}:{:02d}'.format(starth, startm, starts)+',000 --> '+'{:02d}:{:02d}:{:02d}'.format(endh, endm, ends)+',000\n'+segment['text']+'\n\n')
                        output_file.write(str(start)+','+str(end)+','+segment['text']+'*')
                    output_file.close()
                    print('success '+path+'\n')
                else:
                    print('audio too long')
            else:
                print('../'+path)
                os.system('whisper ../'+path+' --language zh --model medium > '+path.split('/')[1].split('.')[0]+'_time.txt')
                time.sleep(0.1)
                input_file = open(path.split('/')[1].split('.')[0]+'_time.txt','r',encoding='utf8')
                output_file = open(path.split('/')[1].split('.')[0]+'_html.txt','w',encoding='utf8')
                for line in input_file.readlines():
                    output_file.write(line.replace('\n','<br>\n'))
                output_file.close()
                input_file.close()
            
        if os.path.exists("/home/aura/hakka_web/openai/lock"):
            os.remove("/home/aura/hakka_web/openai/lock")
        time.sleep(1)

def main():
    process_list = []
    num_process = 3
    for i in range(num_process):
        process_list.append(mp.Process(target=decode))
    for i in range(num_process):
        process_list[i].start()
    for i in range(num_process):
        process_list[i].join()
    while True:
        time.sleep(0.1)

if __name__=="__main__":
    main()