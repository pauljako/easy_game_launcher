import os
import sys
import time

import interface
import notification
import session
import tick
import vars


@tick.on_tick(10, 1)
def process_messages():
    if os.path.exists(vars.IS_RUNNING_MSG_PATH):
        if vars.VERBOSE:
            print("[ Message | Info ] Processing Hook: is-running")
        while True:
            try:
                os.remove(vars.IS_RUNNING_MSG_PATH)
                break
            except:
                if vars.VERBOSE:
                    print("[ Message | Error ] Failed to delete Message. Trying again")
    if os.path.exists(vars.KILL_MSG_PATH):
        if vars.VERBOSE:
            print("[ Message | Info ] Processing Hook: kill")
        while True:
            try:
                os.remove(vars.KILL_MSG_PATH)
                break
            except:
                if vars.VERBOSE:
                    print("[ Message | Error ] Failed to delete Message. Trying again")
        if session.get_session() is not None:
            session.exit_session()
        sys.exit()
    if os.path.exists(vars.OPEN_UI_MSG_PATH):
        if vars.VERBOSE:
            print("[ Message | Info ] Processing Hook: open-ui")
        while True:
            try:
                os.remove(vars.OPEN_UI_MSG_PATH)
                break
            except:
                if vars.VERBOSE:
                    print("[ Message | Error ] Failed to delete Message. Trying again")
        if interface.app is not None:
            if vars.VERBOSE:
                print("[ Message | Warning ] Another Window is already opened")
            return
        interface.open_ui()
    if os.path.exists(vars.LAUNCH_GAME_MSG_PATH):
        if vars.VERBOSE:
            print("[ Message | Info ] Processing Hook: launch")
        with open(vars.LAUNCH_GAME_MSG_PATH, "rt") as f:
            game = f.read()
        while True:
            try:
                os.remove(vars.LAUNCH_GAME_MSG_PATH)
                break
            except:
                if vars.VERBOSE:
                    print("[ Message | Error ] Failed to delete Message. Trying again")
        notification.send("Game started", f"Game {game} started.", 1500)
        session.new_session(game)
    if os.path.exists(vars.EXIT_MSG_PATH):
        if vars.VERBOSE:
            print("[ Message | Info ] Processing Hook: exit")
        while True:
            try:
                os.remove(vars.EXIT_MSG_PATH)
                break
            except:
                if vars.VERBOSE:
                    print("[ Message | Error ] Failed to delete Message. Trying again")
        session.exit_session()
    if os.path.exists(vars.CLOSE_UI_MSG_PATH):
        if vars.VERBOSE:
            print("[ Message | Info ] Processing Hook: close-ui")
        while True:
            try:
                os.remove(vars.CLOSE_UI_MSG_PATH)
                break
            except:
                if vars.VERBOSE:
                    print("[ Message | Error ] Failed to delete Message. Trying again")
        interface.win_quit()


def process_ega_messages(message: list[str]) -> list[str]:
    if message[0] == "achievement":
        if len(message) != 3:
            print("[ EGA | Error ] Not enough Data Send")
            return ["error", "not_enough_data"]
        else:
            if vars.VERBOSE:
                print(f"[ EGA | Info ] Adding Achievement: {message[1]}")
            return ["ok"]
    else:
        return ["error", "unknown_command"]
