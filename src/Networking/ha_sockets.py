import asyncio
import websockets
import os, sys, json, dotenv, platform
from termcolor import cprint
import random, time
import yaml

# Used to interface with Home Assistant using the websockets API

dotenv.load_dotenv()

base_url = os.getenv("SERVER_ENDPOINT")
token = os.getenv("TOKEN")
print(base_url)
PLATFORM = platform.system()
DELAY = 0 # delay in between command send (in seconds)


def load_yml(file: str):
    #TODO loads yaml file to and make json commans
    pass


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
                    #"entity_id": "light.ohad_light"
                    "entity_id": "light.audio",
                    #"entity_id": "light.wiz1",
                    
                }
            }

            await auth(ws)
            while 1: 
                data["id"] += 1
                #time.sleep(0.1)
                data["service_data"]["hs_color"][0] = random.randint(0, 360)
                data["service_data"]["brightness"] = random.randint(150, 250)
                print(data["service_data"]["hs_color"][0], data["service_data"]["brightness"])
                await send_command(ws, data)

    except (TimeoutError, OSError) as error:
        cprint(
            "[CONNECTION ERROR] Make sure you are connected to the correct network", "yellow")
        return None


async def auth(ws):
    """
        completes the server client auth handshake
        args: websocket session
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
        sys.exit(1)
    if auth_status["type"] == "auth_ok":
        cprint("=> Auth succuss", "green")




async def bpm_to_command():
    """
    Convrts bpm to 
    """
    pass


async def set_color():
    """
    pass
    """
    pass


async def off():
    """
    Turns lights off
    """
    pass


async def send_command(ws, data):
    command = await ws.send(json.dumps(data))
    stat = await ws.recv()

asyncio.run(start())

