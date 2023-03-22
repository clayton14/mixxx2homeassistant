import asyncio
import websockets
import os, sys, json, dotenv, platform
from termcolor import cprint
import random, time
import mido, rtmidi


# Used to interface with Home Assistant using the websockets API

dotenv.load_dotenv()

base_url = os.getenv("SERVER_ENDPOINT")
token = os.getenv("TOKEN")

PLATFORM = platform.system()

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
                    "entity_id": "light.rave"
                }
            }

            await auth(ws)
            while 1:
               with mido.open_input() as inport:
                    for msg in inport:
                        if msg.note == 50 and msg.type == 'note_on':
                            print('beat')
                            data["id"] += 1
                            time.sleep(0.1)
                            data["service_data"]["hs_color"][0] = random.randint(0, 360)
                            print(data["service_data"]["hs_color"][0])
                            await send_command(ws, data)

    except (TimeoutError, OSError) as error:
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



def midi_to_command(port:str):
    """
    converts midi values to ha command 
    """
    # with mido.open_input(port, True) as inport:
    #     for msg in inport:
    #         if msg.note == 50 and msg.type == 'note_on':
    #             print('beat')
    #         if msg.note == 52 and msg.type == 'note_on':
    #             print(msg.velocity + 50)



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

#asyncio.run(start())
# asyncio.run(midi_to_command("portaaaaa"))

midi_to_command("aaaaaaa")