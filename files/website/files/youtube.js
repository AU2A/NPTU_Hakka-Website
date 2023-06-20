var domainName = 'test.corelab.dev'

var tag = document.createElement('script');
tag.src = 'https://www.youtube.com/iframe_api';
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
        height: '360',
        width: '640',
        videoId: '',
        playerVars: {
            'playsinline': 1
        },
        events: {
            'onError': onError,
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
}

function onPlayerReady(event) {
    // event.target.playVideo();
}

var errorStatus = false;
function onError(event) {
    console.log('Error')
    errorStatus = true;
    alert('影片網址有誤，請檢查')
}

var done = false;
function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PLAYING && !done) {
        // setTimeout(stopVideo, 6000);
        done = true;
    }
}

function stopVideo() {
    player.stopVideo();
}

var tagurl = ''
var lyric = ''
var hakka = false
var lyric_hakka = ''
var now_lang = ''
var val =''
var reload=false;

function reloadurl() {
    reload=true
    val = document.getElementById('url').value;
    document.getElementById('player').style.visibility = 'hidden';
    errorStatus = false
    // console.log(val)
    tagurl = ''
    lyric = ''
    player.loadVideoById(videoId = val, startSeconds = 0)
    if (!errorStatus) {
        fetch('https://'+domainName+'/uploadyt?url=' + val + '&model=' + document.getElementById('lang').value, {
            method: 'get',
        }).then(res => res.text()).then(res => {
            if (document.getElementById('lang').value == 0) {
                now_lang = 'tiny: '
            }
            else if (document.getElementById('lang').value == 1) {
                now_lang = 'base: '
            }
            else if (document.getElementById('lang').value == 2) {
                now_lang = 'small: '
            }
            else if (document.getElementById('lang').value == 3) {
                now_lang = 'medium: '
            }
            else if (document.getElementById('lang').value == 4) {
                now_lang = 'hakka: '
            }
            if (document.getElementById('lang').value == 4) {
                hakka = true
            } else {
                hakka = false
            }
            tagurl = res
            console.log(tagurl);
            player.stopVideo();
        })
    }
    reload=false

}

function autoRefresh() {
    if (!errorStatus && tagurl != '') {
        console.log(player.playerInfo.currentTime);
        fetch('https://'+domainName+':5002/decodeyt?tag=' + tagurl, {
            method: 'get',
        }).then(res => res.text()).then(res => {
            lyric = res.split('*****');
        })
        if (hakka == true) {
            fetch('https://'+domainName+':5002/decodeyt?tag=' + tagurl.split('!!!')[0] + '!!!1', {
                method: 'get',
            }).then(res => res.text()).then(res => {
                lyric_hakka = res.split('*****');
            })
        }
    }
}
setInterval('autoRefresh()', 1000);

var cnt=0
function refreshlyric() {
    if(val==""){
        document.getElementById('response').style.visibility = 'hidden';
    }
    else if (!reload&&lyric[0] != '請稍後...' &&player.playerInfo.currentTime==0) {
        document.getElementById('response').style.visibility = 'visible';
        document.getElementById('player').style.visibility = 'visible';
        document.getElementById('response').innerHTML = "辨識完成，請播放"
    }
    else if (!reload&&lyric[0] != '請稍後...') {
        document.getElementById('player').style.visibility = 'visible';
        curtime = player.playerInfo.currentTime*100
        for (i = 0; i < lyric.length; i++) {
            now = lyric[i].split('!!!')
            if (now[0] < curtime && curtime < now[1]) {
                document.getElementById('response').innerHTML = now_lang + now[2]
                break;
            }
        }
        if (hakka == true) {
            document.getElementById('response').innerHTML += '<br> base: '
            curtime = player.playerInfo.currentTime*100
            for (i = 0; i < lyric_hakka.length; i++) {
                now = lyric_hakka[i].split('!!!')
                if (now[0] < curtime && curtime < now[1]) {
                    document.getElementById('response').innerHTML += now[2]
                    break;
                }
            }
        }
        else {
            document.getElementById('responsehakka').innerHTML = ''
        }
    }
    else {
        document.getElementById('player').style.visibility = 'hidden';
        player.stopVideo();
        cnt=(cnt+1)%6;
        var temp = "請稍後"
        for(i=0;i<cnt;i++){
            temp+="."
        }
        document.getElementById('response').innerHTML = temp
    }
}
setInterval('refreshlyric()', 100);