f = open('domainName','r')
domain = f.readlines()[0].split('\n')[0]
f.close()

f = open('initFiles/server.js','r')
o = open('website/server.js','w')

content = f.readlines()

for i in range(34):
    o.write(content[i])

o.write('var domainName = \''+domain+'\'\n\n')

for i in range(36,202):
    o.write(content[i])

f.close()
o.close()

f = open('initFiles/youtube.js','r')
o = open('website/files/youtube.js','w')

content = f.readlines()

o.write('var domainName = \''+domain+'\'\n\n')

for i in range(2,163):
    o.write(content[i])

f.close()
o.close()

f = open('initFiles/recorder.js','r')
o = open('website/files/recorder.js','w')

content = f.readlines()

o.write('var domainName = \''+domain+'\'\n\n')

for i in range(2,242):
    o.write(content[i])

f.close()
o.close()

f = open('initFiles/index.ejs','r')
o = open('views/index.ejs','w')

content = f.readlines()

for i in range(17):
    o.write(content[i])

o.write('            <a class="btn" href="https://'+domain+'/">音檔辨識</a>\n')
o.write('            <a class="btn" href="https://'+domain+'/youtube">影片辨識</a>\n')

for i in range(19,66):
    o.write(content[i])

f.close()
o.close()

f = open('initFiles/youtube.ejs','r')
o = open('views/youtube.ejs','w')

content = f.readlines()

for i in range(15):
    o.write(content[i])

o.write('            <a class="btn" href="https://'+domain+'/">音檔辨識</a>\n')
o.write('            <a class="btn" href="https://'+domain+'/youtube">影片辨識</a>\n')

for i in range(17,46):
    o.write(content[i])

f.close()
o.close()