import aiohttp
from dotenv import load_dotenv
import os
import logging
import agent
import asyncio
from kseniaWebsocketLibrary import ksenia_lares
# from ksenia_lares.websocketmanager import WebSocketManager

load_dotenv()

ip   =     os.getenv('WS_IP'  )
pin  = int(os.getenv('WS_PIN' ))
port = int(os.getenv('WS_PORT'))
ispy_api_port = int(os.getenv('ISPY_API_PORT', 8090))

# WAIT_FROM = os.getenv('WAIT_FROM')
# WAIT_UNTIL = os.getenv('WAIT_UNTIL')

# POLL_INTERVAL_MINUTES = int(os.getenv('POLL_INTERVAL_MINUTES', 5))  

async def main():
    # logger = logging.getLogger('Lares')
    # ws_manager = ksenia_lares.WebSocketManager(ip, pin, port, logger)
    # await ws_manager.connectSecure()
    
    # ws_manager.register_listener('system', lambda data: print("System event:", data))
    # co_routine = ws_manager.listener()
    # await co_routine
    # # co_routine = ws_manager.getSystem()
    # # system_info = await co_routine


    # url = f"http://{ip}:{ispy_api_port}"
    # ispy = agent.Agent(url)

    # # sess = aiohttp.ClientSession()
    # # tc2 = agent.Agent(url,sess)

    # devices = await ispy.get_devices()
    # print(devices)
    pass

asyncio.run(main())