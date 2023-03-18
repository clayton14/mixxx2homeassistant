import asyncio
import websockets
import json
import os
import sys
import dotenv
from termcolor import cprint
import random
import time
dotenv.load_dotenv()

base_url = os.getenv("SERVER_ENDPOINT")
token = os.getenv("TOKEN")
# print(f"URL -> {base_url}\nTOKEN -> {token}")
# token = "l"


async def start():
    try:
        async with websockets.connect(base_url) as ws:
            data = {
                "id": 0,
                "type": "call_service",
                "domain": "light",
                "service": "turn_on",
                "service_data": {
                    "hs_color": [300, 100],
                    "brightness": 250
                },
                "target": {
                    "area_id": "den"
                }
            }

            await auth(ws)
            while 1:
                #time.sleep(0)
                data["id"] += 1
                data["service_data"]["hs_color"][0] = random.randint(0, 360)
                print(data["service_data"]["hs_color"][0])
                await send_command(ws, data)

    except (TimeoutError, OSError):
        cprint(
            "[CONNECTION ERROR] Make sure you are connected to the correct network", "yellow")
        return None

async def auth(ws):
    """
        completes the server client auth handshake
        returns: websocket session
    """
    message = await ws.recv()
    message = await ws.send(json.dumps({
        "type": "auth",
        "access_token": token
    }))
    auth_status = await ws.recv()
    auth_status = json.loads(auth_status)
    if auth_status["type"] == "auth_invalid":
        cprint(
            "[ERROR] Invalid auth token! Please generate an auth token in Home Assistant", "red")
    if auth_status["type"] == "auth_ok":
        cprint("=> Auth succuss", "green")


async def send_command(ws, data):
    command = await ws.send(json.dumps(data))
    #print(command)
    stat = await ws.recv()
    #print(stat)

asyncio.run(start())


