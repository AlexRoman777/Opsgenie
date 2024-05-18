import requests


class DeleteTeam:
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key
        self.headers = {"Authorization": f"GenieKey {self.api_key}"}

    def del_team(self):
        response = requests.delete(self.url, headers=self.headers, timeout=10)
        return response.json()
