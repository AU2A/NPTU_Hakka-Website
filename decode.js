const cors = require('cors')
const execSync = require('child_process').execSync
const express = require('express')
const fs = require('fs')
const https = require('https')
const app = express()
const port = 5002

app.use(cors())

const corsOptions = {
    origin: [
        'https://localhost:5002',
    ],
    methods: 'GET,HEAD,PUT,PATCH,POST,DELETE,OPTIONS',
    allowedHeaders: ['Content-Type', 'Authorization'],
}

var privateKey = fs.readFileSync('/etc/letsencrypt/live/hakka.corelab.dev/privkey.pem', 'utf8')
var certificate = fs.readFileSync('/etc/letsencrypt/live/hakka.corelab.dev/cert.pem', 'utf8')
var ca = fs.readFileSync('/etc/letsencrypt/live/hakka.corelab.dev/chain.pem', 'utf8');
var credentials = {
	key: privateKey,
	cert: certificate,
	ca: ca
};

app.use(cors(corsOptions))

app.get('/decode', (req, res) => {
    tag=req.originalUrl.split('tag=')[1].split('.')[0]
    var temp=''
    try{
        if(tag.split('_')[0]=='ai'){
            temp = execSync('cat openai/decode/'+tag+'_html.txt', { shell: 'bash', encoding: 'utf-8' })
        }else{
            temp = execSync('cat decode/'+tag+'.txt', { shell: 'bash', encoding: 'utf-8' })
        }
    }catch{
        temp=''
    }
    // var output = ''
    // var outputArry = temp.split('\n')
    // for (let i = 0; i < outputArry.length; i++) {
    //     if (outputArry[i] != '') {
    //         var nowLine = outputArry[i].split('\r')
    //         var endIndex = nowLine.length - 1
    //         if (nowLine[endIndex] == '') {
    //             output = output + '<br>' + nowLine[endIndex - 1]
    //             console.log(nowLine[endIndex - 1])
    //         } else {
    //             output = output + '<br>' + nowLine[endIndex]
    //             console.log(nowLine[endIndex])
    //         }
    //     }
    // }
    if(temp==''){
        temp='請稍後...'
    }
    res.send(temp)
})

app.get('/decodeyt', (req, res) => {
    tag=req.originalUrl.split('tag=')[1].split('.')[0]
    var temp=''
    try{
        temp = execSync('cat openai/decode/'+tag+'.srt', { shell: 'bash', encoding: 'utf-8' })
    }catch{
        temp=''
    }
    if(temp==''){
        temp='請稍後...'
    }
    res.send(temp)
})

// app.listen(port, () => {
//     console.log(`Example app listening at http://localhost:${port}`)
// })
https.createServer(credentials, app).listen(port, function () {
    console.log('Express https server listening on port ' + port)
  })