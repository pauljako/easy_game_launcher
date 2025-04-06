import json
import minecraft_launcher_lib
import main
import vars
import webbrowser
import flask
import multiprocessing

def authenticate() -> None | dict:
    if "minecraft" in main.account and "client_id" in main.account["minecraft"] and "refresh_token" in main.account["minecraft"]:
        try:
            minecraft_launcher_lib.microsoft_account.complete_refresh(main.account["minecraft"]["client_id"], None, vars.MC_REDIRECT_URI, main.account["minecraft"]["refresh_token"])
        except Exception as e:
            print(f"[ Minecraft | Error ] Failed to login with refresh token: {e}")
            main.account["minecraft"].pop("refresh_token")
            with open(vars.ACCOUNT_PATH, "wt") as f:
                json.dump(main.account, f)
            return None

    elif "minecraft" in main.account and "client_id" in main.account["minecraft"]:
        try:
            login_url = minecraft_launcher_lib.microsoft_account.get_login_url(main.account["minecraft"]["client_id"], vars.MC_REDIRECT_URI)
        except Exception as e:
            print(f"[ Minecraft | Error ] Failed to get url for auth token: {e}")
            return None

        if vars.VERBOSE:
            print(f"[ Minecraft | Info ] Login on {login_url}")
            webbrowser.open(login_url)

def start_web_server():
    app = flask.Flask(__name__)

    @app.route("/callback")
    def callback():
        auth_code = flask.request.args.get("code", default="", type=str)
        if auth_code is not "":
            return "Authenticated!"
        else:
            return "An error occurred"

    server = multiprocessing.Process(target=app.run, args=(vars.MC_REDIRECT_HOST, vars.MC_REDIRECT_PORT), daemon=True)
    server.start()
