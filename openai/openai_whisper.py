import whisper
import time
import os
import multiprocessing as mp


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