## 这是一个定时运行的任务，用于更新access_token
import os
import time
import requests
import json
import os

grant_type = "client_credentials"
client_id = os.getenv("DATA_BAKER_CLIENT_ID")
client_secret = os.getenv("DATA_BAKER_CLIENT_SECRET")
api_key = os.getenv("OPENAPI_API_KEY")
acess_token_url = f"https://openapi.data-baker.com/oauth/2.0/token?grant_type={grant_type}&client_secret={client_secret}&client_id={client_id}"
directory = os.path.dirname(os.path.abspath(__file__))
access_token_path = os.path.join(directory, 'access_token.json')
## access_token过期时间为24小时, 提前timeoutRedundance秒更新
timeoutRedundance = 30
'''
## 更新access_token
def update_access_token():
    response = requests.post(acess_token_url)
    access_token = json.loads(response.text).get('access_token')
    now = time.time()
    expires_at = now + 24 * 60 * 60 - timeoutRedundance
    with open(access_token_path, 'w') as f:
        json.dump({'access_token': access_token, 'expires_at': expires_at}, f)

def initialize_token():
    if not os.path.exists(access_token_path):
        update_access_token()
    with open(access_token_path, 'r+') as f:
        acess_token = json.load(f)
        ##read the toekn and expires_at from the file
        access_token, expires_at = acess_token['access_token'], acess_token['expires_at']

        return access_token, expires_at

access_token, expires_at = initialize_token()

## if token has expired
if expires_at <= time.time():
    accesstoken.getAccessToken()
'''

if __name__ == "__main__":
    print(client_id, client_secret, api_key)