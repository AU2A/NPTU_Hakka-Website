import os
from datetime import datetime

time = 10

for i in os.listdir('openai/upload'):
    if(datetime.now().timestamp()-os.path.getctime('openai/upload/'+i)>time):
        # print(i)
        # print(datetime.now().timestamp()-os.path.getctime('openai/upload/'+i))
        os.remove('openai/upload/'+i)


for i in os.listdir('openai/decode'):
    if(datetime.now().timestamp()-os.path.getctime('openai/decode/'+i)>time):
        # print(i)
        # print(datetime.now().timestamp()-os.path.getctime('openai/upload/'+i))
        os.remove('openai/decode/'+i)

for i in os.listdir('upload'):
    if(datetime.now().timestamp()-os.path.getctime('upload/'+i)>time):
        # print(i)
        # print(datetime.now().timestamp()-os.path.getctime('openai/upload/'+i))
        os.remove('upload/'+i)