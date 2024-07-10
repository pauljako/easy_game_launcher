#!/usr/bin/env python3
import argparse
import json
import os.path
import sys
import time
import tick
import vars
import messages

# Load Games
with open(vars.GAME_PATH, "rb") as f:
    games: dict = json.load(f)

# Load Account
with open(vars.ACCOUNT_PATH, "rb") as f:
    account: dict = json.load(f)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="Easy Game Launcher", epilog="If no arguments are passed, the Interface "
                                                                       "will be opened")

    parser.add_argument("--launch", "-l", help="Launches the specified Game", metavar="game")
    parser.add_argument("--quit", "-q", help="Quits EGL", action="store_true")
    parser.add_argument("--exit", "-e", help="Exits the Session", action="store_true")
    parser.add_argument("--close", "-c", help="Closes the Interface", action="store_true")
    parser.add_argument("--start", "-s", help="Do nothing. Just start EGL in the Background", action="store_true")

    args = parser.parse_args()

    if vars.VERBOSE:
        print("[ Main | Info ] Triggering Hook: is-running")

    f = open(vars.IS_RUNNING_MSG_PATH, "wt")
    f.close()

    if args.quit:
        if vars.VERBOSE:
            print("[ Main | Info ] Triggering Hook: kill")
        with open(vars.KILL_MSG_PATH, "wt"):
            pass
    elif args.exit:
        if vars.VERBOSE:
            print("[ Main | Info ] Triggering Hook: exit")
        with open(vars.EXIT_MSG_PATH, "wt"):
            pass
    elif args.close:
        if vars.VERBOSE:
            print("[ Main | Info ] Triggering Hook: close-ui")
            with open(vars.CLOSE_UI_MSG_PATH, "wt"):
                pass
    elif args.launch is not None:
        if vars.VERBOSE:
            print("[ Main | Info ] Triggering Hook: launch")
        with open(vars.LAUNCH_GAME_MSG_PATH, "wt") as f:
            f.write(args.launch)
    elif args.start:
        print("[ Main | Info ] Starting in Background")
    else:
        if vars.VERBOSE:
            print("[ Main | Info ] Triggering Hook: open-ui")
        with open(vars.OPEN_UI_MSG_PATH, "wt"):
            pass

    time.sleep(0.5)

    if not os.path.exists(vars.IS_RUNNING_MSG_PATH):
        print("[ Main | Error ] Another Instance is already Running")
        sys.exit()

    if vars.VERBOSE:
        print("[ Main | Info ] Starting Main Tick")
    while True:
        tick.tick()
