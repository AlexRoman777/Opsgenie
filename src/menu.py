from termcolor import colored

from utils.assets import SEP_S, parse_args


class Menu:
    def __init__(self, data):
        self.data = data
        self.args = parse_args()

    def get_valid_team_index(self):
        while True:
            team_index = self.get_input(
                colored("Select a team to migrate or press 'q' to quit: ", "green")
            )
            if team_index.lower() == "q":
                return None
            try:
                team_index = int(team_index)
                if 1 <= team_index <= len(self.data):
                    return team_index
                else:
                    print(
                        colored(
                            f"Invalid selection. Please select a number between 1 and {len(self.data)}",
                            "yellow",
                        )
                    )
            except ValueError:
                print(colored("Invalid input. Please enter a number.", "red"))

    def get_input(self, prompt):
        if self.args.color:
            return input(colored(prompt, "green"))
        else:
            return input(prompt)

    def get_confirmation(self, message):
        while True:
            user_input = input(
                colored(message, "green") + colored(" [y/n] ", "red")
            ).lower()
            if user_input in ["y", "n", ""]:
                print(SEP_S)
                return user_input == "y"
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

    def return_to_main_menu(self):
        return self.get_confirmation("Return to main menu? ")

    def confirm(self, message):
        return self.get_confirmation(f"Do you want to {message}?")
