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

        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(0, weight=1)
        self.icon = customtkinter.CTkImage(light_image=icon, size=(96, 96))
        self.icon_label = customtkinter.CTkLabel(self, image=self.icon, text="")
        self.icon_label.grid(row=0, column=0, pady=10, padx=5, sticky="ew", rowspan=2)
        self.label = customtkinter.CTkLabel(self, text=name)
        self.label.grid(row=0, column=1, pady=5, padx=5, sticky="ew", columnspan=2)
        self.launch_button = customtkinter.CTkButton(self, text="Launch", command=lambda x=name: session.new_session(x))
        self.launch_button.grid(row=1, column=1, pady=5, padx=5, sticky="ew")


class FriendFrame(customtkinter.CTkFrame):
    def __init__(self, master, name: str, id: int, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.label = customtkinter.CTkLabel(self, text=name)
        self.label.grid(row=0, column=0, pady=5, padx=5, sticky="ew", columnspan=2)


class AddGameWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.title("Add Game")

        self.label = customtkinter.CTkLabel(self, text="Add Game")
        self.label.pack(padx=20, pady=20)


add_game_window: AddGameWindow = None


def add_game(master):
    global add_game_window
    if add_game_window is None or not add_game_window.winfo_exists():
        add_game_window = AddGameWindow(master)
    else:
        add_game_window.focus()


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

    tab_view = customtkinter.CTkTabview(app, fg_color=app.cget("fg_color"))
    tab_view.grid(row=1, column=0, padx=5, pady=5, sticky="nesw")
    game_tab = tab_view.add("Games")
    game_tab.grid_columnconfigure(0, weight=1)
    game_tab.grid_rowconfigure(0, weight=1)
    friends_tab = tab_view.add("Friends")
    friends_tab.grid_columnconfigure(0, weight=1)
    friends_tab.grid_rowconfigure(0, weight=1)
    tab_view.set("Games")

    game_scrollable_frame = customtkinter.CTkScrollableFrame(game_tab, label_text="Games", fg_color="transparent")
    game_scrollable_frame.bind_all("<Button-4>", lambda e: game_scrollable_frame._parent_canvas.yview("scroll", -1, "units"))
    game_scrollable_frame.bind_all("<Button-5>", lambda e: game_scrollable_frame._parent_canvas.yview("scroll", 1, "units"))
    game_scrollable_frame.grid_columnconfigure(0, weight=1)
    game_scrollable_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nesw")

    friends_scrollable_frame = customtkinter.CTkScrollableFrame(friends_tab, label_text="Friends", fg_color="transparent")
    friends_scrollable_frame.bind_all("<Button-4>", lambda e: friends_scrollable_frame._parent_canvas.yview("scroll", -1, "units"))
    friends_scrollable_frame.bind_all("<Button-5>", lambda e: friends_scrollable_frame._parent_canvas.yview("scroll", 1, "units"))
    friends_scrollable_frame.grid_columnconfigure(0, weight=1)
    friends_scrollable_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nesw")

    game_list_row = 0
    game_list = []
    friend_list_row = 0
    friend_list = []

    for g in games.keys():
        btn_text = g

        icon = Image.open(os.path.join(vars.ICON_DIR, games[g]["icon"]))

        game_display_obj = GameFrame(game_scrollable_frame, g, icon)

        game_list.append(game_display_obj)

    add_game_btn = customtkinter.CTkButton(game_scrollable_frame, text="Add Game", command=lambda x=app: add_game(x))
    game_list.append(add_game_btn)

    for i in game_list:
        game_list_row += 1
        i.grid(row=game_list_row, column=0, padx=5, pady=5, sticky="ew")

    for i in friend_list:
        friend_list_row += 1
        i.grid(row=friend_list_row, column=0, padx=5, pady=5, sticky="ew")

    while True:
        app.update()
        app.update_idletasks()
        status_label.configure(text=session.get_status())
        if session.get_session() is not None:
            exit_button.grid(row=2, column=0, pady=5, padx=5, sticky="ew")
        else:
            exit_button.grid_forget()
