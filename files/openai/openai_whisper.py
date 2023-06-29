import warnings
warnings.filterwarnings("ignore", message=".*The 'nopython' keyword.*")

import whisper
import time
import os
import multiprocessing as mp
import shutil
import random
from pytube import YouTube
from datetime import timedelta
from datetime import datetime

def main():
    while True:
        f = open('aidecodeList.txt', 'r')
        fileCnt=f.readlines()
        f.close()
        if len(fileCnt)>0:
            # print(fileCnt)
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

            if(path.split('://')[0]=='https'):
                print(path.split('///')[0])
                videoID=path.split('watch?v=')[1].split('///')[0]
                if not os.path.exists('openai/upload/output_'+videoID+'.wav'):
                    print('start    download output_'+videoID+'.wav')
                    os.system('python3 openai/download.py '+path.split('///')[0]+' > /dev/null')
                    print('complete download output_'+videoID+'.wav')
                    time.sleep(0.1)
                    os.system('mv output_'+videoID+'.wav openai/upload/output_'+videoID+'.wav')
                else:
                    print('output_'+videoID+'.wav exist')
                if  (path.split('///')[1]=='0'):
                    model = whisper.load_model('openai/model/tiny.pt')
                    print('tiny model loaded.')
                elif(path.split('///')[1]=='1'):
                    model = whisper.load_model('openai/model/base.pt')
                    print('base model loaded.')
                elif(path.split('///')[1]=='2'):
                    model = whisper.load_model('openai/model/small.pt')
                    print('small model loaded.')
                # elif(path.split('///')[1]=='3'):
                #     model = whisper.load_model('openai/model/.pt')
                #     print('medium model loaded.')
                elif(path.split('///')[1]=='4'):
                    model = whisper.load_model('openai/model/whisper-base-zh-20230628.pt')
                    print('hakka model loaded.')
                transcribe = model.transcribe(audio='openai/upload/output_'+videoID+'.wav')
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
                    model = whisper.load_model('openai/model/base.pt')
                    print('base model loaded.')
                    transcribe = model.transcribe(audio='openai/upload/'+videoID+'.wav')
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
                model = whisper.load_model('openai/model/whisper-base-zh-20230628.pt')
                print('base model loaded.')
                transcribe = model.transcribe(audio=path)
                segments = transcribe['segments']
                file_name=path.split('/')[1].split('.')[0]
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

        # time.sleep(0.1)
        # while os.path.exists(fileRootDir+'/openai_lock'):
        #     try:
        #         os.remove(fileRootDir+'/openai_lock')
        #     except:
        #         time.sleep(0.1)
        time.sleep(1.0+0.5*random.randint(1,6))

if __name__=='__main__':
    main()
