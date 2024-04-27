#!/usr/bin/env python3
import argparse
import os.path
import time

import tick
import vars
import messages


if __name__ == "__main__":

    running = True

    parser = argparse.ArgumentParser(prog="Easy Game Launcher")

    parser.add_argument("--launch", "-l")

    args = parser.parse_args()

    with open(vars.IS_RUNNING_MSG_PATH, "wt"):
        pass

    if args.launch is None:
        with open(vars.OPEN_UI_MSG_PATH, "wt"):
            pass
    else:
        with open(vars.LAUNCH_GAME_MSG_PATH, "wt") as f:
            f.write(args.launch)

    time.sleep(0.5)

    if not os.path.exists(vars.IS_RUNNING_MSG_PATH):
        print("[ Main | Error ] Another Instance is already Running")
        exit()

    if vars.VERBOSE:
        print("[ Main | Info ] Starting Main Tick")
    while running:
        tick.tick()
