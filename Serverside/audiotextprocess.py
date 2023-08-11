import requests
import base64
import json
import configUtils
import os
from pydub import AudioSegment
from io import BytesIO
from pydub.playback import play
import simpleaudio as sa
import numpy as np

local_dir_path = os.path.dirname(os.path.realpath(__file__))
# Load the configuration file once when the module is imported
audio_config_path = os.path.join(local_dir_path, 'audio_config.json')
access_token_config_path = os.path.join(local_dir_path, 'access_token.json')
with open(audio_config_path, "r") as f:
    audio_config = json.load(f)
    
with open(access_token_config_path, "r") as f:
    token_data = json.load(f)
    access_token = token_data.get("access_token")

def speech_recognition(audio_data: bytes, token: str, cuid: str, dev_pid: int, format: str, rate: int ) -> str:
    headers = {
        'Content-Type': f'audio/{format};rate={rate}'
    }
    url = f"https://vop.baidu.com/server_api?dev_pid={dev_pid}&cuid={cuid}&token={token}"

    response = requests.post(url, headers=headers, data=audio_data)
    result = response.json()
    if result['err_no'] == 0:
        return result["result"][0]
    else:
        raise Exception('Error in speech recognition: {}'.format(result["err_msg"]))


def audio_data_to_text(audio_data: bytes, cuid: str) -> str:
    dev_pid = audio_config['recognization_params']['dev_pid']
    audio_format = audio_config['recognization_params']['format']
    rate = audio_config['recognization_params']['rate']
    text =  speech_recognition(audio_data, access_token, cuid, dev_pid, audio_format, rate)
    return text

def text_synthesis(text, token, cuid):
    # parameters
    params = {
        'tex': text,
        'tok': token,
        'cuid': cuid,
        'ctp': audio_config['synthesis_params']['ctp'],
        'lan': audio_config['synthesis_params']['lang'],
        'spd': audio_config['synthesis_params']['speed'],
        'vol': audio_config['synthesis_params']['options']['vol'],
        'per': audio_config['synthesis_params']['options']['per'],
        'aue': audio_config['synthesis_params']['aue']
    }
    
    # send a post request
    response = requests.post(audio_config['synthesis_params']['url'], params)
    
    # check if synthesis was successful
    if response.headers['Content-Type'].startswith('audio'):
        return response.content
    else:
        return None

def text_to_audio_data(text: str, cuid) -> bytes:
    token = configUtils.retrieve_access_token()
    audio_data = text_synthesis(text, token, cuid)
    return audio_data




## utils
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

def test_text_synthesis(text:str):
    # Assuming audio_bytes is the WAV data
    audio_bytes = text_synthesis(text , configUtils.retrieve_access_token(), configUtils.generate_cuid())
    # Load the data into a BytesIO object
    audio = BytesIO(audio_bytes)

    # Skip the 44 bytes WAV header
    audio.seek(44)

    # Read the data into a numpy array
    data = np.frombuffer(audio.read(), dtype=np.int16)

    # Play the audio
    play_obj = sa.play_buffer(data, 1, 2, 16000)
    play_obj.wait_done()


if __name__ == "__main__":
    test_text_synthesis("测试")