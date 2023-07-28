const sendAudioData = (blob, baseUrl, endpoint) => {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', baseUrl + endpoint, true);

    let formData = new FormData();
    
    formData.append('audioData', blob, config.fileName);
    xhr.send(formData);
    return xhr;
}


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

const appendChild = (parent, child) => {
    parent.appendChild(child);
    return parent;
}

const startAudioMessage = () => {
    var chatContainer = document.getElementById('chatContainer');
    var messageDiv = createDiv(null, 'chat-message user');
    var userImage = createImage(config.userImagePath);
    var audioDiv = createDiv(null, 'audio-message');
    var loadingImg = createImage(config.loadingImagePath);
    appendChild(audioDiv, loadingImg);
    appendChild(messageDiv, audioDiv);
    appendChild(messageDiv, userImage);
    appendChild(chatContainer, messageDiv);
    return messageDiv;
}

const finishAudioMessage = (messageDiv, audioLength) => {
    var audioDiv = messageDiv.querySelector('.audio-message');
    audioDiv.innerText = 'Audio Message (' + audioLength + '")';
    return audioDiv;
}

const fetchArrayBuffer = (audioUrl) =>
    fetch(audioUrl)
        .then(response => response.arrayBuffer())
        .catch(error => console.log(error));

const decodeAudioData = (arrayBuffer) =>
    audioContext.decodeAudioData(arrayBuffer, audioBuffer => audioBuffer.getChannelData(0));

const convertWebMToPCM = (audioUrl, callback) =>
    fetchArrayBuffer(audioUrl).then(decodeAudioData).then(callback);

const createPCMBlob = (pcmBuffer) => {
    var pcmData = new Float32Array(pcmBuffer);
    var pcmArrayBuffer = pcmData.buffer;
    return new Blob([pcmArrayBuffer], { type: 'audio/pcm' });
}

const changeTopic = () => {
    document.getElementById('chatContainer').innerHTML = '';
}
window.changeTopic = changeTopic;
window.generateStory = generateStory;
const generateStory = () => {
    // Implement your story generation logic here
}

document.addEventListener('DOMContentLoaded', function () {
    var recorder = null;
    var recordButton = '#sendButton';
    var stream = null;
    var recordingStartTime;
    var messageDiv;
    var audioChunks = [];

    var constraints = { 
        audio: {
            channelCount: config.audioRecorderOptions.channelCount,
            sampleRate: config.audioRecorderOptions.sampleRate,
            sampleSize: config.audioRecorderOptions.sampleSize
        }
    };

    const handleDataAvailable = (e) => audioChunks.push(e.data);
    const handleError = (error) => console.log(error, 'Microphone access denied');
    const handleSuccess = (mediaStream) => {
        console.log('Microphone access granted');
        stream = mediaStream;
        recorder = new MediaRecorder(stream);
        recorder.ondataavailable = handleDataAvailable;
    }

    navigator.mediaDevices.getUserMedia(constraints).then(handleSuccess).catch(handleError);

    const startRecording = (event) => {
        event.preventDefault();
        if (recorder) {
            recordingStartTime = Date.now();  // Save the recording start time
            messageDiv = startAudioMessage();
            recorder.start();
        } else {
            console.log('Error: Microphone access was not granted');
        }
    };

    const stopRecording = (event) => {
        event.preventDefault();
        if (recorder) {
            recorder.stop();
            recorder.onstop = e => {
                var blob = new Blob(audioChunks);
                var xhr = sendAudioData(blob, config.audioBaseUrl, 
                    config.audioEndpoint, config.audioRecorderOptions.audioBitsPerSecond);
                xhr.onload = function () {
                    if (xhr.status >= 200 && xhr.status < 300) {
                        console.log('Audio data successfully sent to the server.');
                        var recordingEndTime = Date.now();  // Get the recording end time
                        var recordingDuration = (recordingEndTime - recordingStartTime) / 1000;  // Calculate recording duration in seconds
                        finishAudioMessage(messageDiv, recordingDuration.toFixed(2));
                        document.querySelector(recordButton).disabled = false; // Enable button when bot is finished processing
                    }
                };
                audioChunks = [];
                recorder = null;
            };
        }
    };



    window.startRecording = startRecording;
    window.stopRecording = stopRecording;

});
