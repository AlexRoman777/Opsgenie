import requests


class DeleteData:
    def __init__(self, url, api_key, data):
        self.url = url
        self.api_key = api_key
        self.data = data
        self.headers = {"Authorization": f"GenieKey {self.api_key}"}

    def del_default_escalation(self, data):
        response = requests.delete(
            self.url, headers=self.headers, json=data, timeout=10
        )
        return response.json()
