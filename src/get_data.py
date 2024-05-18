import requests

from utils.assets import BASE_URL


class GetData:
    def __init__(self, url, api_key, team_id=None, team_name=None):
        self.url = url
        self.api_key = api_key
        self.team_id = team_id
        self.headers = {"Authorization": f"GenieKey {self.api_key}"}

    def get_data(self):
        response = requests.get(self.url, headers=self.headers, timeout=10)
        return response.json()

    def get_teams(self):
        response = requests.get(self.url, headers=self.headers, timeout=10)
        response_data = response.json()
        if isinstance(response_data, list):
            return response_data
        elif isinstance(response_data, dict) and "data" in response_data:
            return response_data["data"]
        else:
            raise ValueError("Unexpected response structure")

    def get_team_id(self, team_name):
        response = requests.get(self.url, headers=self.headers, timeout=10)
        response_json = response.json()
        if isinstance(response_json, dict) and "data" in response_json:
            for team in response_json["data"]:
                if team["name"] == team_name:
                    return team["id"]
        else:
            raise ValueError("Unexpected response structure")

    def get_team_data(self, team_id):
        response = requests.get(
            f"{self.url}/{team_id}", headers=self.headers, timeout=10
        )
        return response.json()

    def get_custom_roles(self):
        response = requests.get(
            f"{self.url}/teams/{self.team_id}/roles", headers=self.headers, timeout=10
        )
        return response.json()

    def get_default_routing_rule_id(self, team_id):
        response = requests.get(
            f"{self.url}/teams/{team_id}/routing-rules",
            headers=self.headers,
            timeout=10,
        )
        response_json = response.json()
        if isinstance(response_json, dict) and "data" in response_json:
            for routing_rule in response_json["data"]:
                if routing_rule["name"] == "Default Routing Rule":
                    return routing_rule["id"]
        else:
            raise ValueError("Unexpected response structure")

    def get_team_shedules_id(self, ownerTeam):
        response = requests.get(self.url, headers=self.headers, timeout=10)
        response_json = response.json()
        if isinstance(response_json, dict) and "data" in response_json:
            for schedule in response_json["data"]:
                owner_team = schedule.get("ownerTeam")
                if owner_team and owner_team.get("name") == ownerTeam:
                    return schedule["id"]
        else:
            raise ValueError("Unexpected response structure")

    def get_schedule(self, schedule_id):
        response = requests.get(
            f"{self.url}/{schedule_id}", headers=self.headers, timeout=10
        )
        return response.json()

    def get_escalation_id(self, team_name):
        response = requests.get(self.url, headers=self.headers, timeout=10)
        response_json = response.json()
        if isinstance(response_json, dict) and "data" in response_json:
            for escalation in response_json["data"]:
                if escalation["name"] == f"{team_name}_escalation":
                    return escalation["id"]
        else:
            raise ValueError("Unexpected response structure")

    def get_escalations(self):
        response = requests.get(self.url, headers=self.headers, timeout=10)
        response_json = response.json()
        if isinstance(response_json, dict) and "data" in response_json:
            return response_json["data"]
        else:
            raise ValueError("Unexpected response structure")

    def get_routing_rules(self):
        response = requests.get(self.url, headers=self.headers, timeout=10)
        response_json = response.json()
        if isinstance(response_json, dict) and "data" in response_json:
            return response_json["data"]
        else:
            raise ValueError("Unexpected response structure")

    def get_users(self):
        response = requests.get(self.url, headers=self.headers, timeout=10)
        response_json = response.json()
        if isinstance(response_json, dict) and "data" in response_json:
            return response_json["data"]
        else:
            raise ValueError("Unexpected response structure")

    def get_team_admins(self, team_data):
        if "data" in team_data and "members" in team_data["data"]:
            return [
                user
                for user in team_data["data"]["members"]
                if user["role"] == "Team Admin"
                or user["role"] == "admin"
                or user["role"] == "user"
            ]
        else:
            raise KeyError("'members' not found in team_data")

    def get_team_integrations_id(self, team_id_old):
        team_integration_ids = []
        url = f"{BASE_URL}/integrations"
        response = requests.get(url, headers=self.headers, timeout=10)
        json_data = response.json()
        data = json_data.get("data", {})
        for each in data:
            if each.get("enabled") is True and each.get("teamId") == team_id_old:
                team_integration_ids.append(each.get("id"))
        return team_integration_ids

    def get_team_integrations(self, team_integration_ids):
        slack_integrations = []
        team_integrations = []
        for id in team_integration_ids:
            url = f"{BASE_URL}/integrations/{id}"
            response = requests.get(url, headers=self.headers, timeout=10)
            json_data = response.json()
            data = json_data.get("data", {})
            if data.get("type") != "SlackApp":
                data["ownerTeam"].pop("id", None)
                data["assignedTeam"].pop("id", None)
                team_integrations.append(data)

            elif data.get("type") == "SlackApp":
                data["ownerTeam"].pop("id", None)
                data["assignedTeam"].pop("id", None)
                slack_integrations.append(data)
        return team_integrations, slack_integrations
