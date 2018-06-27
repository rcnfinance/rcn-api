import json
import requests
from preserver import Preserver

class APIPreserver(Preserver):
    def __init__(self, settings_path):
        self._settings_path = settings_path
        self._config = json.load(open(self._settings_path))

        self._url = self._config['URL']
        self._headers = {
            'Content-Type': "application/json"
        }

    def preserve(self, data):
        response = requests.post(self._url, json=data, headers=self._headers)
        print(response.status_code, response.text)
        return response.status_code, response.text

class EchoPreserver(Preserver):
    def preserve(self, data):
        print(data)