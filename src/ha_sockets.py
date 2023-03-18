import asyncio
import socket
import json
import os, sys, dotenv

dotenv.load_dotenv()

base_url = os.getenv("SERVER_ENDPOINT")
token = os.getenv("TOKEN")

print(f"URL -> {base_url}\nTOKEN -> {token}")

async def listen():
    pass 