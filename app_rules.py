import json
import os


RULES_FILE = "app_rules.json"


def load_rules():
    if not os.path.exists(RULES_FILE):
        return {}

    with open(RULES_FILE, "r") as file:
        return json.load(file)


def save_rules(rules):
    with open(RULES_FILE, "w") as file:
        json.dump(rules, file, indent=4)


def set_app_blocked(app_name, blocked):
    rules = load_rules()

    rules[app_name] = blocked

    save_rules(rules)


def is_app_blocked(app_name):
    rules = load_rules()

    return rules.get(app_name, False)


if __name__ == "__main__":

    set_app_blocked("Google Chrome", True)

    print("Chrome blocked:",
          is_app_blocked("Google Chrome"))

    print("\nCurrent rules:")
    print(load_rules())