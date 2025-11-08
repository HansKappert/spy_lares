import aiohttp
from dotenv import load_dotenv
import os
import logging
import agent
import asyncio
# from kseniaWebsocketLibrary import ksenia_lares
import ksenia_lares
import logging

load_dotenv()

ksenia_ip   =     os.getenv('KSENIA_IP'  )
ksenia_pin  = int(os.getenv('KSENIA_PIN' ))
ksenia_port = int(os.getenv('KSENIA_PORT'))

ispy_api_ip   =     os.getenv('ISPY_IP'  )
ispy_api_port = int(os.getenv('ISPY_API_PORT', 8090))

# WAIT_FROM = os.getenv('WAIT_FROM')
# WAIT_UNTIL = os.getenv('WAIT_UNTIL')

# POLL_INTERVAL_MINUTES = int(os.getenv('POLL_INTERVAL_MINUTES', 5))  


async def handle_systems_message(data):
    logger = logging.getLogger('ispy_activator')
    logger.info(data)
    if not data:
        return
    # data = [{'ID': '1', 'ARM': {'D': 'Uitgeschakeld', 'S': 'D'}, 'TIME': {'GMT': '1757656800', 'TZ': '2', 'TZM': '120', 'DAWN': '07:10', 'DUSK': '20:07'}}]
    if "ARM" in data[0].keys():
        modus = data[0]["ARM"]["D"]

        url = f"http://{ispy_api_ip}:{ispy_api_port}"
        ispy = agent.Agent(url)

        try:
            if modus == "Ingeschakeld":
                logger.info(f"Camera alerts inschakelen")
                ispy.arm()
            if modus == "Uitgeschakeld":
                logger.info(f"Camera alerts uitschakelen")
                ispy.disarm()
        except Exception as e:
            logger.info(f"Fout bij afhandelen van event {modus}: {e}")

async def handle_zone_message(data):
    logging.info("Zone data:", data)
    
async def main():
    logging.basicConfig(filename="logging.txt",
                    filemode='a',
                    format='%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

    logger = logging.getLogger('Lares')
    ws_manager = ksenia_lares.WebSocketManager(ksenia_ip, ksenia_pin, ksenia_port, logger)
    await ws_manager.connectSecure()
    logger = logging.getLogger('ispy_activator')
    logger.setLevel(logging.DEBUG)
    logger.info("connected")
    ws_manager.register_listener('systems', handle_systems_message)
    # ws_manager.register_listener('zones', handle_zone_message)
    co_routine = ws_manager.listener()
    logger.info("listening")
    await co_routine
    pass

# asyncio.run(handle_systems_message(''))
asyncio.run(main())