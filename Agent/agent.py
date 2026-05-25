import os

import requests


def run_command(cmd: str):
    result = os.system(cmd)
    return result
    

def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    print('response->', response)
    print('response->', response.status_code)
    
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    
    return f"something went wrong"

available_tools = {
    "run_command": run_command,
    "get_weather": get_weather
}