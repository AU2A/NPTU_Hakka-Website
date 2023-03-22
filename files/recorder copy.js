const recordBtn = document.querySelector(".record-btn");
const player = document.querySelector(".audio-player");

function blobToFile(theBlob, fileName){
  //A Blob() is almost a File() - it's just missing the two properties below which we will add
  theBlob.lastModifiedDate = new Date();
  theBlob.name = fileName;
  return theBlob;
}

if (navigator.mediaDevices.getUserMedia) {
  var chunks = [];
  const constraints = { audio: true};
  navigator.mediaDevices.getUserMedia(constraints).then(
    stream => {
      console.log("record permission success");

      const mediaRecorder = new MediaRecorder(stream);

      recordBtn.onclick = () => {
        if (mediaRecorder.state === "recording") {
          mediaRecorder.stop();
          recordBtn.textContent = "record";
          console.log("start recording");
        } else {
          mediaRecorder.start();
          console.log("recording...");
          recordBtn.textContent = "stop";
        }
        console.log("status：", mediaRecorder.state);
      };

      mediaRecorder.ondataavailable = e => {
        chunks.push(e.data);

      };

      mediaRecorder.onstop = e => {
        mediaRecorder
        // var blob = new Blob(chunks, { type: "audio/ogg; codecs=opus" });
        var blob = new Blob([chunks[chunks.length-1]], { type: "audio/wav; codecs=0" });
        chunks = [];
        var audioURL = window.URL.createObjectURL(blob);
        player.src = audioURL;
        console.log(audioURL)
        var file = blobToFile(blob, "audio.wav");
        const data = new FormData();
        data.append('file', file);
        fetch('/upload_files', {
          method: 'post',
          body: data
        }).then(res => res.text()).then(res => {
          const log = document.createElement('p');
          //   document.body.appendChild！(log);
          // document.getElementById("response").innerHTML = res;
        })
      };
    },
    () => {
      console.error("record permission failed");
    }
  );
} else {
  console.error("browser not support getUserMedia");
}