const execSync = require('child_process').execSync
const express = require('express')
const fs = require('fs')
const https = require('https')
const multer = require("multer")
const app = express()
const port = 5001

// 設定 view engine
app.set('view engine', 'ejs')
app.set('views', './views')

const storage = multer.diskStorage({
  filename: function (req, file, cb) {
    cb(null, file.originalname)
  },
  destination: function (req, file, cb) {
    cb(null, './upload')
  },
})

const upload = multer({ storage })

var hskey = fs.readFileSync('ssl/server-key.pem', 'utf8')
var hscert = fs.readFileSync('ssl/server-cert.pem', 'utf8')
var credentials = {
  key: hskey,
  cert: hscert
}

app.get('/', (req, res) => {
  res.render('index')
})

app.post('/upload_files', upload.any('file'), (req, res) => {
  var fileInfo = req.files[0]
  console.log(fileInfo.path)
  // execSync('mv ' + fileInfo.path + ' upload/audio.wav', { shell: 'bash', encoding: 'utf-8' })
  const output = ''
  // const output = execSync('sox ' + fileInfo.path + ' -t raw -c 1 -b 16 -r 16000 -e signed-integer - | tee >(play -t raw -r 16000 -e signed-integer -b 16 -c 1 -q -) |pv -L 16000 -q | nc -N localhost 5050 > decode/output.txt', { shell: 'bash', encoding: 'utf-8' })
  console.log(output)
})

app.get('/decode', (req, res) => {
  const output = execSync('cat decode/output.txt', { shell: 'bash', encoding: 'utf-8' })
  console.log(output)
  res.send(output)
})

// app.listen(port, () => {
//   console.log(`Example app listening at http://localhost:${port}`)
// })
https.createServer(credentials, app).listen(port, function () {
  console.log('Express https server listening on port ' + port)
})