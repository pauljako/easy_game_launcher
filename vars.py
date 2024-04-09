import os

CONFIG_DIR = os.path.realpath(os.path.join(os.path.expanduser("~"), "EGL"))

ICON_DIR = os.path.realpath(os.path.join(CONFIG_DIR, "icons"))

GAME_PATH = os.path.realpath(os.path.join(CONFIG_DIR, "games.json"))

ACCOUNT_PATH = os.path.realpath(os.path.join(CONFIG_DIR, "account.json"))

SESSION_PATH = os.path.realpath(os.path.join(CONFIG_DIR, "session.pkl"))
