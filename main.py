#!/usr/bin/env python3
import argparse
import json
import os.path
import sys
import time

import interface
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


def move_game_up(game: str):
    global games
    if game not in games:
        print("[ Main | Error ] Can't move Game Up, Game not found")
        return

    gm_idx = 0
    gm_pos = 0

    for gm in games.keys():

        if gm == game:
            gm_pos = gm_idx

        gm_idx += 1

    if gm_pos == 0:
        gm_pos = 1

    gm_list = list(games.keys())
    gm_obj = gm_list.pop(gm_pos)
    gm_list.insert(gm_pos - 1, gm_obj)

    gm_new = {}

    for gm in gm_list:
        gm_new[gm] = games[gm]

    games = gm_new

    with open(vars.GAME_PATH, "wt") as fi:
        json.dump(games, fi)

    interface.redraw()


def move_game_down(game: str):
    global games
    if game not in games:
        print("[ Main | Error ] Can't move Game Down, Game not found")
        return

    gm_idx = 0
    gm_pos = 0

    for gm in games.keys():

        if gm == game:
            gm_pos = gm_idx

        gm_idx += 1

    gm_list = list(games.keys())
    gm_obj = gm_list.pop(gm_pos)
    gm_list.insert(gm_pos + 1, gm_obj)

    gm_new = {}

    for gm in gm_list:

        gm_new[gm] = games[gm]

    games = gm_new

    with open(vars.GAME_PATH, "wt") as fi:
        json.dump(games, fi)

    interface.redraw()
