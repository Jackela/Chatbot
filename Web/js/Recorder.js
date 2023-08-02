(function (window) {

    function Recorder(stream, config = {}) {
        console.log("Recorder is running")
        try {
            const sampleBits = config.sampleBits || 16;
            const sampleRate = config.sampleRate || 16000;

            const context = new AudioContext();
            const audioInput = context.createMediaStreamSource(stream);
            const recorder = context.createScriptProcessor(4096, 1, 1);

            let audioData = {
                size: 0,
                buffer: [],
                inputSampleRate: context.sampleRate,
                inputSampleBits: 16,
                outputSampleRate: sampleRate,
                outputSampleBits: sampleBits,
            };

            const inputData = (data) => {
                audioData = {
                    ...audioData,
                    buffer: [...audioData.buffer, new Float32Array(data)],
                    size: audioData.size + data.length
                }
            };

            const compressData = () => {
                const data = audioData.buffer.reduce((data, buf, i) => {
                    data.set(buf, i * buf.length);
                    return data;
                }, new Float32Array(audioData.size));

                const compression = Math.floor(audioData.inputSampleRate / audioData.outputSampleRate);
                const length = data.length / compression;

                const result = Array.from({ length }, (_, i) => data[i * compression]);

                return new Float32Array(result);
            };

            const writeString = (data, offset, string) => {
                Array.from(string).forEach((char, i) => {
                    data.setUint8(offset + i, char.charCodeAt(0));
                });
            };

            const encodeWav = () => {
                const sampleRate = Math.min(audioData.inputSampleRate, audioData.outputSampleRate);
                const sampleBits = Math.min(audioData.inputSampleBits, audioData.outputSampleBits);
                const bytes = compressData();
                const dataLength = bytes.length * (sampleBits / 8);
                const buffer = new ArrayBuffer(44 + dataLength);
                const data = new DataView(buffer);

                let offset = 0;
                writeString(data, offset, 'RIFF');
                offset += 4;

                data.setUint32(offset, 36 + dataLength, true);
                offset += 4;

                writeString(data, offset, 'WAVE');
                offset += 4;

                writeString(data, offset, 'fmt ');
                offset += 4;

                data.setUint32(offset, 16, true);
                offset += 4;

                data.setUint16(offset, 1, true);
                offset += 2;

                const channelCount = 1;
                data.setUint16(offset, channelCount, true);
                offset += 2;

                data.setUint32(offset, sampleRate, true);
                offset += 4;

                data.setUint32(offset, channelCount * sampleRate * (sampleBits / 8), true);
                offset += 4;

                data.setUint16(offset, channelCount * (sampleBits / 8), true);
                offset += 2;

                data.setUint16(offset, sampleBits, true);
                offset += 2;

                writeString(data, offset, 'data');
                offset += 4;

                data.setUint32(offset, dataLength, true);
                offset += 4;

                bytes.forEach((sample, i) => {
                    const s = Math.max(-1, Math.min(1, sample));
                    if (sampleBits === 8) {
                        const val = s < 0 ? s * 0x8000 : s * 0x7FFF;
                        data.setInt8(offset + i, parseInt(255 / (65535 / (val + 32768))), true);
                    } else {
                        data.setInt16(offset + i * 2, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
                    }
                });

                return new Blob([data], { type: 'audio/wav' });
            };

            const start = () => {
                audioInput.connect(recorder);
                recorder.connect(context.destination);
            }

            const stop = () => {
                recorder.disconnect();
            }
            // Start and stop delay timers
            let startTimeoutId, stopTimeoutId;
            const startDelay = config.startDelay || 1000;  // Default 1 second delay
            const stopDelay = config.stopDelay || 1000;  // Default 1 second delay
            //不好看，但是可以用
            //需要同时修改script.js（调用方式）
            // Start recording with a delay
            function startDelayed()  {
                // Clear any previous timeout
                clearTimeout(startTimeoutId);

                startTimeoutId = setTimeout(() => {
                    start();
                }, startDelay);
            };

            // Stop recording with a delay
            function stopDelayed() {
                // Clear any previous timeout
                clearTimeout(stopTimeoutId);

                stopTimeoutId = setTimeout(() => {
                    stop();
                }, stopDelay);
            };
            const getBlob = () => {
                stop();
                return encodeWav();
            }

            const play = (audio) => {
                audio.src = window.URL.createObjectURL(getBlob());
            }

            const upload = (url, callback) => {
                const fd = new FormData();
                fd.append("audioData", getBlob());
                const xhr = new XMLHttpRequest();

                if (callback) {
                    ['progress', 'load', 'error', 'abort'].forEach(event => {
                        xhr.upload.addEventListener(event, e => callback(event, e), false);
                    });
                }

                xhr.open("POST", url);
                xhr.send(fd);
            }

            const clear = () => {
                audioData.buffer = [];
                audioData.size = 0;
            }

            recorder.onaudioprocess = (e) => {
                inputData(e.inputBuffer.getChannelData(0));
            }

            return {
                start,
                stop,
                startDelayed,
                stopDelayed,
                getBlob,
                play,
                upload,
                clear,
            };
        }
        catch (e) {
            console.log("An exception was thrown in the Recorder function:", e);
            throw e;  // Re-throw the exception so the caller knows something went wrong
        }

    };

    //抛出异常
    Recorder.throwError = function (message) {
        alert(message);
        throw new function () { this.toString = function () { return message; } }
    }

    // Static method to check if the browser supports recording.
    Recorder.canRecord = !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);


    // 错误处理
    const handleError = (error) => {
        const errorMapping = {
            NotAllowedError: '用户拒绝提供信息。',
            PermissionDeniedError: '用户拒绝提供信息。',
            NotReadableError: '无法访问麦克风。',
            TrackStartError: '无法访问麦克风。',
            NotFoundError: '无法找到麦克风设备。',
            DevicesNotFoundError: '无法找到麦克风设备。',
            OverconstrainedError: '硬件设备无法满足所需的约束。',
            ConstraintNotSatisfiedError: '硬件设备无法满足所需的约束.'
        };

        const message = errorMapping[error.name] || '无法打开麦克风。异常信息:';
        return Promise.reject(message + error.name);
    };

    // 获取录音机
    const getRecorder = (callback, config) => {
        if (callback) {
            navigator.mediaDevices.getUserMedia(
                { audio: true } // 只启用音频
            ).then(function (stream) {
                console.log("getRecorder then called")
                rec = Recorder(stream, config);
                console.log("rec created")
                callback(rec);
            }).catch(handleError);
        }
        else {
            console.log("getRecorder was called with a null or undefined callback");
        }
    }

    Recorder.get = getRecorder;

    window.Recorder = Recorder;
    console.log("Recorder.js loaded")

})(window);
