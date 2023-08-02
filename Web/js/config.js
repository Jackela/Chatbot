let sampleRate = 16000;
let sampleBits = 16;
var config = {
    userImagePath: 'path-to-user-image',
    loadingImagePath: 'path-to-loading-image',
    botImagePath: 'path-to-bot-image',
    playImagePAth: 'path-to-play-image',
    audioEndpoint: '/upload',
    audioBaseUrl: 'http://localhost:8080',
    audioRecorderOptions : {
        mimeType: "audio/webm;codecs=opus",
        audioBitsPerSecond: sampleRate
    },
    startDelay: 500, // Delay in milliseconds (0.5 seconds)
    stopDelay: 500, // Delay in milliseconds (0.5 seconds)
};
