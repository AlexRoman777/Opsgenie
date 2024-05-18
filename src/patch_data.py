import requests


class PatchData:
    def __init__(self, url, api_key, data, team_id, routing_rule_id):
        self.url = url
        self.api_key = api_key
        self.data = data
        self.team_id = team_id
        self.routing_rule_id = routing_rule_id

    def patch_team_routing_rule(self, team_id, data, routing_rule_id):
        data = {"notify": {"type": "none"}}
        headers = {"Authorization": f"GenieKey {self.api_key}"}
        response = requests.patch(
            f"{self.url}/teams/{team_id}/routing-rules/{routing_rule_id}",
            headers=headers,
            json=data,
            timeout=10,
        )
        return response.json()
