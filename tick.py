import os.path
import threading

import dill

import vars

tick_objs: dict = {}


def get_tick_objs() -> dict:
    global tick_objs
    data = tick_objs
    if not isinstance(data, dict):
        return {}
    return data


def add_tick_obj(id: str, func):
    global tick_objs
    objs = get_tick_objs()
    objs[id] = func
    tick_objs = objs


def on_tick(id: int):
    def decorator(function):

        add_tick_obj(str(id), function)

        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            return result
        return wrapper
    return decorator


def tick():
    objs = get_tick_objs()
    for id in objs:
        func = objs[id]
        if vars.VERBOSE:
            # print("[ Tick | Info ] Running " + id)
            pass
        func()
