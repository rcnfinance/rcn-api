from preserver import Preserver
import requests

class APIPreserver(Preserver):
    def __init__(self):
        self._url = "http://10.0.4.120:8000/v1/loans/"
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