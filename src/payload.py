class Payload:
    def __init__(self, data):
        self.data = data

    def create_team_payload_without_members(self, source_team_data):
        team_data = source_team_data.get("data", {})
        team_name = team_data.get("name")
        team_description = team_data.get("description")
        payload = {"name": team_name, "description": team_description}
        return payload

    def create_team_payload(self, source_team_data):
        team_data = source_team_data.get("data", {})
        team_name = team_data.get("name")
        team_description = team_data.get("description")
        team_members = team_data.get("members", [])
        for member in team_members:
            if "id" in member.get("user", {}):
                del member["user"]["id"]
        payload = {
            "name": team_name,
            "description": team_description,
            "members": team_members,
        }
        return payload

    def create_custom_role_payload(self, source_custom_roles):
        custom_roles = source_custom_roles.get("data", [])
        for custom_role in custom_roles:
            if "id" in custom_role:
                del custom_role["id"]
            if "data" in custom_role:
                del custom_role["data"]
        payload = custom_roles[0] if custom_roles else None
        return payload

    def user_with_custom_role(self, source_team_data):
        team_members = source_team_data.get("data", {}).get("members", [])
        for member in team_members:
            if "id" in member.get("user", {}):
                del member["user"]["id"]
        payload = {"members": team_members}
        return payload

    def create_schedule_payload(team_schedule):
        schedule_name = team_schedule.get("data", {}).get("name")
        schedule_description = team_schedule.get("data", {}).get("description")
        schedule_timezone = team_schedule.get("data", {}).get("timezone")
        schedule_enabled = team_schedule.get("data", {}).get("enabled")
        schedule_owner_team = (
            team_schedule.get("data", {}).get("ownerTeam", {}).get("name")
        )
        schedule_rotations = team_schedule.get("data", {}).get("rotations")

        if schedule_rotations:
            for rotation in schedule_rotations:
                if "id" in rotation:
                    del rotation["id"]
                for participant in rotation.get("participants", []):
                    if "id" in participant:
                        del participant["id"]
                    if "data" in participant:
                        del participant["data"]
                for restriction in rotation.get("restrictions", []):
                    if "id" in restriction:
                        del restriction["id"]
                    if "data" in restriction:
                        del restriction["data"]
                for period in rotation.get("periods", []):
                    if "id" in period:
                        del period["id"]
                    if "data" in period:
                        del period["data"]
        payload = {
            "name": schedule_name,
            "description": schedule_description,
            "timezone": schedule_timezone,
            "enabled": schedule_enabled,
            "ownerTeam": {"name": schedule_owner_team},
            "rotations": schedule_rotations,
        }
        return payload

    def create_escalation_payload(self, source_escalations, team_name):
        escalation_payloads = []
        for escalation in source_escalations:
            if escalation["ownerTeam"]["name"] == team_name:
                payload = {
                    "description": escalation["description"],
                    "name": escalation["name"],
                    "ownerTeam": {"name": escalation["ownerTeam"]["name"]},
                    "rules": [
                        {
                            "condition": rule["condition"],
                            "delay": rule["delay"],
                            "notifyType": rule["notifyType"],
                            "recipient": {
                                "name": rule["recipient"]["name"],
                                "type": rule["recipient"]["type"],
                            },
                        }
                        if "recipient" in rule
                        and "name" in rule["recipient"]
                        and "type" in rule["recipient"]
                        else {
                            "condition": rule["condition"],
                            "delay": rule["delay"],
                            "notifyType": rule["notifyType"],
                        }
                        for rule in escalation["rules"]
                    ],
                }
                escalation_payloads.append(payload)
        return escalation_payloads

    def create_routing_rule_payload(self, source_routing_rules):
        routing_rule_payloads = []
        for routing_rule in source_routing_rules:
            notify_name = (
                routing_rule["notify"]["name"]
                if "name" in routing_rule["notify"]
                else None
            )
            payload = {
                "name": routing_rule["name"],
                "enabled": routing_rule.get("enabled", True),
                "criteria": routing_rule["criteria"],
                "notify": {"name": notify_name, "type": routing_rule["notify"]["type"]},
                "order": routing_rule["order"],
                "timezone": routing_rule["timezone"],
            }
            if "timeRestriction" in routing_rule:
                payload["timeRestriction"] = routing_rule["timeRestriction"]
            routing_rule_payloads.append(payload)
        return routing_rule_payloads

    def create_user_payload(self, admin):
        return {"user": {"username": admin["user"]["username"]}, "role": admin["role"]}
