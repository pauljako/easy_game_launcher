#!/usr/bin/env python3
import argparse

import interface
import notification
import session

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Easy Game Launcher")

    parser.add_argument("--launch", "-l")

    args = parser.parse_args()

    if args.launch is None:
        notification.send("EGL Running", "Easy Game Launcher is Running", 1500)
        interface.main()
    else:
        notification.send("Game started", f"Game {args.launch} started.", 1500)
        session.new_session(args.launch)
