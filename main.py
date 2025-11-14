import aiohttp
from dotenv import load_dotenv
import os
import logging
# import agent
import asyncio
# from kseniaWebsocketLibrary import ksenia_lares
import ksenia_lares
import logging
import requests
import json

load_dotenv()

ksenia_ip   =     os.getenv('KSENIA_IP'  )
ksenia_pin  = int(os.getenv('KSENIA_PIN' ))
ksenia_port = int(os.getenv('KSENIA_PORT'))

ispy_api_ip   =     os.getenv('ISPY_IP'  )
ispy_api_port = int(os.getenv('ISPY_API_PORT', 8090))

agentdvr_url = f"http://{ispy_api_ip}:{ispy_api_port}"

# WAIT_FROM = os.getenv('WAIT_FROM')
# WAIT_UNTIL = os.getenv('WAIT_UNTIL')

# POLL_INTERVAL_MINUTES = int(os.getenv('POLL_INTERVAL_MINUTES', 5))  


def get_profile(name:str)->int:
    a = requests.get(agentdvr_url + "/command/getProfiles")
    if a.ok:
        json_data = json.loads(a.text)["profiles"]
        profile_ids = [p["id"] for p in json_data if p["name"]==name]
        if len(profile_ids) == 1:
           return profile_ids[0]
        else:
            raise f"Unknown profile specified: {name}"

def activate_profile(profile_id:int):
    a = requests.get(agentdvr_url + f"/command/armProfile?ind={profile_id}")
    logger = logging.getLogger('ispy_activator')
    logger.debug(a.text)

async def handle_systems_message(data):
    logger = logging.getLogger('ispy_activator')
    logger.info(data)
    if not data:
        return
    # data = [{'ID': '1', 'ARM': {'D': 'Uitgeschakeld', 'S': 'D'}, 'TIME': {'GMT': '1757656800', 'TZ': '2', 'TZM': '120', 'DAWN': '07:10', 'DUSK': '20:07'}}]
    if "ARM" in data[0].keys():
        modus = data[0]["ARM"]["D"]

        try:
            if modus == "Ingeschakeld":
                logger.info(f"Camera alerts inschakelen")
                activate_profile(get_profile("Nacht"))

            if modus == "Uitgeschakeld":
                logger.info(f"Camera alerts uitschakelen")
                activate_profile(get_profile("Dag"))

        except Exception as e:
            logger.info(f"Fout bij afhandelen van event {modus}: {e}")

async def handle_zone_message(data):
    logging.info("Zone data:", data)
    
async def main():
    logging.basicConfig(filename="logging.txt",
                    filemode='a',
                    format='%(asctime)s,%(msecs)03d %(levelname)s %(name)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

    logger = logging.getLogger('Lares')
    ws_manager = ksenia_lares.WebSocketManager(ksenia_ip, ksenia_pin, ksenia_port, logger)
    await ws_manager.connectSecure()
    logger = logging.getLogger('ispy_activator')
    logger.setLevel(logging.INFO)
    logger.info("connected")
    ws_manager.register_listener('systems', handle_systems_message)
    # ws_manager.register_listener('zones', handle_zone_message)
    co_routine = ws_manager.listener()
    logger.info("listening")
    await co_routine
    pass

# asyncio.run(handle_systems_message(''))
asyncio.run(main())