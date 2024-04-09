#!/usr/bin/env python3
import interface
import notification

if __name__ == "__main__":
    notification.send("EGL Running", "Easy Game Launcher is Running", 1500)
    interface.main()
