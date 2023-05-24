const execSync = require('child_process').execSync
const express = require('express')
const fs = require('fs')
const https = require('https')
const multer = require("multer")
const app = express()
const port = 443

var date = new Date();

app.set('view engine', 'ejs')
app.set('views', './views')
// app.set('demo', './demo')

app.use(express.static('static'));
app.use(express.static(__dirname, { dotfiles: 'allow' }));

app.use(express.static(__dirname + '/files'));

// app.use(express.static(__dirname + '/demo'));

const storage = multer.diskStorage({
  filename: function (req, file, cb) {
    cb(null, file.originalname)
  },
  destination: function (req, file, cb) {
    cb(null, './upload')
  },
})

const upload = multer({ storage })

var privateKey = fs.readFileSync('/etc/letsencrypt/live/hakka.corelab.dev/privkey.pem', 'utf8')
var certificate = fs.readFileSync('/etc/letsencrypt/live/hakka.corelab.dev/cert.pem', 'utf8')
var ca = fs.readFileSync('/etc/letsencrypt/live/hakka.corelab.dev/chain.pem', 'utf8');
var credentials = {
  key: privateKey,
  cert: certificate,
  ca: ca
};

app.get('/', (req, res) => {
  fs.writeFile('decode/output.txt', '', (err) => {
    if (err) throw err;
  })
  res.render('index')
})
app.get('/youtube', (req, res) => {
  res.render('youtube')
})
app.get('/recorder', (req, res) => {
  res.render('recorder')
})

// app.get('/screen', (req, res) => {
//   res.render('screen')
// })

app.post('/upload_files', upload.any('file'), (req, res) => {
  lang = req.originalUrl.split('?lang=')[1]
  var fileInfo = req.files[0]
  if (fileInfo.path.endsWith('.wav')||fileInfo.path == 'upload/blob'){
    if (lang < 3) {
      if (lang == 0) {
        newFileName = 'chinese_'
      } else if(lang==1) {
        newFileName = 'hakka_'
      }else {
        newFileName = 'chAndHa_'
      }
      if (fileInfo.path == 'upload/blob') {
        newFileName = 'upload/' + newFileName + 'record_' + Date.now() + '.wav'
      } else {
        newFileName = 'upload/' + newFileName + 'upload_' + Date.now() + '.wav'
        // fileInfo.path.split('.')[0]+'_'+Date.now()+'.'+fileInfo.path.split('.')[1]
      }
      console.log(fileInfo.path)
  
      execSync('mv ' + fileInfo.path + ' ' + newFileName, { shell: 'bash', encoding: 'utf-8' })
      execSync('sox ' + newFileName + ' -e signed -c 1 -r 16000 -b 16 ' + newFileName.split('.wav')[0] + '.new.wav', { shell: 'bash', encoding: 'utf-8' })
      execSync('mv ' + newFileName.split('.wav')[0] + '.new.wav ' + newFileName, { shell: 'bash', encoding: 'utf-8' })
      execSync('echo \"' + newFileName + '\" >> decodeList.txt', { shell: 'bash', encoding: 'utf-8' })
      // execSync('sox upload/audio.wav -t raw -c 1 -b 16 -r 16000 -e signed-integer - | tee >(play -t raw -r 16000 -e signed-integer -b 16 -c 1 -q -) |pv -L 16000 -q | nc -N localhost 5050 > decode/output.txt', { shell: 'bash', encoding: 'utf-8' })
      // execSync('ffprobe upload/audio.wav 2>&1 | grep -A1 Duration: > decode/output.txt', { shell: 'bash', encoding: 'utf-8' })
      res.send(newFileName)
    } else if (lang == 3) {
      newFileName = 'ai_'
      if (fileInfo.path == 'upload/blob') {
        newFileName = 'upload/' + newFileName + 'record_' + Date.now() + '.wav'
      } else {
        newFileName = 'upload/' + newFileName + 'upload_' + Date.now() + '.wav'
        // fileInfo.path.split('.')[0]+'_'+Date.now()+'.'+fileInfo.path.split('.')[1]
      }
      console.log(newFileName)
      execSync('mv ' + fileInfo.path + ' ' + newFileName, { shell: 'bash', encoding: 'utf-8' })
      execSync('sox ' + newFileName + ' -e signed -c 1 -r 16000 -b 16 ' + newFileName.split('.wav')[0] + '.new.wav', { shell: 'bash', encoding: 'utf-8' })
      execSync('mv ' + newFileName.split('.wav')[0] + '.new.wav ' + newFileName, { shell: 'bash', encoding: 'utf-8' })
      execSync('echo \"' + newFileName + '\" >> aidecodeList.txt', { shell: 'bash', encoding: 'utf-8' })
      res.send(newFileName)
    }
  }else{
    res.send("wrongFileName")
  }
  
})

// app.get('/decode', (req, res) => {
//   const output = execSync('cat decode/output.txt', { shell: 'bash', encoding: 'utf-8' })
//   console.log(output)
//   res.send(output)
// })

app.get('/uploadyt', (req, res) => {
  tag = req.originalUrl.split('url=')[1].split('&model=')[0]
  model = req.originalUrl.split('model=')[1]
  var temp = ''
  try {
    console.log('echo "https://www.youtube.com/watch?v=' + tag + '///' + model + '" >> aidecodeList.txt')
    execSync('echo "https://www.youtube.com/watch?v=' + tag + '///' + model + '" >> aidecodeList.txt', { shell: 'bash', encoding: 'utf-8' })
    if (model == 4) {
      console.log('echo "https://www.youtube.com/watch?v=' + tag + '///1" >> aidecodeList.txt')
      execSync('echo "https://www.youtube.com/watch?v=' + tag + '///1" >> aidecodeList.txt', { shell: 'bash', encoding: 'utf-8' })
    }
    // if(tag.split('_')[0]=='ai'){
    //     temp = execSync('cat openai/'+tag+'_html.txt', { shell: 'bash', encoding: 'utf-8' })
    // }else{
    //     temp = execSync('cat decode/'+tag+'.txt', { shell: 'bash', encoding: 'utf-8' })
    // }
  } catch {
    temp = ''
  }
  res.send(tag + '!!!' + model)
})

app.get('/use_demo', (req, res) => {
  tag = req.originalUrl.split('id=')[1]
  if(tag=='0'){
    orfileName='hakka_test1'
    fileName='hakka_test1_'+Date.now()
  }
  else if(tag=='1'){
    orfileName='hakka_test2'
    fileName='hakka_test2_'+Date.now()
  }
  else if(tag=='2'){
    orfileName='hakka_test3'
    fileName='hakka_test3_'+Date.now()
  }

  execSync('cp demo/' + orfileName + '.wav upload/' + fileName + '.wav', { shell: 'bash', encoding: 'utf-8' })
  execSync('sox upload/' + fileName + '.wav -e signed -c 1 -r 16000 -b 16 upload/' + fileName + '.new.wav', { shell: 'bash', encoding: 'utf-8' })
  execSync('mv upload/' + fileName + '.new.wav upload/' + fileName+'.wav', { shell: 'bash', encoding: 'utf-8' })
  execSync('echo \"upload/' + fileName + '.wav\" >> decodeList.txt', { shell: 'bash', encoding: 'utf-8' })

  res.send(fileName)
})

// app.listen(port, () => {
//   console.log(`Example app listening at http://localhost:${port}`)
// })

https.createServer(credentials, app).listen(port, function () {
  console.log('Express https server listening on port ' + port)
})
