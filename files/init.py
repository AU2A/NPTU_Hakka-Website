f = open('initFile','r').readlines()
domain = f[0].split('\n')[0]
port1 = f[1].split('\n')[0]
port2 = f[2].split('\n')[0]

f = open('initFiles/server.js','r')
o = open('website/server.js','w')

content = f.readlines()

for i in range(8):
    o.write(content[i])
o.write('const port = 443\n\n')
for i in range(10,32):
    o.write(content[i])
o.write('var domainName = \''+domain+'\'\n\n')
for i in range(34,136):
    o.write(content[i])
o.write('const port2 = 5002\n\n')
for i in range(138,142):
    o.write(content[i])
o.write('    \'https://localhost:'+port2+'\',\n')
for i in range(143,len(content)):
    o.write(content[i])

f.close()
o.close()

f = open('initFiles/youtube.js','r')
o = open('website/files/youtube.js','w')

content = f.readlines()

o.write('var domainName = \''+domain+'\'\n\n')
for i in range(2,64):
    o.write(content[i])
o.write('        fetch(\'https://\' + domainName + \':'+port1+'/uploadyt?url=\' + val + \'&model=\' + document.getElementById(\'lang\').value, {\n')
for i in range(65,99):
    o.write(content[i])
o.write('        fetch(\'https://\' + domainName + \':'+port2+'/decodeyt?tag=\' + tagurl, {\n')
for i in range(100,105):
    o.write(content[i])
o.write('            fetch(\'https://\' + domainName + \':'+port2+'/decodeyt?tag=\' + tagurl.split(\'!!!\')[0] + \'!!!1\', {\n')
for i in range(106,len(content)):
    o.write(content[i])

f.close()
o.close()

f = open('initFiles/recorder.js','r')
o = open('website/files/recorder.js','w')

content = f.readlines()

o.write('var domainName = \''+domain+'\'\n\n')
for i in range(2,114):
    o.write(content[i])
o.write('    var url = \'https://\' + domainName + \':'+port1+'/demo/\' + id + \'.wav\'\n')
for i in range(115,150):
    o.write(content[i])
o.write('    fetch(\'https://\' + domainName + \':'+port2+'/decode?tag=\' + tag, {\n')
for i in range(151,len(content)):
    o.write(content[i])

f.close()
o.close()

f = open('initFiles/index.ejs','r')
o = open('views/index.ejs','w')

content = f.readlines()

for i in range(17):
    o.write(content[i])

o.write('            <a class="btn" href="/">音檔辨識</a>\n')
o.write('            <!-- <a class="btn" href="/youtube">影片辨識</a> -->\n')

for i in range(19,len(content)):
    o.write(content[i])

f.close()
o.close()

f = open('initFiles/youtube.ejs','r')
o = open('views/youtube.ejs','w')

content = f.readlines()

for i in range(15):
    o.write(content[i])

o.write('            <a class="btn" href="/">音檔辨識</a>\n')
o.write('            <!-- <a class="btn" href="/youtube">影片辨識</a> -->\n')

for i in range(17,len(content)):
    o.write(content[i])

f.close()
o.close()