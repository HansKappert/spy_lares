import aiohttp
from dotenv import load_dotenv
import os
import logging
import asyncio
import agent

load_dotenv()

ispy_api_ip   =     os.getenv('ISPY_IP'  )
ispy_api_port = int(os.getenv('ISPY_API_PORT', 8090))

async def main():
    url = f"http://{ispy_api_ip}:{ispy_api_port}"
    ispy = agent.Agent(url)

    devices = await ispy.get_devices()
    # devices = await ispy.get_profiles()
    for device in devices:
        print(f"id={device.id}, name={device.name}")
    ispy.arm()
    pass

asyncio.run(main())