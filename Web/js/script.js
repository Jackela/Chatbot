window.onload = function () {
    switchInput('text');
}
let autoplay = true;

const cuid = "ciy7xg9p600003sxo5b70c99d";// for testing, in real conditon it will be fetched from database
// Toggle autoplay
const toggleAutoplay = () => {
    autoplay = !autoplay;
};


const sendAudioData = (blob, baseUrl, endpoint) => {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', baseUrl + endpoint, true);

    let formData = new FormData();
    console.log(config.fileName)
    formData.append('audioData', blob, config.fileName);
    xhr.send(formData);
    return xhr;
}
function base64ToBlob(base64, mime) {
    mime = mime || '';
    var sliceSize = 1024;
    var byteChars = window.atob(base64);
    var byteArrays = [];

    for (var offset = 0, len = byteChars.length; offset < len; offset += sliceSize) {
        var slice = byteChars.slice(offset, offset + sliceSize);

        var byteNumbers = new Array(slice.length);
        for (var i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
        }

        var byteArray = new Uint8Array(byteNumbers);

        byteArrays.push(byteArray);
    }

    return new Blob(byteArrays, { type: mime });
}
function startBotMessage(message, audioSrc) {
    const messageContainer = document.createElement('div');
    messageContainer.className = 'chat-message bot';

    const img = document.createElement('img');
    img.src = config.botImagePath;
    messageContainer.appendChild(img);

    const bubbleContainer = document.createElement('div');
    bubbleContainer.className = 'bubble-container';

    const textContainer = document.createElement('div');
    textContainer.className = 'text-container';

    const span = document.createElement('span');
    span.textContent = message;

    const audio = document.createElement('audio');
    audio.src = audioSrc;
    audio.controls = true;

    // Check if the checkbox is checked
    const autoplayCheckbox = document.getElementById('autoplayCheckbox');
    if (autoplayCheckbox.checked) {
        audio.autoplay = true;
    }

    bubbleContainer.appendChild(audio);
    textContainer.appendChild(bubbleContainer);
    textContainer.appendChild(span);
    messageContainer.appendChild(textContainer);
    return messageContainer;
}

function startUserMessage(message) {
    const messageContainer = document.createElement('div');
    messageContainer.className = 'chat-message user';

    const img = document.createElement('img');
    img.src = config.userImagePath;
    messageContainer.appendChild(img);

    const bubbleContainer = document.createElement('div');
    bubbleContainer.className = 'bubble-container';

    const textContainer = document.createElement('div');
    textContainer.className = 'text-container';

    const span = document.createElement('span');
    span.textContent = message;
    textContainer.appendChild(span);

    bubbleContainer.appendChild(textContainer);
    messageContainer.appendChild(bubbleContainer);

    return messageContainer;
}



function switchInput(inputType) {
    if (inputType === 'text') {
        document.getElementById('chat-input').style.display = '';
        document.getElementById('switchToText').style.display = 'none';
        document.getElementById('switchToVoice').style.display = '';
        document.getElementById('record').style.display = 'none';
    } else if (inputType === 'voice') {
        document.getElementById('chat-input').style.display = 'none';
        document.getElementById('switchToText').style.display = '';
        document.getElementById('switchToVoice').style.display = 'none';
        document.getElementById('record').style.display = '';
    }
}


const sendPCMData = (blob, baseUrl, endpoint) => {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', baseUrl + endpoint, true);

    xhr.setRequestHeader('Content-Type', 'audio/wav');
    xhr.send(blob);
    return xhr;
};

const createDiv = (id, className) => {
    var div = document.createElement('div');
    div.className = className;
    return div;
}

const createImage = (src) => {
    var img = document.createElement('img');
    img.src = src;
    return img;
}

const createSpan = (text) => {
    var span = document.createElement('span');
    span.textContent = text;
    return span;
}

const appendChild = (parent, child) => {
    parent.appendChild(child);
    return parent;
}

const startAudioMessage = () => {
    var chatContainer = document.getElementById('chatContainer');
    var messageDiv = createDiv(null, 'chat-message user');
    var userImage = createImage(config.userImagePath);
    var bubbleContainer = createDiv(null, 'bubble-container'); // Create a bubble container
    var audioDiv = createDiv(null, 'audio-message');
    var loadingImg = createImage(config.loadingImagePath);
    appendChild(audioDiv, loadingImg);
    appendChild(bubbleContainer, audioDiv); // Append the audioDiv to the bubble container
    appendChild(messageDiv, bubbleContainer); // Append the bubble container to the messageDiv
    appendChild(messageDiv, userImage);
    appendChild(chatContainer, messageDiv);
    return { messageDiv, audioDiv, loadingImg };
}


const finishAudioMessage = (messageDiv, audioLength) => {
    var audioDiv = messageDiv.querySelector('.audio-message');
    audioDiv.innerText = 'Audio Message (' + audioLength + '")';
    return audioDiv;
}


const generateStory = () => {
    // Implement your story generation logic here
}

const changeTopic = () => {
    document.getElementById('chatContainer').innerHTML = '';
}

window.changeTopic = changeTopic;
window.generateStory = generateStory;
window.changeTopic = changeTopic;
window.generateStory = generateStory;

document.addEventListener('DOMContentLoaded', function () {
    var recordButton = document.getElementById("record");
    recordButton.disabled = true; // Disable the button initially
    /*------------Recorder----------------------------*/
    var recorder = null;
    var audio = document.querySelector('audio');

    Recorder.get(function (rec) {
        console.log("Recorder is ready")
        recorder = rec;
        recordButton.disabled = false;
    });

    var recordingStartTime;

    function startRecording() {
        if (recorder) {
            console.log("开始录音")
            recorder.clear(); // clear the previous recorded audio
            //recorder.start();
            recorder.startDelayed();
            recordingStartTime = Date.now(); // set the recording start time
        }
    }

    function stopRecording() {
        if (recorder) {
            recorder.stop();
            recorder.startDelayed();
            var recordingEndTime = Date.now();
            var durationInSeconds = (recordingEndTime - recordingStartTime) / 1000;
            console.log("结束录音")
            console.log("录音时长：" + durationInSeconds + "秒");
            return durationInSeconds;
        } else {
            console.error('recorder is not defined');
        }
    }


    function uploadAudio() {
        if (recorder) {
            const formData = new FormData();
            formData.append("audioData", recorder.getBlob());
            formData.append("cuid", cuid)
            fetch(config.baseUrl + config.uploadAudioEndpoint, {
                method: 'POST',
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    console.log("Upload successful. Response:", data);
                    // Convert base64 audio data to a blob
                    var audioBlob = base64ToBlob(data.audio, 'audio/wav');
                    var message = data.text;
                    // Create a URL for the audio blob
                    var audioUrl = URL.createObjectURL(audioBlob);
                    // Create a new bot message with the AI response text and audio
                    var messageContainer = startBotMessage(message, audioUrl);

                    let chatContainer = document.getElementById("chatContainer");
                    chatContainer.appendChild(messageContainer);

                })
                .catch(error => console.error(error));
        } else {
            console.error('recorder object is not defined');
        }
    }

    recordButton.addEventListener('mousedown', function () {
        // start recording
        var { messageDiv, audioDiv, loadingImg } = startAudioMessage();
        recordButton.messageDiv = messageDiv;
        recordButton.audioDiv = audioDiv;
        recordButton.loadingImg = loadingImg;
        startRecording();  // this function comes from your recording logic
    });
    document.getElementById('textForm').addEventListener('submit', function(e) {
        e.preventDefault();
    });
    recordButton.addEventListener('mouseup', function () {
        // stop recording and get the duration
        var duration = stopRecording();
        console.log("duration: " + duration)
        // Only proceed to replace the loading image if a duration was returned
        if (duration !== undefined) {
            console.log("结束录音")
            // create a duration span
            var durationSpan = createSpan(duration + ' seconds');
            // replace loading image with duration span
            var audioDiv = this.audioDiv;
            var loadingImg = this.loadingImg;
            // Timeout is used to delay the execution to allow time for other processes to finish.
            // It's not the best solution, but it might be necessary in some cases.
            setTimeout(function () {
                audioDiv.replaceChild(durationSpan, loadingImg);
            }, 100);
        }
        uploadAudio();
    });
    var storyButton = document.getElementById('story')
    storyButton.addEventListener('click', function () {
        // Clear the chat
        changeTopic()
        console.log("开始生成故事")
        console.log(cuid)
        // Make a POST request to the '/story' route
        fetch(config.baseUrl + config.storyEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ cuid: cuid })
        }
        )
            .then(response => response.json())
            .then(data => {
                console.log("Upload successful. Response:", data);
                // Convert base64 audio data to a blob
                var audioBlob = base64ToBlob(data.audio, 'audio/wav');
                var message = data.text;
                // Create a URL for the audio blob
                var audioUrl = URL.createObjectURL(audioBlob);
                // Create a new bot message with the AI response text and audio
                var messageContainer = startBotMessage(message, audioUrl);

                let chatContainer = document.getElementById("chatContainer");
                chatContainer.appendChild(messageContainer);

            })
            .catch(error => console.error(error));
    });
    function submitForm() {
        console.log("submitted")
        var text = document.getElementById('chat-input').value;  // This gets the text from the textarea
        document.getElementById('chat-input').value = '';  // This clears the textarea
        var messageContainer = startUserMessage(text);

        let chatContainer = document.getElementById("chatContainer");
        chatContainer.appendChild(messageContainer);
        fetch(config.baseUrl + config.uploadTextEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: text,
                cuid: cuid
            })  // This sends the text as a JSON object
        })
            .then(response => response.json())
            .then(data => {
                console.log("Upload successful. Response:", data);
                // Convert base64 audio data to a blob
                var audioBlob = base64ToBlob(data.audio, 'audio/wav');
                var message = data.text;
                // Create a URL for the audio blob
                var audioUrl = URL.createObjectURL(audioBlob);
                // Create a new bot message with the AI response text and audio
                var messageContainer = startBotMessage(message, audioUrl);

                let chatContainer = document.getElementById("chatContainer");
                chatContainer.appendChild(messageContainer);

            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }


    document.getElementById('chat-input').addEventListener('keydown', function (event) {
        if (event.key == 'Enter') {
            event.preventDefault(); // Prevents the default action
            console.log("Enter")
            submitForm(); // Call the form submission function
        }
    });


});
