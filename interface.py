import json
import threading
import time
import vars
import session

import customtkinter
import os
from PIL import Image

with open(vars.GAME_PATH, "rb") as f:
    games = json.load(f)

with open(vars.ACCOUNT_PATH, "rb") as f:
    account = json.load(f)

status_label: customtkinter.CTkLabel


class GameFrame(customtkinter.CTkFrame):
    def __init__(self, master, name, icon: Image, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame, for example:
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(0, weight=1)
        self.icon = customtkinter.CTkImage(light_image=icon, size=(96, 96))
        self.icon_label = customtkinter.CTkLabel(self, image=self.icon, text="")
        self.icon_label.grid(row=0, column=0, pady=10, padx=5, sticky="ew", rowspan=2)
        self.label = customtkinter.CTkLabel(self, text=name)
        self.label.grid(row=0, column=1, pady=5, padx=5, sticky="ew", columnspan=2)
        self.launch_button = customtkinter.CTkButton(self, text="Launch", command=lambda x=name: session.new_session(x))
        self.launch_button.grid(row=1, column=1, pady=5, padx=5, sticky="ew")


def main():
    global status_label

    app = customtkinter.CTk(className="easy-game-launcher")

    app.title("Easy Game Launcher")
    app.geometry("500x550")
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=1)

    account_frame = customtkinter.CTkFrame(app)
    account_frame.grid(row=0, column=0, padx=10, pady=5, sticky="new")
    account_frame.grid_columnconfigure(0, weight=1)
    username = customtkinter.CTkLabel(account_frame, text=account["name"])
    username.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    status_label = customtkinter.CTkLabel(account_frame, text=session.get_status())
    status_label.grid(row=1, column=0, pady=5, padx=5, sticky="ew")
    exit_button = customtkinter.CTkButton(account_frame, text="Exit", command=session.exit_session)

    scrollable_frame = customtkinter.CTkScrollableFrame(app, label_text="Games", fg_color="transparent")
    scrollable_frame.bind_all("<Button-4>", lambda e: scrollable_frame._parent_canvas.yview("scroll", -1, "units"))
    scrollable_frame.bind_all("<Button-5>", lambda e: scrollable_frame._parent_canvas.yview("scroll", 1, "units"))
    scrollable_frame.grid_columnconfigure(0, weight=1)
    scrollable_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nesw")

    btn_row = 0
    game_list = []

    for g in games.keys():
        btn_text = g

        icon = Image.open(os.path.join(vars.ICON_DIR, games[g]["icon"]))

        game_display_obj = GameFrame(scrollable_frame, g, icon)

        game_list.append(game_display_obj)

        btn_row += 1

    for i in range(btn_row):
        game_list[i].grid(row=i, column=0, padx=5, pady=5, sticky="ew")

    while True:
        app.update()
        app.update_idletasks()
        status_label.configure(text=session.get_status())
        if session.get_session() is not None:
            exit_button.grid(row=2, column=0, pady=5, padx=5, sticky="ew")
        else:
            exit_button.grid_forget()
