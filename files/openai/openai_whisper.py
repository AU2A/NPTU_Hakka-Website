import warnings
warnings.filterwarnings("ignore", message=".*The 'nopython' keyword.*")

import whisper
import time
import os
import multiprocessing as mp
import shutil
import random
import librosa
from pytube import YouTube
from datetime import timedelta
from datetime import datetime

model_tiny = whisper.load_model('openai/model/tiny.pt')
model_base = whisper.load_model('openai/model/base.pt')
model_small = whisper.load_model('openai/model/small.pt')
model_hakka = whisper.load_model('openai/model/whisper-base-zh-20230711.pt')

def main():
    while True:
        f = open('aidecodeList.txt', 'r')
        fileCnt=f.readlines()
        f.close()
        if len(fileCnt)>0:
            # wait for decode files
            while os.path.exists('openai_lock'):
                time.sleep(0.1+0.1*random.randint(1,5))
            lock = open('openai_lock', 'x')
            time.sleep(0.1)
            lock.close()
            f = open('aidecodeList.txt', 'r')
            now=f.readlines()
            f.close()
            new_file = open('aidecodeList.txt', 'w')
            for i in range(1,len(now)):
                new_file.write(now[i])
            new_file.close()
            if os.path.exists('openai_lock'):
                os.remove('openai_lock')
            path=''
            try:
                path=now[0].split('\n')[0]
            except:
                time.sleep(0.1)

            #check decode youtube or record
            decode_start = time.time()
            if(path.split('://')[0]=='https'):
                # check path
                print(path.split('///')[0])
                videoID=path.split('watch?v=')[1].split('///')[0]

                output_file=open('openai/decode/time_'+videoID+'!!!'+path.split('///')[1]+'.srt','w',encoding='utf8')
                output_file.write('downloading')
                output_file.close()

                # download audio
                if not os.path.exists('openai/upload/output_'+videoID+'.wav'):
                    print('start    download output_'+videoID+'.wav')
                    os.system('python3 openai/download.py '+path.split('///')[0]+' > /dev/null')
                    print('complete download output_'+videoID+'.wav')
                    time.sleep(0.1)
                    os.system('mv output_'+videoID+'.wav openai/upload/output_'+videoID+'.wav')
                    os.system('sox openai/upload/output_'+videoID+'.wav -e signed -c 1 -r 16000 -b 16 openai/upload/output_'+videoID+'new.wav')
                    os.system('mv openai/upload/output_'+videoID+'new.wav openai/upload/output_'+videoID+'.wav')
                else:
                    print('output_'+videoID+'.wav exist')

                # decode use time
                output_file=open('openai/decode/time_'+videoID+'!!!'+path.split('///')[1]+'.srt','w',encoding='utf8')
                if(path.split('///')[1]=='4'):
                    output_file.write(str(int(round(librosa.get_duration(path='openai/upload/output_'+videoID+'.wav')/15))))
                # elif(path.split('///')[1]=='3'):
                    # output_file.write(librosa.get_duration(path='openai/upload/output_'+videoID+'.wav')/5)
                elif(path.split('///')[1]=='2'):
                    output_file.write(str(int(round(librosa.get_duration(path='openai/upload/output_'+videoID+'.wav')/10))))
                elif(path.split('///')[1]=='1'):
                    output_file.write(str(int(round(librosa.get_duration(path='openai/upload/output_'+videoID+'.wav')/15))))
                else: # (path.split('///')[1]=='0'):
                    output_file.write(str(int(round(librosa.get_duration(path='openai/upload/output_'+videoID+'.wav')/20))))
                output_file.close()

                if(path.split('///')[1]=='4'):
                    print('hakka model loaded.')
                    transcribe = model_hakka.transcribe(audio='openai/upload/output_'+videoID+'.wav')
                # elif(path.split('///')[1]=='3'):
                #     model = whisper.load_model('openai/model/.pt')
                #     print('medium model loaded.')
                elif(path.split('///')[1]=='2'):
                    print('small model loaded.')
                    transcribe = model_small.transcribe(audio='openai/upload/output_'+videoID+'.wav')
                elif(path.split('///')[1]=='1'):
                    print('base model loaded.')
                    transcribe = model_base.transcribe(audio='openai/upload/output_'+videoID+'.wav')
                else: # (path.split('///')[1]=='0'):
                    print('tiny model loaded.')
                    transcribe = model_tiny.transcribe(audio='openai/upload/output_'+videoID+'.wav')

                segments = transcribe['segments']
                print('openai/decode/'+videoID+'!!!'+path.split('///')[1]+'.srt')
                output_file=open('openai/decode/'+videoID+'!!!'+path.split('///')[1]+'.srt','w',encoding='utf8')
                # print(segments)
                for segment in segments:
                    start = int(segment['start']*100)
                    end = int(segment['end']*100)
                    startm, starts = divmod(start, 6000)
                    starth, startm = divmod(startm, 6000)
                    endm, ends = divmod(end, 6000)
                    endh, endm = divmod(endm, 6000)
                    # (start//3600)
                    # output_file.write(str(segment['id']+1)+'\n'+'{:02d}:{:02d}:{:02d}'.format(starth, startm, starts)+',000 --> '+'{:02d}:{:02d}:{:02d}'.format(endh, endm, ends)+',000\n'+segment['text']+'\n\n')
                    output_file.write(str(start)+'!!!'+str(end)+'!!!'+segment['text']+'*****')
                output_file.close()
                if(path.split('///')[1]=='4'):
                    print('base model loaded.')
                    transcribe = model_base.transcribe(audio='openai/upload/output_'+videoID+'.wav')
                    segments = transcribe['segments']
                    print('openai/decode/'+videoID+'!!!1.srt')
                    output_file=open('openai/decode/'+videoID+'!!!1.srt','w',encoding='utf8')
                    for segment in segments:
                        start = int(segment['start']*100)
                        end = int(segment['end']*100)
                        startm, starts = divmod(start, 6000)
                        starth, startm = divmod(startm, 6000)
                        endm, ends = divmod(end, 6000)
                        endh, endm = divmod(endm, 6000)
                        # (start//3600)
                        # output_file.write(str(segment['id']+1)+'\n'+'{:02d}:{:02d}:{:02d}'.format(starth, startm, starts)+',000 --> '+'{:02d}:{:02d}:{:02d}'.format(endh, endm, ends)+',000\n'+segment['text']+'\n\n')
                        output_file.write(str(start)+'!!!'+str(end)+'!!!'+segment['text']+'*****')
                    output_file.close()
                print('success '+path+'\n')
            elif path!='':
                print(path)
                file_name=path.split('/')[1].split('.')[0]

                output_file=open('openai/decode/time_'+file_name+'_html.txt','w',encoding='utf8')
                output_file.write(str(int(round(librosa.get_duration(path=path)/15))))
                output_file.close()

                if file_name[0:2]=='ha':
                    print('hakka base model loaded.')
                    transcribe = model_hakka.transcribe(audio=path)
                else:
                    print('base model loaded.')
                    transcribe = model_base.transcribe(audio=path)
                segments = transcribe['segments']
                print('openai/decode/'+file_name+'_html.txt')
                output_file=open('openai/decode/'+file_name+'_html.txt','w',encoding='utf8')
                for segment in segments:
                    start = int(segment['start']*100)
                    end = int(segment['end']*100)
                    startm, starts = divmod(start, 6000)
                    starth, startm = divmod(startm, 6000)
                    endm, ends = divmod(end, 6000)
                    endh, endm = divmod(endm, 6000)
                    # (start//3600)
                    # output_file.write(str(segment['id']+1)+'\n'+'{:02d}:{:02d}:{:02d}'.format(starth, startm, starts)+',000 --> '+'{:02d}:{:02d}:{:02d}'.format(endh, endm, ends)+',000\n'+segment['text']+'\n\n')
                    output_file.write(str(start)+'!!!'+str(end)+'!!!'+segment['text']+'*****')
                output_file.close()
                print('success '+path+'\n')
            decode_end = time.time()
            print(f'Use time {decode_end-decode_start}\n')


        # time.sleep(0.1)
        # while os.path.exists(fileRootDir+'/openai_lock'):
        #     try:
        #         os.remove(fileRootDir+'/openai_lock')
        #     except:
        #         time.sleep(0.1)
        time.sleep(1.0+0.5*random.randint(1,6))

if __name__=='__main__':
    main()
