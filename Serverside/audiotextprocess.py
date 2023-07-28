import requests
import base64
import json
import config
import os
from pydub import AudioSegment
from io import BytesIO

def speech_recognition(audio_data: bytes, token: str, cuid: str, dev_pid: int, format: str, rate: int ) -> str:
    
    headers = {
        'Content-Type': f'audio/{format};rate={rate}'
    }
    url = f"https://vop.baidu.com/server_api?dev_pid={dev_pid}&cuid={cuid}&token={token}"

    response = requests.post(url, headers=headers, data=audio_data)
    result = response.json()
    return result
    if result['err_no'] == 0:
        return result["result"]
    else:
        raise Exception('Error in speech recognition: {}'.format(result["err_msg"]))

def audio_data_to_text(audio_data: bytes, dev_pid: int = 1537, format: str = "pcm", rate: int = 16000) -> str:
    access_token = config.retrieve_access_token()
    cuid = config.generate_cuid()
    text =  speech_recognition(audio_data, access_token, cuid, dev_pid, format, rate)
    return text
def convert_webm_bytes_to_wav_bytes(input_bytes:bytes) -> bytes:
    byte_stream = BytesIO(input_bytes)
    audio = AudioSegment.from_file(byte_stream, format="webm")
    # 设置音频的位深（bit depth）为16
    audio = audio.set_sample_width(2).set_frame_rate(8000)
    output_io = BytesIO()
    audio.export(output_io, format="wav")
    return output_io.getvalue()

## for testing
def read_local_audio_file(file_path: str) -> bytes:
    with open(file_path, 'rb') as f:
        audio_data = f.read()
    return audio_data

def test_speech_recognition():
    file_name = "16k.wav"
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_directory, file_name)
    audio_data = read_local_audio_file(file_path)
    dev_pid = 1537  # the recognition language model
    format = 'wav'
    rate = 16000  # sample rate
    text = audio_data_to_text(audio_data, dev_pid, format, rate)
    print(text)

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.realpath(__file__))
    f = open(os.path.join(current_directory,"audio.webm"), "rb")
    audio_data = f.read()
    new_audio_data = convert_webm_bytes_to_wav_bytes(audio_data)
    new_f = open((os.path.join(current_directory,"audio.wav")), "wb")
    new_f.write(new_audio_data)
    new_f.close()
    f.close()
    