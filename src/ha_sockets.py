import asyncio
import websockets
import json
import os
import sys
import dotenv
from termcolor import cprint


dotenv.load_dotenv()

base_url = os.getenv("SERVER_ENDPOINT")
# token = os.getenv("TOKEN")
# print(f"URL -> {base_url}\nTOKEN -> {token}")
token = "l"


async def auth():
    try:
        async with websockets.connect(base_url) as ws:
            message = await ws.recv()
            print(message)
            message = await ws.send(json.dumps({
                "type": "auth",
                "access_token": token
            }))
            auth_status = await ws.recv()
            auth_status = json.loads(auth_status)
            print(auth_status)
            if auth_status["type"] == "auth_invalid":
                cprint(
                    "[ERROR] Invalid auth token! Please genrate an auth toke in Home Assistant", "red")

    except ConnectionError as e:
        print("ERROR")
        print(e)  # this is dumb


asyncio.run(auth())
