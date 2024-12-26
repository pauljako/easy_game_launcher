import os.path
import threading
import time
import dill

import vars

tick_objs: dict = {}
ticks_ago: int = 0
start_second: float = round(time.time(), 2) * 100


def get_tick_objs() -> dict:
    global tick_objs
    data = tick_objs
    if not isinstance(data, dict):
        return {}
    return data


def add_tick_obj(id: str, every: int, func):
    global tick_objs
    objs = get_tick_objs()
    if every not in objs:
        objs[every] = {}
    objs[every][id] = func
    tick_objs = objs


def on_tick(id: int, every: float):
    def decorator(function):

        add_tick_obj(str(id), int(every * 100), function)

        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            return result
        return wrapper
    return decorator


def tick():
    global ticks_ago, start_second
    objs = get_tick_objs()
    for every in objs.keys():
        if ((round(time.time(), 2) * 100) - start_second) % int(every) == 0:
            for id in objs[every].keys():
                func = objs[every][id]
                if vars.VERBOSE:
                    # print("[ Tick | Info ] Running " + id)
                    pass
                start_time = round(time.time(), 2) * 100
                func()
                diff = (round(time.time(), 2) * 100) - start_time
                start_second -= diff
                if diff / 100 > 1 and vars.VERBOSE:
                    print(f"[ Tick | Warning ] Running {id} took {diff / 100} seconds")

    ticks_ago += 1
