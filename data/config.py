from json import load

with open('data/config.ini', 'r') as file:
    config_data = load(file)

admins = []
for admin in config_data["admins"].split():
    admins.append(admin)


BOT_TOKEN = config_data["token"]
ADMINS = admins


def is_admin(user):
    return str(user.id) in ADMINS
