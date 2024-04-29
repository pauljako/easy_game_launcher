import os
import time

import interface
import notification
import session
import tick
import vars


@tick.on_tick(10)
def process_messages():
    if os.path.exists(vars.IS_RUNNING_MSG_PATH):
        if vars.VERBOSE:
            print("[ Message | Info ] Processing Hook: is-running")
        os.remove(vars.IS_RUNNING_MSG_PATH)
    if os.path.exists(vars.KILL_MSG_PATH):
        if vars.VERBOSE:
            print("[ Message | Info ] Processing Hook: kill")
        os.remove(vars.KILL_MSG_PATH)
        if session.get_session() is not None:
            session.exit_session()
        exit()
    if os.path.exists(vars.OPEN_UI_MSG_PATH):
        if vars.VERBOSE:
            print("[ Message | Info ] Processing Hook: open-ui")
        os.remove(vars.OPEN_UI_MSG_PATH)
        if interface.app is not None:
            if vars.VERBOSE:
                print("[ Message | Warning ] Another Window is already opened")
            return
        interface.main()
    if os.path.exists(vars.LAUNCH_GAME_MSG_PATH):
        if vars.VERBOSE:
            print("[ Message | Info ] Processing Hook: launch")
        with open(vars.LAUNCH_GAME_MSG_PATH, "rt") as f:
            game = f.read()
        os.remove(vars.LAUNCH_GAME_MSG_PATH)
        notification.send("Game started", f"Game {game} started.", 1500)
        session.new_session(game)
    if os.path.exists(vars.EXIT_MSG_PATH):
        if vars.VERBOSE:
            print("[ Message | Info ] Processing Hook: exit")
        os.remove(vars.EXIT_MSG_PATH)
        session.exit_session()
