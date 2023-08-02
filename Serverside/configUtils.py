"""
获取各种配置信息（例如：读取文件） 或者生成一些随机的字符串
"""
import os
import json
import uuid
from typing import Dict

def retrieve_access_token(file_name: str = "access_token.json") -> str:
    """
    Retrieve the token data from a JSON file in the same directory as this script
    """
    # Get the directory of this script
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Join the directory path and filename to get the full file path
    file_path = os.path.join(dir_path, file_name)

    # Make sure the file exists before trying to open it
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"No file found at {file_path}")

    # Read the token data from the file
    with open(file_path, "r") as token_file:
        token_data = json.load(token_file)
    
    access_token = token_data.get("access_token")
    return access_token


def generate_cuid() -> str:
    return str(uuid.uuid4())[:60]

if __name__ == "__main__":
    print(retrieve_access_token())