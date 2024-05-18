import json

from termcolor import colored

from utils.assets import SEP_D, SEP_S, parse_args


class Display:
    def __init__(self, data, message=None):
        self.data = data
        self.args = parse_args()
        self.message = message

    def display_destination_teams(self):
        print("Destination Teams:")
        print(SEP_S)
        for index, team in enumerate(self.data, start=1):
            if self.args.color:
                print(f"{index:02}: {colored(team['name'], 'blue')}")
            else:
                print(f"{index:02}: {team['name']}")
        print(SEP_D)

    def display_source_teams(self, destination_teams):
        print("Source Teams:")
        print(SEP_S)
        message_length = len(SEP_S) - 1
        offset = 8
        for index, team in enumerate(self.data, start=1):
            migrated = any(d["name"] == team["name"] for d in destination_teams)
            if self.args.color:
                status = colored("✅", "green") if migrated else colored("❌", "red")
                team_name = (
                    colored(team["name"], "green")
                    if migrated
                    else colored(team["name"], "white")
                )
                message = f"{index:02}: {team_name}"
                message = message[: message_length + offset]
                print(message.ljust(message_length + offset) + status)
            else:
                status = "(migrated)" if migrated else "(not migrated)"
                message = f"{index:02}: {team['name']}"
                print(f"{message} {status.rjust(message_length - len(message))}")
        print(SEP_D)

    def display_users(self):
        for index, user in enumerate(self.data, start=1):
            print(f"{index}: {user['username']}")

    def display_policies(self):
        for index, policy in enumerate(self.data, start=1):
            print(f"{index}: {policy['name']}")

    def display_schedules(self):
        for index, schedule in enumerate(self.data, start=1):
            print(f"{index}: {schedule['name']}")

    def display_escalations(self):
        for index, escalation in enumerate(self.data, start=1):
            print(f"{index}: {escalation['name']}")

    def display_payload_data(self, payload):
        if self.args.color:
            print(f"{colored('Payload Data:', 'magenta')}")
            print(SEP_S)
            print(colored(json.dumps(payload, indent=4, sort_keys=True), "white"))
            print(SEP_D)
        else:
            print("Payload:")
            print(SEP_S)
            print(json.dumps(payload, indent=4, sort_keys=True))
            print(SEP_D)

    def display_debug_data(self, result):
        if self.args.color:
            print(f"{colored('Debug Data:', 'magenta')}")
            print(SEP_S)
            print(colored(json.dumps(result, indent=4, sort_keys=True), "white"))
            print(SEP_D)
        else:
            print("Debug:")
            print(SEP_S)
            print(json.dumps(result, indent=4, sort_keys=True))
            print(SEP_D)

    def display_message(self, first_message, second_message=None, emoji=None):
        second_message = second_message or ""
        emoji = "✅" if emoji is None else emoji
        message_length = len(SEP_S) - 1
        offset = 8  # Adjust this value as needed
        if self.args.color:
            message = colored(first_message, "yellow") + " " + second_message
            message = message[: message_length + offset]
            print(message.ljust(message_length + offset) + emoji)
        else:
            message = first_message + " " + second_message
            message = message[:message_length]
            print(message.ljust(message_length))
        print(SEP_S)

    def display_step(self, step_number, step_name, emoji=None):
        message_length = len(SEP_S) - 1
        offset = 8
        if self.args.color:
            message = colored(f"Step {step_number}", "red") + " " + step_name
            message = message[: message_length + offset]
            print(message.ljust(message_length + offset) + emoji)
        else:
            message = f"Step {step_number}: {step_name}"
            message = message[:message_length]
            print(message.ljust(message_length))
        print(SEP_S)
