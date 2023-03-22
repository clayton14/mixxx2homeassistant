import requests
import dotenv
import os
from requests import get, post
import random
import json
import time
dotenv.load_dotenv()

base_url = "http://192.168.0.5:8123/api"
token = os.getenv("TOKEN")

print(token)

headers = {
    "Authorization": f"Bearer {token}",
    "content-type": "application/json",
}

print(base_url)

def update_status(data):
    data = json.dumps(data, indent=4)
    response = post(f"{base_url}/services/light/turn_on",
                    headers=headers, data=data)
    return response

def get_services():
    pass


while 1:
    color = random.randint(1, 360)
    data = {
    "hs_color": [color, 100],
    "entity_id": "light.ohad_light"
    }
    # time.sleep(0.1)
    print(update_status(data))
    print(color)
