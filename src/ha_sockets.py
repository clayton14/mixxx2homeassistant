import asyncio
import websockets
import json
import os, sys, dotenv

dotenv.load_dotenv()

base_url = os.getenv("SERVER_ENDPOINT")
token = os.getenv("TOKEN")
#print(f"URL -> {base_url}\nTOKEN -> {token}")

async def auth():
    try:
        async with websockets.connect(base_url) as ws:
            message = await ws.recv()
            print(message)
            auth_status = await ws.send(json.dumps({
                "type" : "auth",
                "access_token": token
            }))
            print(auth_status)
            message = await ws.recv()

    except ConnectionError as e:
        print("ERROR")
        print(e) # this is dumb    

    print(message)


asyncio.run(auth())