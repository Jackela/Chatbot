let sampleRate = 16000;
let sampleBits = 16;
var config = {
    userImagePath: './assets/user.png',
    loadingImagePath: './assets/loading.gif',
    botImagePath: './assets/bot.png',
    playImagePAth: './assets/play.png',
    uploadAudioEndpoint: '/uploadAudio',
    uploadTextEndpoint:'/uploadText',
    baseUrl: 'http://localhost:8080',
    storyEndpoint: '/story',
    audioRecorderOptions : {
        mimeType: "audio/webm;codecs=opus",
        audioBitsPerSecond: sampleRate
    },
    startDelay: 500, // Delay in milliseconds (0.5 seconds)
    stopDelay: 500, // Delay in milliseconds (0.5 seconds)
};
