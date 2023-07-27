let audioType = 'wave';
let sampleRate = 16000;


var config = {
    userImagePath: 'path-to-user-image',
    loadingImagePath: 'path-to-loading-image',
    audioEndpoint: '/upload',
    audioBaseUrl: 'http://localhost:8080',
    audioFormat : 'pcm',
    audioRecorderOptions : {
        audioType: "audio/" + audioType,
        sampleRate: sampleRate
    },
};