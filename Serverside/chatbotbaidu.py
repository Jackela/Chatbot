import requests
import json
import os
from initialize import initialize_api_key, get_access_token
from configUtils import retrieve_access_token
from audiotextprocess import audio_data_to_text
from typing import Union


local_dir_path = os.path.dirname(os.path.realpath(__file__))
bot_config_path = os.path.join(local_dir_path, 'bot_config.json')
with open(bot_config_path, 'r') as f:
    bot_config = json.load(f)



def single_response(content: str, messages: list = [], access_token = retrieve_access_token()):
    url = bot_config["url"] + access_token
    messages.append({"role":"user", "content":content})
    payload = json.dumps({
        "messages": messages
    })
    headers = bot_config["headers"]
    
    response = requests.request("POST", url, headers=headers, data=payload)
    parsed_response = response.json()
    # get the value of the "result" field
    result = parsed_response["result"]

    messages.append({"role":"assistant", "content":result})
    return result
## TO BE IMPLEMENTED
def handle_user_text_input(text: str):
    # Process text input here
    pass

def handle_user_audio_input(audio: bytes):
    # audio to text conversion would go here
    text, cuid = audio_data_to_text(audio)
    response = single_response(text)
    return text, response, cuid

def handle_user_input(input_data: Union[str, bytes], input_type: str):

    if input_type == bot_config['text_input']:
        assert isinstance(input_data, str), "Expected input_data to be a string for text input"
        return handle_user_text_input(input_data)
    elif input_type == bot_config['audio_input']:
        assert isinstance(input_data, bytes), "Expected input_data to be bytes for audio input"
        return handle_user_audio_input(input_data)
    else:
        raise ValueError("Invalid input type. Expected 'text' or 'audio'.")


def tell_a_story(messages: list, access_token = retrieve_access_token()):
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "根据下面用户与AI的对话写一个故事：".join(messages)
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    url = bot_config["url"] + access_token

    response = requests.request("POST", url, headers=headers, data=payload)
    parsed_response = response.json()
    # get the value of the "result" field
    result = parsed_response["result"]
    
    return result


if __name__ == '__main__':
    messages = r"{'role':'user', 'content':'我饿了'}), {'role':'assistant', 'content':'吃了'}"
    story = tell_a_story(messages)
    print(story)