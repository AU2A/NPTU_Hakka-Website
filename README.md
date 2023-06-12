# Hakka_Website

## 安全憑證
因為網頁有使用的錄音功能，所以網頁需要走`https`協定，因此需要申請安全憑證。

我是使用`LetsEncrypt`的安全憑證，每90天需要重新申請一次

參考網站：[Link](https://itnext.io/node-express-letsencrypt-generate-a-free-ssl-certificate-and-run-an-https-server-in-5-minutes-a730fbe528ca)

申請完成憑證後，要去`website/server.js`更改憑證的位置
```javascript=35
var domain_Name = 'New domain name' //要修改的地方

var privateKey = fs.readFileSync('/etc/letsencrypt/live/'+domain_Name+'/privkey.pem', 'utf8')
var certificate = fs.readFileSync('/etc/letsencrypt/live/'+domain_Name+'/cert.pem', 'utf8')
var ca = fs.readFileSync('/etc/letsencrypt/live/'+domain_Name+'/chain.pem', 'utf8');
var credentials = {
  key: privateKey,
  cert: certificate,
  ca: ca
};

```
## 網址
以下檔案也需要修改網址才可以正常執行

`website/files/youtube.js`
```javascript=
var domainName = 'New domain name' //要修改的地方
```
`website/files/recorder.js`
```javascript=
var domainName = 'New domain name' //要修改的地方
```
`views/index.ejs`
```htmlmixed=18
<a class="btn" href="https://*New domain name*/">音檔辨識</a>
<a class="btn" href="https://*New domain name*/youtube">影片辨識</a>
```
`views/youtube.ejs`
```htmlmixed=16
<a class="btn" href="https://*New domain name*/">音檔辨識</a>
<a class="btn" href="https://*New domain name*/youtube">影片辨識</a>
```

## NodeJS
要先到`website/`底下安裝網頁需要的套件
```bash
~/Hakka_Website/website$ npm install
```

## 分開測試
請先分開測試程序與套件是否有缺，請在專案位置執行
`web`
```bash
~/Hakka_Website$ sudo node server.js
```
`whisper`
```bash
~/Hakka_Website$ sudo python3 openai/openai_whisper.py
```

## 執行
```bash
~/Hakka_Website$ sudo ./run.sh
```