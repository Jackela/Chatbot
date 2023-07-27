import requests
import base64
import json
import config
import os
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
    test_speech_recognition()