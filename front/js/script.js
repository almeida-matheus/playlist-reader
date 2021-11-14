const btn_link = document.getElementById('btn_link')
const link = document.getElementById('link')
const btn_download = document.getElementById('btn_download')
const len_songs = document.getElementById('len_songs')
const alert_message = document.querySelector('.alert-message');

const api = {
    base: "http://127.0.0.1:8000/playlist/"
}

function CreateAlert(message) {
    alert_message.parentElement.classList.add('active')
    alert_message.innerHTML = `${message}`
    console.log(`${message}`)
    window.setTimeout(function () { alert_message.parentElement.classList.remove('active') }, 3000);
}

btn_link.addEventListener('click', function () {
    getSongs(link.value)
})

link.addEventListener('keypress', enter)
function enter(event) {
    key = event.keyCode
    if (key === 13) {
        getSongs(link.value)
    }
}

async function loadResponse(param) {
    param_encoded = encodeURIComponent(param)
    let response = await fetch(`${api.base}${param_encoded}`)
    let response_json = await response.json()
    return response_json
}

function ValidateInput(array) {
    let include = array.includes('https://www.youtube.com/playlist?list='); //return True if include in str
    if (include)
        return true
    CreateAlert(`<i class="fas fa-exclamation-triangle"></i> <strong>Erro!</strong> URL invalida`)
}

async function getSongs(link) {
    let validate = ValidateInput(link)
    if (!validate)
        return
    try {
        param = link.replace('https://www.youtube.com/playlist?list=', '')
        response = await loadResponse(param)
    }
    catch (e) {
        CreateAlert(`<i class="fas fa-exclamation-triangle"></i> <strong>Erro!</strong> ${e}`)
        console.log(e)
    }
    if (response.status != 200) {
        CreateAlert(`<i class="fas fa-exclamation-triangle"></i> <strong>Erro!</strong> URL não encontrada`)
        return
    }
    genList(response.videos)
    fillText(response.videos)
}

function genList(response_videos) {

    response_videos.forEach((video) => {
        let a = document.createElement('a');
        a.setAttribute('href', `${video.link_video}`)
        a.setAttribute('class', `card`)
        a.setAttribute('rel', `noopener`)
        a.setAttribute('target', `_blank`)
        a.innerHTML = `
            <div class="card-horizontal">
                <div class="img-square-wrapper">
                    <img src="${video.link_img}"
                        width="64px" height="64px">
                </div>
                <div class="card-body">
                    <h5 class="card-title text-dark">${video.title}</h5>
                </div>
            </div>
        `
        document.getElementById('container_list').appendChild(a)
    });
    len_songs.innerText = response_videos.length
}

function fillText(response_videos) {
    let text = ``
    response_videos.forEach((video) => {
        text = text + video.title + '\n'
    });
    document.getElementById("text-val").value = text
}

function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

btn_download.addEventListener("click", function(){
    var text = document.getElementById("text-val").value;
    var filename = "playlist.txt";
    download(filename, text);
}, false);