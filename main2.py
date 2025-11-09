from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

ispy_api_ip   =     os.getenv('ISPY_IP'  )
ispy_api_port = int(os.getenv('ISPY_API_PORT', 8090))
 
url = f"http://{ispy_api_ip}:{ispy_api_port}"


def get_profile(name:str)->int:
    a = requests.get(url+"/command/getProfiles")
    if a.ok:
       json_data = json.loads(a.text)["profiles"]
       profile_id = [p["id"] for p in json_data if p["name"]==name][0]
       return profile_id
    

def activate_profile(profile_id:int):
    a = requests.get(url+f"/command/armProfile?ind={profile_id}")
    if a.ok:
        print(a.text)
       


activate_profile(get_profile("Dag"))


