import json
import shutil
import threading
import time
import tkinter
import tkinter.filedialog
import main
import notification
import vars
import session
import tick

import customtkinter
import os
from PIL import Image

# Define Global Variables
status_label: customtkinter.CTkLabel
exited: bool = False
app: customtkinter.CTk = None
exit_button: customtkinter.CTkButton
exit_triggered: bool = False
game_right_click_menu: tkinter.Menu = None
game_right_click_menu_game: str = ""
game_right_click_menu_pin: tkinter.IntVar = None


# Frame that shows the Game List
class GameFrame(customtkinter.CTkFrame):
    def __init__(self, master, name, icon: Image, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(0, weight=1)
        self.icon = customtkinter.CTkImage(light_image=icon, size=(96, 96))
        self.icon_label = customtkinter.CTkLabel(self, image=self.icon, text="")
        self.icon_label.grid(row=0, column=0, pady=10, padx=5, sticky="ew", rowspan=2)
        self.icon_label.bind("<Button-2>", lambda x, y=name: open_game_right_click_menu(x, y))
        self.label = customtkinter.CTkLabel(self, text=name)
        self.label.grid(row=0, column=1, pady=5, padx=5, sticky="ew", columnspan=2)
        self.label.bind("<Button-2>", lambda x, y=name: open_game_right_click_menu(x, y))
        self.launch_button = customtkinter.CTkButton(self, text="Launch", command=lambda x=name: session.new_session(x))
        self.launch_button.grid(row=1, column=1, pady=5, padx=5, sticky="ew")
        self.launch_button.bind("<Button-2>", lambda x, y=name: open_game_right_click_menu(x, y))
        self.bind("<Button-2>", lambda x, y=name: open_game_right_click_menu(x, y))


# Frame that shows the Friends List
class FriendFrame(customtkinter.CTkFrame):
    def __init__(self, master, name: str, id: int, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.label = customtkinter.CTkLabel(self, text=name)
        self.label.grid(row=0, column=0, pady=5, padx=5, sticky="ew", columnspan=2)


# Window for adding Games
class AddGameWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x500")
        self.title("Add Game")
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)

        self.label = customtkinter.CTkLabel(self, text="Add Game")
        self.label.grid(padx=20, pady=20, row=0, column=0, sticky="ew", columnspan=2)

        self.name_entry = customtkinter.CTkEntry(self, placeholder_text="Name")
        self.name_entry.grid(padx=20, pady=20, row=1, column=0, sticky="ew", columnspan=2)

        self.cmd_entry = customtkinter.CTkEntry(self, placeholder_text="Launch Command")
        self.cmd_entry.grid(padx=20, pady=20, row=2, column=0, sticky="ew", columnspan=2)

        self.icon_entry = customtkinter.CTkEntry(self, placeholder_text="Path to Icon")
        self.icon_entry.grid(padx=20, pady=20, row=3, column=0, sticky="ew")

        self.icon_browse = customtkinter.CTkButton(self, command=self.browse_icon, text="Browse")
        self.icon_browse.grid(padx=20, pady=20, row=3, column=1, sticky="ew")

        self.save_button = customtkinter.CTkButton(self, command=self.save, text="Add")
        self.save_button.grid(padx=20, pady=20, row=4, column=0, sticky="ew", columnspan=2)

    def browse_icon(self):
        icon = tkinter.filedialog.askopenfilename(title="Select Icon")

        self.icon_entry.insert(tkinter.END, icon)

    def save(self):

        icon = self.icon_entry.get()

        if icon == "":
            self.browse_icon()

        icon = self.icon_entry.get()

        if icon == "":
            return

        new_icon_name = self.name_entry.get().lower().replace(" ", "_")
        new_icon_path = str(os.path.join(vars.ICON_DIR, new_icon_name))

        new_icon_path = shutil.copy(icon, new_icon_path)

        saved_data = {"cmd": self.cmd_entry.get(), "icon": new_icon_path}
        main.games[self.name_entry.get()] = saved_data
        with open(vars.GAME_PATH, "wt") as f:
            json.dump(main.games, f)

        self.destroy()
        redraw()


add_game_window: AddGameWindow = None


def add_game(master):
    global add_game_window
    if add_game_window is None or not add_game_window.winfo_exists():
        add_game_window = AddGameWindow(master)
    else:
        add_game_window.focus()


def win_quit():
    global exit_triggered
    exit_triggered = True


@tick.on_tick(21, 2)
def win_update():
    global status_label, app, exited, exit_button, exit_triggered
    if app is None:
        return
    app.update()
    app.update_idletasks()
    if exit_triggered:
        if vars.VERBOSE:
            print("[ Interface | Info ] App exiting")
        # notification.send("EGL Running", "Easy Game Launcher is still running in the Background", delay=1500)
        app.destroy()
        app.update()
        app = None
        return
    status_label.configure(text=session.get_status())
    if session.get_session() is not None:
        exit_button.grid(row=2, column=0, pady=5, padx=5, sticky="ew")
    else:
        exit_button.grid_forget()


def draw():
    global status_label, app, exited, exit_button, game_right_click_menu, game_right_click_menu_game, game_right_click_menu_pin

    account_frame = customtkinter.CTkFrame(app)
    account_frame.grid(row=0, column=0, padx=10, pady=5, sticky="new")
    account_frame.grid_columnconfigure(0, weight=1)
    username = customtkinter.CTkLabel(account_frame, text=main.account["name"])
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
    game_scrollable_frame.bind_all("<Button-4>",
                                   lambda e: game_scrollable_frame._parent_canvas.yview("scroll", -1, "units"))
    game_scrollable_frame.bind_all("<Button-5>",
                                   lambda e: game_scrollable_frame._parent_canvas.yview("scroll", 1, "units"))
    game_scrollable_frame.grid_columnconfigure(0, weight=1)
    game_scrollable_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nesw")

    friends_scrollable_frame = customtkinter.CTkScrollableFrame(friends_tab, label_text="Friends",
                                                                fg_color="transparent")
    friends_scrollable_frame.bind_all("<Button-4>",
                                      lambda e: friends_scrollable_frame._parent_canvas.yview("scroll", -1, "units"))
    friends_scrollable_frame.bind_all("<Button-5>",
                                      lambda e: friends_scrollable_frame._parent_canvas.yview("scroll", 1, "units"))
    friends_scrollable_frame.grid_columnconfigure(0, weight=1)
    friends_scrollable_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nesw")

    game_list_row = 0
    game_list = []
    friend_list_row = 0
    friend_list = []

    non_pinned_games = []

    for g in main.games.keys():

        if ("pinned" in main.games[g]) and (main.games[g]["pinned"] is True):

            icon = Image.open(os.path.join(vars.ICON_DIR, main.games[g]["icon"]))

            game_display_obj = GameFrame(game_scrollable_frame, g, icon)

            game_list.append(game_display_obj)

        else:

            non_pinned_games.append(g)

    for g in non_pinned_games:
        icon = Image.open(os.path.join(vars.ICON_DIR, main.games[g]["icon"]))

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

    game_right_click_menu_pin = tkinter.IntVar(value=0)

    game_right_click_menu = tkinter.Menu(app, tearoff=0)
    game_right_click_menu.add_command(label="Launch", command=lambda: session.new_session(game_right_click_menu_game))
    game_right_click_menu.add_command(label="Achievements")
    game_right_click_menu.add_separator()
    game_right_click_menu.add_checkbutton(label="Pin", variable=game_right_click_menu_pin)
    game_right_click_menu.add_command(label="Move Up", command=lambda: main.move_game_up(game_right_click_menu_game))
    game_right_click_menu.add_command(label="Move Down", command=lambda: main.move_game_down(game_right_click_menu_game))
    game_right_click_menu.add_separator()
    game_right_click_menu.add_command(label="Remove", command=lambda: remove_game(game_right_click_menu_game))


@tick.on_tick(22, 7500)
def redraw():
    global exited, app
    if exited or (app is None):
        return
    draw()


def remove_game(name: str):
    if name not in main.games:
        notification.send(f"Could not Remove {name}", "Game not Found", 4000)
        return
    main.games.pop(name)
    with open(vars.GAME_PATH, "wt") as f:
        json.dump(main.games, f)
    redraw()


def open_game_right_click_menu(event: tkinter.Event, game: str):
    global game_right_click_menu_game, game_right_click_menu_pin
    game_right_click_menu_game = game
    if (game in main.games) and ("pinned" in main.games[game]) and (main.games[game]["pinned"] is True):
        before_pin = 1
        game_right_click_menu_pin.set(1)
    else:
        before_pin = 0
        game_right_click_menu_pin.set(0)
    game_right_click_menu.tk_popup(event.x_root, event.y_root)
    if (game in main.games) and (game_right_click_menu_pin.get() != before_pin):
        if game_right_click_menu_pin.get() == 1:
            main.games[game]["pinned"] = True
        else:
            main.games[game]["pinned"] = False
        with open(vars.GAME_PATH, "wt") as f:
            json.dump(main.games, f)
        redraw()


def open_ui():
    global status_label, app, exited, exit_button, exit_triggered

    exited = False
    exit_triggered = False

    app = customtkinter.CTk(className="easy-game-launcher")

    app.title("Easy Game Launcher")
    app.geometry("500x550")
    app.protocol("WM_DELETE_WINDOW", win_quit)
    app.wm_protocol("WM_DELETE_WINDOW", win_quit)

    icon = tkinter.PhotoImage(file="icon.png")
    app.wm_iconphoto(True, icon)

    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=1)

    draw()
