import aiohttp
from dotenv import load_dotenv
import os
import logging
import asyncio
import agent

load_dotenv()

ip   =     os.getenv('WS_IP'  )
pin  = int(os.getenv('WS_PIN' ))
port = int(os.getenv('WS_PORT'))
ispy_api_port = int(os.getenv('ISPY_API_PORT', 8090))

async def main():
    url = f"http://{ip}:{ispy_api_port}"
    ispy = agent.Agent(url)

    # devices = await ispy.get_devices()
    devices = await ispy.get_profiles()
    print(devices)
    pass

asyncio.run(main())