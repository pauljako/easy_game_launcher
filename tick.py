import os.path
import threading

import dill

import vars

tick_objs: dict = {}
ticks_ago: int = 0


def get_tick_objs() -> dict:
    global tick_objs
    data = tick_objs
    if not isinstance(data, dict):
        return {}
    return data


def add_tick_obj(id: str, every: str, func):
    global tick_objs
    objs = get_tick_objs()
    if every not in objs:
        objs[every] = {}
    objs[every][id] = func
    tick_objs = objs


def on_tick(id: int, every: int):
    def decorator(function):

        add_tick_obj(str(id), str(every), function)

        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            return result
        return wrapper
    return decorator


def tick():
    global ticks_ago
    objs = get_tick_objs()
    for every in objs.keys():
        if ticks_ago % int(every) == 0:
            for id in objs[every].keys():
                func = objs[every][id]
                if vars.VERBOSE:
                    # print("[ Tick | Info ] Running " + id)
                    pass
                func()
    ticks_ago += 1
