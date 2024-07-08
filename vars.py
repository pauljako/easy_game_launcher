import os

VERBOSE = True

EGA_SEPERATOR = ":-:"

CONFIG_DIR = os.path.realpath(os.path.join(os.path.expanduser("~"), "EGL"))

ICON_DIR = os.path.realpath(os.path.join(CONFIG_DIR, "icons"))

GAME_PATH = os.path.realpath(os.path.join(CONFIG_DIR, "games.json"))

ACCOUNT_PATH = os.path.realpath(os.path.join(CONFIG_DIR, "account.json"))

TICK_OBJ_PATH = os.path.realpath(os.path.join(CONFIG_DIR, "tick.pkl"))

TICK_THREAD_PATH = os.path.realpath(os.path.join(CONFIG_DIR, "tick_thread.pkl"))

MESSAGE_PATH = os.path.realpath(os.path.join(CONFIG_DIR, "message"))

OPEN_UI_MSG_PATH = os.path.realpath(os.path.join(MESSAGE_PATH, "open_ui"))

CLOSE_UI_MSG_PATH = os.path.realpath(os.path.join(MESSAGE_PATH, "close_ui"))

LAUNCH_GAME_MSG_PATH = os.path.realpath(os.path.join(MESSAGE_PATH, "launch"))

IS_RUNNING_MSG_PATH = os.path.realpath(os.path.join(MESSAGE_PATH, "is-running"))

KILL_MSG_PATH = os.path.realpath(os.path.join(MESSAGE_PATH, "kill"))

EXIT_MSG_PATH = os.path.realpath(os.path.join(MESSAGE_PATH, "exit"))
