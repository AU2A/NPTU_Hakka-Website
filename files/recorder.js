const recordBtn = document.querySelector('.record-btn')
const player = document.querySelector('.audio-player')

var tag=''
var stat = 'Not recording'
var startTime=''
function blobToFile(theBlob, fileName) {
  theBlob.lastModifiedDate = new Date()
  theBlob.name = fileName
  return theBlob
}

function createAudioController(rec) {
  rec && rec.exportWAV((blob) => {
    const url = URL.createObjectURL(blob)
    uploadAudio(blob)
    document.getElementById('src').src = url
    document.getElementById('audio').load();
    
    document.getElementById('downloadBtn').href = url
    document.getElementById('downloadButton').disabled = false
  })
}
if (navigator.mediaDevices.getUserMedia) {
  var chunks = []
  const constraints = { audio: true, video: false }
  
  navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
    console.log('record permission success')

    const audioContext = new AudioContext
    const audioInput = audioContext.createMediaStreamSource(stream)
    const rec = new Recorder(audioInput)

    recordBtn.onclick = () => {
      if (stat === 'recording') {
        stat = 'Not recording'
        rec.stop()
        recordBtn.textContent = '開始錄音'
        console.log('start recording')
        createAudioController(rec)
        rec.clear()
      } else {
        stat = 'recording'
        document.getElementById('recordTime').textContent=0
        startTime=new Date()
        rec.record()
        console.log('recording...')
        recordBtn.textContent = '停止錄音'
      }
      console.log('status：', stat)
    }
  }).catch(function (err) {
    console.log(err);
    if (err.name == "NotFoundError" || err.name == "DevicesNotFoundError") {
      console.log('Required track is missing');
    } else if (err.name == "NotReadableError" || err.name == "TrackStartError") {
      console.log('Webcam or mic are already in use');
    } else if (err.name == "OverconstrainedError" || err.name == "ConstraintNotSatisfiedError") {
      console.log('Constraints can not be satisfied by available devices');
    } else if (err.name == "NotAllowedError" || err.name == "PermissionDeniedError") {
      console.log('Permission Denied.');
    } else if (err.name == "TypeError") {
      console.log('Both audio and video are FALSE');
    } else {
      console.log('Sorry! Another error occurred.');
    }
  });
} else {
  console.error('browser not support getUserMedia')
}


//選擇音檔
const $input = document.querySelector('#upload');
$input.addEventListener('change', event => {
  uploadAudio(event.target.files[0])
})

//上傳音檔
function uploadAudio(bin) {
  const data = new FormData();
  if (bin.size > 209715200) {
    document.getElementById('response').innerHTML = 'Upload audio must be less than 200MB';
  } else {
    data.append('file', bin);
    fetch('/upload_files?lang='+document.getElementById('lang').value, {
      method: 'post',
      body: data
    }).then(res => res.text()).then(res => {
      tag=res.split('upload/')[1]
    })
  }
}

//按鈕取代
const selectFileBtn = document.querySelector('.select-file-btn')
const selectFileBtn2 = document.querySelector('.select-file-btn2')
selectFileBtn.addEventListener("click", function () {
  document.getElementById('upload').value=''
  document.getElementById('recordTime').textContent=''
  selectFileBtn2.click()
});

//刷新解碼結果
function refreshDecode() {
  if(tag!=''){
    fetch('https://hakka.corelab.dev:5002/decode?tag='+tag, {
      method: 'get',
    }).then(res => res.text()).then(res => {
      document.getElementById('response').innerHTML = res;
    })
  }
}
setInterval('refreshDecode()', 1000);

function refreshRecordTime() {
  if(stat=='recording'){
    var minute = parseInt((new Date()-startTime)/60000)
    var second = parseInt((new Date()-startTime)/1000)%60
    var output = minute+':'
    if(minute<10){
      output='0'+output
    }
    if(second<10){
      output=output+'0'+second
    }else{
      output=output+second
    }
    document.getElementById('recordTime').textContent=output
  }
}
setInterval('refreshRecordTime()', 100);

//檔案變更
function handleFiles(event) {
  var files = event.target.files;
  var url = URL.createObjectURL(files[0])
  $('#src').attr('src', url);
  document.getElementById('audio').load();

  document.getElementById('downloadBtn').href = url
  document.getElementById('downloadButton').disabled = false
}
document.getElementById('upload').addEventListener('change', handleFiles, false);



const volumeMeterEl = document.getElementById('volumeMeter');
window.onload = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
    const audioContext = new AudioContext();
    const mediaStreamAudioSourceNode = audioContext.createMediaStreamSource(stream);
    const analyserNode = audioContext.createAnalyser();
    mediaStreamAudioSourceNode.connect(analyserNode);

    const pcmData = new Float32Array(analyserNode.fftSize);
    const onFrame = () => {
        analyserNode.getFloatTimeDomainData(pcmData);
        let sumSquares = 0.0;
        for (const amplitude of pcmData) { sumSquares += amplitude*amplitude; }
        volumeMeterEl.value = Math.sqrt(sumSquares / pcmData.length);
        window.requestAnimationFrame(onFrame);
    };
    window.requestAnimationFrame(onFrame);
};