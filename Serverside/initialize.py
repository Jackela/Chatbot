import os
import json
import requests
import datetime
from typing import Dict
def initialize_api_key():
    """
    初始化百度API Key，从环境变量中获取
    """
    api_key = os.environ["BAIDU_API_KEY"]
    secret_key = os.environ["BAIDU_SECRET_KEY"]
    return api_key, secret_key

def get_access_token(api_key:str, secret_key:str) -> Dict[str, str]:
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
        
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}".format(api_key=api_key, secret_key=secret_key)
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    access_token = response.json().get("access_token")
    token_data = {
        'access_token': access_token,
        'timestamp': str(datetime.datetime.now())
    }
    return token_data

def save_access_token(token_data: Dict[str, str], file_name: str = "access_token.json"):
    # Get the directory of this script
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Join the directory path and filename to get the full file path
    file_path = os.path.join(dir_path, file_name)

    with open(file_path, "w") as token_file:
        json.dump(token_data, token_file)


if __name__ == "__main__":
    save_access_token(get_access_token(*initialize_api_key()))