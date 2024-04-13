import os.path

import dill

import vars


def get_tick_objs() -> dict:
    if not os.path.exists(vars.TICK_OBJ_PATH):
        return {}
    with open(vars.TICK_OBJ_PATH, "rb") as f:
        data = dill.load(f)
    if not isinstance(data, dict):
        return {}
    return data


def add_tick_obj(id: str, func):
    objs = get_tick_objs()
    objs[id] = func
    with open(vars.TICK_OBJ_PATH, "wb") as f:
        dill.dump(objs, f)


def on_tick(id: int):
    def decorator(function):

        add_tick_obj(str(id), function)

        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            return result
        return wrapper
    return decorator


def tick():
    while True:
        objs = get_tick_objs()
        for id, func in objs.values():
            if vars.VERBOSE:
                print("Running " + id)
            func()


print(get_tick_objs())


@on_tick(0)
def say_hi():
    print("hi")


print(get_tick_objs())

say_hi()
