import argparse
import subprocess
import sys
import tkinter as tk


def notification_simple(text: str, description: str, delay):
    window = tk.Tk(className="easy-game-launcher")
    window.overrideredirect(True)
    window.geometry("200x50+0+0")
    window.attributes('-topmost', True)
    window.after(delay, window.destroy)

    tk.Label(window, text=text).pack()
    tk.Label(window, text=description).pack()

    window.mainloop()


def send(text: str, description: str, delay: int = 5000):
    subprocess.Popen([sys.executable, __file__, "--text", text, "--description", description, "--delay", str(delay)])


if __name__ == "__main__":
    arguments = argparse.ArgumentParser()

    arguments.add_argument("--text", default="")
    arguments.add_argument("--description", default="")
    arguments.add_argument("--delay", default=5000)

    args = arguments.parse_args()

    notification_simple(args.text, args.description, args.delay)
