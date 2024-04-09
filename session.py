import json
import notification
import os
import vars
import time
import threading

with open(vars.GAME_PATH, "rb") as f:
    games = json.load(f)

status = "Online"

game_thread: threading.Thread

session = ""


def set_status(new_status: str = "Online"):
    global status
    status = new_status


def get_session() -> str | None:
    global session
    if session == "":
        return None
    else:
        return session


def exit_session():
    global game_thread, session
    if get_session() is None:
        notification.send("Cannot exit session", "There is no Game running", 4000)
        return
    session = ""
    set_status()


def run(name: str):
    global games
    cmd = games[name]["cmd"]
    before_time = time.time()
    os.system(cmd)
    took = time.time() - before_time
    if took >= 30.0:
        print("Exiting Session")
        exit_session()
    else:
        print("Command exited too Fast")


def new_session(name: str):
    global games, game_thread, session
    if get_session() is not None:
        notification.send(f"Could not start {name}.", "Another Game is already Running", 4000)
        return
    if name not in games or "cmd" not in games[name]:
        notification.send(f"Could not start {name}.", "Game not found", 4000)
        return
    session = name
    game_thread = threading.Thread(name=name, args=(name,), target=run)
    game_thread.start()
    set_status("Playing " + name)
