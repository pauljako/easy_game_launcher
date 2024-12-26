import json
import api
import tick
import dill
import notification
import os
import vars
import time
import threading
import main


class Session:
    def __init__(self, name: str, status: str):
        self.name = name
        self.game_thread = threading.Thread(name=name, target=self.run)
        self.status = status

    def run(self):
        cmd = main.games[self.name]["cmd"]
        before_time = time.time()
        os.system(cmd)
        took = time.time() - before_time
        if took >= 30.0:
            print("Exiting Session")
            exit_session()
        else:
            print("Command exited too Fast")

    def start(self):
        if not self.game_thread.is_alive():
            self.game_thread.start()
        threading.Thread(target=api.connect).start()

    def set_status(self, new_status: str = "Online"):
        self.status = new_status


session: Session = None


def get_session() -> Session | None:
    global session
    return session


def get_status() -> str:
    global session
    if session is None:
        return "Online"
    else:
        return session.status


def set_status(new_status: str = "Online") -> None:
    global session
    if session is None:
        return
    session.status = new_status


def exit_session():
    global session
    if get_session() is None:
        notification.send("Cannot exit session", "There is no Game running", 4000)
        return
    session = None
    if api.connection is not None:
        api.disconnect()


def new_session(name: str):
    global session
    if get_session() is not None:
        notification.send(f"Could not start {name}.", "Another Game is already Running", 4000)
        return
    if name not in main.games or "cmd" not in main.games[name]:
        notification.send(f"Could not start {name}.", "Game not found", 4000)
        return
    session = Session(name, "Playing " + name)
    get_session().start()
