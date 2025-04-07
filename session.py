import subprocess
import api
import minecraft
import notification
import os
import time
import threading
import main

class Session:
    def __init__(self, name: str, status: str):
        self.name = name
        self.game_thread = threading.Thread(name=name, target=self.run)
        self.status = status

    def run(self):
        pass

    def start(self):
        if not self.game_thread.is_alive():
            self.game_thread.start()
        threading.Thread(target=api.connect).start()

    def set_status(self, new_status: str = "Online"):
        self.status = new_status

class CmdSession(Session):
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

class MinecraftSession(Session):
    def __init__(self, status: str, instance_directory: str, version: str, offline: bool = False, java_path: str | None = None):
        self.launch_cmd = minecraft.get_command(instance_directory, version, offline, java_path)
        super().__init__(status, f"Minecraft-{version}")

    def run(self):
        before_time = time.time()
        subprocess.run(self.launch_cmd)
        took = time.time() - before_time
        if took >= 30.0:
            print("Exiting Session")
            exit_session()
        else:
            print("Command exited too Fast")

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


def new_cmd_session(name: str):
    global session
    if get_session() is not None:
        notification.send(f"Could not start {name}.", "Another Game is already Running", 4000)
        return
    if name not in main.games or "cmd" not in main.games[name]:
        notification.send(f"Could not start {name}.", "Game not found", 4000)
        return
    session = CmdSession(name, "Playing " + name)
    get_session().start()

def new_minecraft_session(name: str):
    global session
    if get_session() is not None:
        notification.send(f"Could not start {name}.", "Another Game is already Running", 4000)
        return
    if name not in main.games or "version" not in main.games[name] or "instance" not in main.games[name]:
        notification.send(f"Could not start {name}.", "Game not found", 4000)
        return
    offline = False
    if "offline" in main.games[name]:
        offline = main.games[name]["offline"]

    java_path = None
    if "java_path" in main.games[name]:
        java_path = main.games[name]["java_path"]

    session = MinecraftSession("Playing " + name, main.games[name]["instance"], main.games[name]["version"], offline, java_path)
    get_session().start()

def new_session(name: str):
    if name in main.games:
        if "type" in main.games[name]:
            if "cmd" == main.games[name]["type"]:
                new_cmd_session(name)
            elif "minecraft" == main.games[name]["type"]:
                new_minecraft_session(name)
        else:
            new_cmd_session(name)
