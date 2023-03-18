import asyncio
import websockets
import json
import os
import sys
import dotenv
from termcolor import cprint


dotenv.load_dotenv()

base_url = os.getenv("SERVER_ENDPOINT")
token = os.getenv("TOKEN")
# print(f"URL -> {base_url}\nTOKEN -> {token}")
# token = "l"


async def auth():
    """
        completes the server client auth handshake
        returns: websocket session
    """
    try:
        async with websockets.connect(base_url) as ws:
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
    except (TimeoutError, OSError):
        cprint(
            "[CONNECTION ERROR] Make sure you are connected to the correct network", "yellow")
        return None
    
    return ws


data = json.dumps({
    "id": 24,
    "type": "call_service",
    "domain": "light",
    "service": "turn_on",
    "service_data": {
        "color_name": "beige",
        "brightness": "100"
    },
    "target": {
        "entity_id": "sofa.light"
    }
})


async def send_command(session, data):
    comand = await session.send(data)
    print(comand)
    stat = await session.recv()
    print(stat)

ws = asyncio.run(auth())
asyncio.run(send_command(ws, data))
