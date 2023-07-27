import requests
import json
import os
from initialize import initialize_api_key, get_access_token
from audiotextprocess import speech_recognition

def single_response(content: str, messages: list = []):
    api_key, secret_key = initialize_api_key()
    access_token = get_access_token(api_key, secret_key)
    ##url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + access_token
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + access_token
    messages.append({"role":"user", "content":content})
    payload = json.dumps({
        "messages": messages
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    parsed_response = response.json()

    # get the value of the "result" field
    result = parsed_response["result"]
    messages.append({"role":"assistant", "content":result})
    return result

from typing import Union

def handle_user_text_input(text: str):
    # Process text input here
    pass

def handle_user_audio_input(audio: bytes):
    ## audio to text
    text = speech_recognition(audio)

def handle_user_input(input_data: Union[str, bytes], input_type: str):
    if input_type == 'text':
        assert isinstance(input_data, str), "Expected input_data to be a string for text input"
        return handle_user_text_input(input_data)
    elif input_type == 'audio':
        assert isinstance(input_data, bytes), "Expected input_data to be bytes for audio input"
        return handle_user_audio_input(input_data)
    else:
        raise ValueError("Invalid input type. Expected 'text' or 'audio'.")


if __name__ == '__main__':
    initialize_api_key()
    messages = []
    while (True):
        content = input(">>> ")
        result = single_response(content, messages)
        print(result)