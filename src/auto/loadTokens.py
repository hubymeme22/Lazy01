from ..libraries.Strings import ConsoleStr
from dotenv import load_dotenv

import requests as re
import json
import os

load_dotenv()
TOKEN_RETRIEVAL_CONFIG = os.getenv('TOKEN_RETRIEVAL_CONFIG')

def loadTokens():
    if (TOKEN_RETRIEVAL_CONFIG == None or TOKEN_RETRIEVAL_CONFIG == ''):
        ConsoleStr.red('[-] Cannot find find the configuration path for token retrieval')
        exit()

    if (not os.path.isfile(TOKEN_RETRIEVAL_CONFIG)):
        ConsoleStr.red(f'[-] File for token retrieval ({TOKEN_RETRIEVAL_CONFIG}) not found')
        exit()

    configFp = open(TOKEN_RETRIEVAL_CONFIG, 'r')
    loadedConfig: list[dict] = json.load(configFp)
    ConsoleStr.green(f'[+] Loaded json configuration from {TOKEN_RETRIEVAL_CONFIG}')

    for proceure in loadedConfig:
        name = proceure.get('name')
        host = proceure.get('host')
        endp = proceure.get('endpoint')

        print(f'[*] Retrieving token for {ConsoleStr.v(name)}')
        if (proceure.get('type') == 'json'):
            response = re.post(f'{host}{endp}', json=proceure.get('data'))
            if (200 <= response.status_code <= 299):
                jsonResponse = response.json()
                ConsoleStr.green(f'[+] Token: {ConsoleStr.y(jsonResponse[proceure.get("response-key")])}')
            else: ConsoleStr.yellow(f'[!] Server error response: {response.status_code}')
            continue
        else:
            response = re.post(f'{host}{endp}', data=proceure.get('data'))
            if (200 <= response.status_code <= 299):
                ConsoleStr.green(f'[+] Response Body: {response.raw}')
            else: ConsoleStr.yellow(f'[!] Server error response: {response.status_code}')
            continue
