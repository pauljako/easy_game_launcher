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
    req = requests.get(f"{server_url}/api/authenticate?username={username}&password={password}")
    if req.status_code != 200:
        return None
    data = req.json()
    if data["status"] != "success" or data["username"] != username:
        return None
    SESSION_KEY = data["session_key"]
    return data["session_key"]

@tick.on_tick(80, 500)
def get_friends() -> dict[str, str] | None:
    global SESSION_KEY, FRIENDS_LIST
    if SESSION_KEY is None:
        return None
    server_url = main.account["server_url"]
    req = requests.get(f"{server_url}/api/get-friends?session_key={SESSION_KEY}")
    if req.status_code != 200:
        return FRIENDS_LIST
    data = req.json()
    if data["status"] != "success":
        return FRIENDS_LIST
    FRIENDS_LIST = data["friends"]
    main.account["friends"] = FRIENDS_LIST.keys()
    return FRIENDS_LIST

@tick.on_tick(81, 500)
def update_status():
    global SESSION_KEY
    if SESSION_KEY is None:
        return
    server_url = main.account["server_url"]
    status = session.get_status()
    req = requests.get(f"{server_url}/api/update-status?session_key={SESSION_KEY}&status={status}")
