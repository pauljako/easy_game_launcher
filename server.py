import requests
import main
import session
import tick

SESSION_KEY: str = None
FRIENDS_LIST: dict[str, str] = None

def get_session_key() -> str | None:
    global SESSION_KEY
    if ("server_url" not in main.account) or ("name" not in main.account) or ("password" not in main.account):
        return None
    server_url = main.account["server_url"]
    username = main.account["name"]
    password = main.account["password"]
    try:
        req = requests.get(f"{server_url}/api/authenticate?username={username}&password={password}")
    except Exception as err:
        print(f"[ Server | Error ] Error occured while trying to get the session key: {str(err)}")
        return
    if req.status_code != 200:
        print(f"[ Server | Error ] Error occured while trying to get the session key: server returned status code {req.status_code}")
        return None
    data = req.json()
    if data["status"] != "success":
        print(f"[ Server | Error ] Error occured while trying to get the session key: {data['error']}")
        return None
    SESSION_KEY = data["session_key"]
    return data["session_key"]

@tick.on_tick(80, 1000)
def get_friends() -> dict[str, str] | None:
    global SESSION_KEY, FRIENDS_LIST
    if SESSION_KEY is None:
        return None
    server_url = main.account["server_url"]
    try:
        req = requests.get(f"{server_url}/api/get-friends?session_key={SESSION_KEY}")
    except Exception as err:
        print(f"[ Server | Error ] Error occured while trying to get friends: {str(err)}")
        return
    if req.status_code != 200:
        if req.status_code != 200:
            print(f"[ Server | Error ] Error occured while trying to get friends: server returned status code {req.status_code}")
        return FRIENDS_LIST
    data = req.json()
    if data["status"] != "success":
        print(f"[ Server | Error ] Error occured while trying to get friends: {data['error']}")
        if data["error"] == "invalid session key" or data["error"] == "session key expired":
            get_session_key()
        return FRIENDS_LIST
    FRIENDS_LIST = data["friends"]
    main.account["friends"] = FRIENDS_LIST.keys()
    return FRIENDS_LIST

@tick.on_tick(81, 1000)
def update_status():
    global SESSION_KEY
    if SESSION_KEY is None:
        return
    server_url = main.account["server_url"]
    status = session.get_status()
    try:
        req = requests.get(f"{server_url}/api/update-status?session_key={SESSION_KEY}&status={status}")
    except Exception as err:
        print(f"[ Server | Error ] Error occured while trying to update the status: {str(err)}")
        return
    if req.status_code != 200:
        print(f"[ Server | Error ] Error occured while trying to update the status: server returned status code {req.status_code}")
        return
    data = req.json()
    if data["status"] != "success":
        print(f"[ Server | Error ] Error occured while trying to update the status: {data['error']}")
