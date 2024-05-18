import argparse
import os

from dotenv import load_dotenv
from termcolor import colored

from src.delete_data import DeleteData
from src.delete_team import DeleteTeam
from src.display import Display
from src.get_data import GetData
from src.menu import Menu
from src.patch_data import PatchData
from src.payload import Payload
from src.post_data import PostData
from src.write_file import WriteFile
from utils.assets import (BASE_URL, RETURN_MENU, SEP_D, SEP_S, SHOW_PAYLOAD,
                          SHOW_RESPONSE, clear, display_title)

load_dotenv()


SOURCE_API_KEY = os.getenv("SOURCE_API_KEY")
if SOURCE_API_KEY is None:
    print("Source API Key not found in .env file")
    exit(1)

DESTINATION_API_KEY = os.getenv("DESTINATION_API_KEY")
if DESTINATION_API_KEY is None:
    print("Destination API Key not found in .env file")
    exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--color", action="store_true", help="Display output in color")
    args = parser.parse_args()
    clear()
    display_title()
    print(SEP_D)
    display_source_teams = Display(
        GetData(f"{BASE_URL}/teams", SOURCE_API_KEY).get_teams()
    )
    display_destination_teams = Display(
        GetData(f"{BASE_URL}/teams", DESTINATION_API_KEY).get_teams()
    )
    menu = Menu(GetData(f"{BASE_URL}/teams", SOURCE_API_KEY).get_teams())
    message = Display(args)

    display_source_teams.display_source_teams(display_destination_teams.data)
    display_destination_teams.display_destination_teams()

    team_index = menu.get_valid_team_index()
    if team_index is None:
        return
    team = GetData(f"{BASE_URL}/teams", SOURCE_API_KEY).get_teams()[team_index - 1]
    print(SEP_S)
    team = GetData(f"{BASE_URL}/teams", SOURCE_API_KEY).get_teams()[team_index - 1]

    message.display_message(team["name"], "selected")
    if team["name"] in [d["name"] for d in display_destination_teams.data]:
        team_name = colored(team["name"], "white")
        message.display_message(team["name"], "already exists in destination", "🚫")

        if menu.confirm(f"to delete {team_name}"):
            destination_team_id = GetData(
                f"{BASE_URL}/teams", DESTINATION_API_KEY
            ).get_team_id(team["name"])
            message.display_message("Destination Team ID", destination_team_id)
            delete_team = DeleteTeam(
                f"{BASE_URL}/teams/{destination_team_id}", DESTINATION_API_KEY
            )
            result = delete_team.del_team()
            if SHOW_RESPONSE == "yes":
                message.display_debug_data(result)
            message.display_message(team["name"], "deleted")
            exit(0)
        else:
            exit(0)
    else:
        team_name = colored(team["name"], "green")
        if not menu.confirm(f"to migrate {team_name} on destination"):
            exit(0)

    # Step 1 - Post Team
    message.display_step(1, "Create Team", "🧑‍🤝‍🧑")
    source_team_data = GetData(f"{BASE_URL}/teams", SOURCE_API_KEY).get_team_data(
        team["id"]
    )
    payload = Payload(source_team_data)
    destination_team_payload = payload.create_team_payload_without_members(
        source_team_data
    )
    if SHOW_PAYLOAD == "yes":
        message.display_payload_data(destination_team_payload)
    message.display_message("Source Team ID", team["id"])
    message.display_message(team["name"], "payload created")
    post_data = PostData(
        f"{BASE_URL}/teams", DESTINATION_API_KEY, destination_team_payload
    )
    result = post_data.post_data(destination_team_payload)
    if SHOW_RESPONSE == "yes":
        message.display_debug_data(result)
    message.display_message(f"Team {team['name']}", "migrated")

    # Step 2 - Create Custom Roles
    message.display_step(2, "Create Custom Roles", "⏳")
    destination_team = GetData(f"{BASE_URL}/teams", DESTINATION_API_KEY)
    destination_team_id = destination_team.get_team_id(team["name"])
    message.display_message("Destination Team ID", destination_team_id)
    source_custom_roles = GetData(
        f"{BASE_URL}", SOURCE_API_KEY, team["id"]
    ).get_custom_roles()
    destination_custom_roles_payload = payload.create_custom_role_payload(
        source_custom_roles
    )
    if SHOW_PAYLOAD == "yes":
        message.display_payload_data(destination_custom_roles_payload)
    message.display_message(team["name"], "custom roles payload created")
    post_custom = PostData(
        f"{BASE_URL}", DESTINATION_API_KEY, destination_custom_roles_payload
    )
    result = post_custom.post_custom_roles(
        destination_custom_roles_payload, destination_team_id
    )
    if SHOW_RESPONSE == "yes":
        message.display_debug_data(result)
    message.display_message(f"Team {team['name']}", "custom roles migrated")

    # Step 3 - Patch Team Routing Rule
    message.display_step(3, "Patch Team Routing Rule", "🔁")
    destination_routing_rule = GetData(f"{BASE_URL}", DESTINATION_API_KEY)
    destination_routing_rule_id = destination_routing_rule.get_default_routing_rule_id(
        destination_team_id
    )
    message.display_message("Routing Rule ID", destination_routing_rule_id)
    patch_data = PatchData(
        f"{BASE_URL}",
        DESTINATION_API_KEY,
        destination_team_payload,
        destination_team_id,
        destination_routing_rule_id,
    )
    result = patch_data.patch_team_routing_rule(
        destination_team_id, destination_team_payload, destination_routing_rule_id
    )
    if SHOW_RESPONSE == "yes":
        message.display_debug_data(result)
    message.display_message(f"Team {team['name']}", "routing rule patched")

    # Step 4 - Delete Default Escalation Policy
    message.display_step(4, "Delete Default Escalation Policy", "🗑️")
    destination_team = GetData(f"{BASE_URL}/teams", DESTINATION_API_KEY)
    destination_escalation_id = GetData(
        f"{BASE_URL}/escalations", DESTINATION_API_KEY
    ).get_escalation_id(team["name"])
    if SHOW_PAYLOAD == "yes":
        message.display_payload_data(destination_escalation_id)
    message.display_message("Escalation ID", destination_escalation_id)
    delete_data = DeleteData(
        f"{BASE_URL}/escalations/{destination_escalation_id}",
        DESTINATION_API_KEY,
        destination_escalation_id,
    )
    result = delete_data.del_default_escalation(destination_escalation_id)
    if SHOW_RESPONSE == "yes":
        message.display_debug_data(result)
    message.display_message(f"Default {team['name']}_escalation", "deleted")

    # Step 5 - Add Schedules
    message.display_step(5, "Add Schedules", "📅")
    ownerTeam = team["name"]
    source_schedule_id = GetData(
        f"{BASE_URL}/schedules", SOURCE_API_KEY
    ).get_team_shedules_id(ownerTeam)
    source_schedule_data = GetData(
        f"{BASE_URL}/schedules", SOURCE_API_KEY
    ).get_schedule(source_schedule_id)
    schedule_payload = Payload.create_schedule_payload(source_schedule_data)
    if SHOW_PAYLOAD == "yes":
        message.display_payload_data(schedule_payload)
    post_schedules = PostData(
        f"{BASE_URL}/schedules", DESTINATION_API_KEY, schedule_payload
    )
    result = post_schedules.post_data(schedule_payload)
    if SHOW_RESPONSE == "yes":
        message.display_debug_data(result)
    message.display_message(f"Schedule {schedule_payload['name']}", "migrated")

    # Step 6 - Add Escalations
    message.display_step(6, "Add Escalations", "📈")
    escalations = GetData(f"{BASE_URL}/escalations", SOURCE_API_KEY).get_escalations()
    escalation_payload = payload.create_escalation_payload(escalations, team["name"])
    if SHOW_PAYLOAD == "yes":
        message.display_payload_data(escalation_payload)
    for escalation in escalation_payload:
        post_escalation = PostData(
            f"{BASE_URL}/escalations", DESTINATION_API_KEY, escalation
        )
        result = post_escalation.post_data(escalation)
        if SHOW_RESPONSE == "yes":
            message.display_debug_data(result)
        message.display_message(f"{escalation['name']}", "migrated")

    # Step 7 - Add Routing Rules
    message.display_step(7, "Add Routing Rules", "🔁")
    source_routing_rules = GetData(
        f"{BASE_URL}/teams/{team['id']}/routing-rules", SOURCE_API_KEY
    ).get_routing_rules()
    routing_rule_payloads = payload.create_routing_rule_payload(source_routing_rules)
    if SHOW_PAYLOAD == "yes":
        message.display_payload_data(routing_rule_payloads)
    for routing_rule in routing_rule_payloads:
        if routing_rule["name"] != "Default Routing Rule":
            post_routing = PostData(
                f"{BASE_URL}/teams/{destination_team_id}/routing-rules",
                DESTINATION_API_KEY,
                routing_rule,
            )
            result = post_routing.post_data(routing_rule)
            if SHOW_RESPONSE == "yes":
                message.display_debug_data(result)
            message.display_message(f"{routing_rule['name']}", "migrated")

    # Step 8 - Add Integrations
    message.display_step(8, "Add Integrations", "🔌")
    src_integration_ids = GetData(
        f"{BASE_URL}/integrations", SOURCE_API_KEY, team["id"]
    )
    integration_ids = src_integration_ids.get_team_integrations_id(
        src_integration_ids.team_id
    )
    (
        integration_payload,
        slack_integration_payload,
    ) = src_integration_ids.get_team_integrations(integration_ids)
    post_integrations = PostData(f"{BASE_URL}/integrations", DESTINATION_API_KEY)
    print(integration_payload)
    return_data = post_integrations.post_team_integrations(integration_payload)
    print(return_data)

    if None in return_data:
        message.display_message("Integrations already exist...", "Skipping")
    else:
        if os.path.exists(f"integrations/{team['name']}"):
            message.display_message(
                f"Directory for {team['name']} already exists...", "Skipping"
            )
        else:
            os.makedirs(f"integrations/{team['name']}", exist_ok=True)
            message.display_message(f"Creating directory for {team['name']}")

            write_to_file = WriteFile(
                "w", f"integrations/{team['name']}/{team['name']}_INTEGRATIONS.md"
            )
            for integrations in return_data:
                write_to_file.write_to_txt("")
                write_to_file.mode = "a"
                output = GetData.get_integration_output(integrations)
                write_to_file.write_to_txt(output)
                message.display_message(f"{integrations['name']}", "Migrated")
                if len(slack_integration_payload) > 0:
                    slack_integrations_list = []
                    for slack_integrations in slack_integration_payload:
                        slack_output = GetData.get_slack_integration_output(
                            slack_integrations
                        )
                        slack_integrations_list.append(slack_output)
                        write_to_file_slack = WriteFile(
                            "w",
                            f"integrations/{team['name']}/{team['name']}_SLACK_INTEGRATIONS.md",
                        )
                    for integration in slack_integrations_list:
                        write_to_file_slack.mode = "a"
                        write_to_file_slack.write_to_txt(integration)
                    message.display_message("Wrote Slack integrations to .md", "")

    # Step 9 - Update Users (Add Custom Roles)
    message.display_step(9, "Update Users", "👤")
    source_team_admins = GetData(f"{BASE_URL}/teams", SOURCE_API_KEY).get_team_admins(
        source_team_data
    )

    for admin in source_team_admins:
        user_payload = payload.create_user_payload(admin)
        if SHOW_PAYLOAD == "yes":
            message.display_payload_data(user_payload)
        destination_team_id = destination_team.get_team_id(team["name"])
        result = post_custom.post_user_custom_role(user_payload, destination_team_id)
        if result.get("message") is not None and "No user exists" not in result.get(
            "message"
        ):
            message.display_message(f"{admin['user']['username']}", "migrated")
        elif result.get("message") is not None and "No user exists" in result.get(
            "message"
        ):
            write_to_file_missing_users = WriteFile(
                "w", f"integrations/{team['name']}/{team['name']}_MISSING_USERS.md"
            )
            write_to_file_missing_users.mode = "a"
            message.display_message(f"{admin['user']['username']}", "does not exist")
            output = GetData.get_missing_users_output(result)
            write_to_file_missing_users.write_to_txt(output)

    if RETURN_MENU == "no":
        exit(0)
    else:
        main()


if __name__ == "__main__":
    main()
