import requests

from utils.assets import BASE_URL


class PostData:
    def __init__(self, url, api_key, data=None, team_id=None):
        self.url = url
        self.api_key = api_key
        self.data = data
        self.team_id = team_id
        self.headers = {"Authorization": f"GenieKey {self.api_key}"}

    def post_data(self, data):
        response = requests.post(self.url, headers=self.headers, json=data, timeout=10)
        return response.json()

    def post_custom_roles(self, data, team_id):
        response = requests.post(
            f"{self.url}/teams/{team_id}/roles",
            headers=self.headers,
            json=data,
            timeout=10,
        )
        return response.json()

    def post_user_custom_role(self, data, team_id):
        response = requests.post(
            f"{BASE_URL}/teams/{team_id}/members",
            headers=self.headers,
            json=data,
            timeout=10,
        )
        return response.json()

    def post_team_integrations(self, team_integrations):
        url = "https://api.opsgenie.com/v2/integrations"
        return_data_list = []
        for integration in team_integrations:
            response = requests.post(
                url, headers=self.headers, json=integration, timeout=10
            )
            json_data = response.json()
            print(json_data)
            return_data = json_data.get("data")
            return_data_list.append(return_data)
        return return_data_list
