from json import load

with open('data/config.ini', 'r') as file:
    config_data = load(file)

admins = []
for admin in config_data["admins"].split():
    admins.append(admin)


BOT_TOKEN = config_data["token"]

ADMINS = admins

# need to ask consultant his ID
# my temp id here
CONSULTANT = 912239061

def is_admin(user):
    return str(user.id) in ADMINS


ROLE_NAMES = {
    "user": "user",
    "admin": "admin",
    "consultant": "consultant"
}

ROLES = {
    "admins": ADMINS,
    "consultant": CONSULTANT
}

ROLE_COMMANDS = {
    "consultant_on": "!&consult",
    "consultant_off": "!&consultoff",

    "admin_on": "",
    "admin_off": ""
}



