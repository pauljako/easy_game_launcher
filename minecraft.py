import json
import minecraft_launcher_lib
import webbrowser
import flask
import multiprocessing

import session
import vars
import main

def authenticate() -> None | dict:
    if "minecraft" in main.account and "client_id" in main.account["minecraft"] and "refresh_token" in main.account["minecraft"]:
        try:
            if vars.VERBOSE:
                print("[ Minecraft | Info ] Trying to login with refresh token")
            login_info = minecraft_launcher_lib.microsoft_account.complete_refresh(main.account["minecraft"]["client_id"], None, vars.MC_REDIRECT_URI, main.account["minecraft"]["refresh_token"])
            return login_info
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

        auth_code = get_auth_code()

        try:
            login_response = minecraft_launcher_lib.microsoft_account.complete_login(main.account["minecraft"]["client_id"], None, vars.MC_REDIRECT_URI, auth_code, None)
        except Exception as e:
            print(f"[ Minecraft | Error ] Failed to complete login: {e}")
            return None

        main.account["minecraft"]["refresh_token"] = login_response["refresh_token"]
        with open(vars.ACCOUNT_PATH, "wt") as f:
            json.dump(main.account, f)

        return login_response

def flask_webserver(queue: multiprocessing.Queue):
    app = flask.Flask(__name__)

    @app.route("/callback")
    def callback():
        auth_code = flask.request.args.get("code", default="", type=str)
        if auth_code != "":
            queue.put(auth_code)
            return "Authenticated!"
        return "An error occurred"

    app.run(vars.MC_REDIRECT_HOST, vars.MC_REDIRECT_PORT)

def get_auth_code():
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=flask_webserver, args=(q,))
    p.start()
    if vars.VERBOSE:
        print(f"[ Minecraft | Info ] Waiting for callback on {vars.MC_REDIRECT_URI}")
    code = q.get(block=True)
    p.terminate()
    if vars.VERBOSE:
        print(f"[ Minecraft | Info ] Code received: {code}")
    return code

def get_command(instance_directory: str, version: str, offline: bool = False, java_bin: str | None = None):

    minecraft_launcher_lib.install.install_minecraft_version(version, instance_directory)

    if offline:
        launch_options = minecraft_launcher_lib.utils.generate_test_options()
    else:
        launch_options = authenticate()

    if java_bin is not None:
        launch_options["executablePath"] = java_bin

    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, instance_directory, launch_options)
    return minecraft_command
