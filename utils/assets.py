import argparse
import os

from dotenv import load_dotenv
from termcolor import colored

BASE_URL = "https://api.eu.opsgenie.com/v2"

SEP_S = "-" * 83
SEP_D = "=" * 83

load_dotenv()

# yes/no in lowercase
# Return to the main menu after each action
RETURN_MENU = "no"
# Display the payload of the request for debugging
SHOW_PAYLOAD = "yes"
# Display the response of the request for debugging
SHOW_RESPONSE = "yes"


def parse_args():
    """Parse the arguments passed to the script
    Returns:
        args: The arguments passed to the script
    """
    parser = argparse.ArgumentParser(description="OpsGenie Migration Tool")
    parser.add_argument("--color", action="store_true", help="Use colors in output")
    args = parser.parse_args()
    return args


def display_title():
    """Display the title of the script"""
    args = parse_args()
    if args.color:
        print(
            colored(
                """
             ██████╗ ██████╗ ███████╗ ██████╗ ███████╗███╗   ██╗██╗███████╗
            ██╔═══██╗██╔══██╗██╔════╝██╔════╝ ██╔════╝████╗  ██║██║██╔════╝
            ██║   ██║██████╔╝███████╗██║  ███╗█████╗  ██╔██╗ ██║██║█████╗
            ██║   ██║██╔═══╝ ╚════██║██║   ██║██╔══╝  ██║╚██╗██║██║██╔══╝
            ╚██████╔╝██║     ███████║╚██████╔╝███████╗██║ ╚████║██║███████╗
            ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═╝╚══════╝
        """,
                "red",
            )
        )
        message = "Migration Tool"
        padding = (len(SEP_S) - len(message)) // 2
        print(f"{' ' * padding}{message}\n")
    else:
        print("OpsGenie Migration Tool")


def clear():
    """Clear the terminal"""
    os.system("cls" if os.name == "nt" else "clear")


def debug(result):
    """Display the payload and the response of the request for debugging"""
    if SHOW_PAYLOAD == "yes":
        print(result)
