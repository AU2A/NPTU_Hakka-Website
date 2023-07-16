import os
import time

def main():
    delayTime = 86400
    while(True):
        time.sleep(delayTime)
        print('clean file')
        print(time.time())
        for i in os.listdir('openai/upload'):
            if(i!='README.md' and time.time()-os.path.getctime('openai/upload/'+i)>delayTime):
                # print(i)
                # print(datetime.now().timestamp()-os.path.getctime('openai/upload/'+i))
                os.remove('openai/upload/'+i)
        for i in os.listdir('openai/decode'):
            if(i!='README.md' and time.time()-os.path.getctime('openai/decode/'+i)>delayTime):
                os.remove('openai/decode/'+i)

        for i in os.listdir('upload'):
            if(time.time()-os.path.getctime('upload/'+i)>delayTime):
                os.remove('upload/'+i)

        for i in os.listdir('decode'):
            if(i!='README.md' and time.time()-os.path.getctime('decode/'+i)>delayTime):
                os.remove('decode/'+i)

if __name__=="__main__":
    main()