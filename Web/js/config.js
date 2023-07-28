let audioType = 'webm';
let sampleRate = 8000;

var config = {
    userImagePath: 'path-to-user-image',
    loadingImagePath: 'path-to-loading-image',
    audioEndpoint: '/upload',
    audioBaseUrl: 'http://localhost:8080',
    audioFormat : 'webm',
    audioRecorderOptions : {
        mimeType: "audio/webm;codecs=opus",
        audioBitsPerSecond: sampleRate
    },
    fileName :"audio." + audioType,
};

//mediaRecorder 不主动报错/崩溃。。。 需要注意当前浏览器是否支持所选的音频格式
if (MediaRecorder.isTypeSupported(config.audioRecorderOptions.mimeType)) {
    console.log(config.audioRecorderOptions.mimeType + " recording is supported")
} else {
    console.log(config.audioRecorderOptions.mimeType + " recording is not supported")
}