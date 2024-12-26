import threading
import time

import messages
import session
import tick
import socket

import vars

HOST = "127.0.0.1"
CURRENT_HANDLED_THREAD: threading.Thread = None

connection: socket.socket = None

def handle():
    global connection
    if connection is not None:
        try:
            data = connection.recv(4096)

            if not data:
                disconnect()
            else:
                received_data: list[str] = data.decode().replace("\n", "").replace("\r", "").split(vars.EGA_SEPERATOR)
                if vars.VERBOSE:
                    print(f"[ EGA | Info ] Received: {received_data}")
                answer = vars.EGA_SEPERATOR.join(messages.process_ega_messages(received_data)) + "\r"
                connection.sendall(answer.encode())

        except:
            print("[ EGA | Error ] Error receiving Data")
            disconnect()

@tick.on_tick(61, 3)
def handle_threaded():
    global CURRENT_HANDLED_THREAD
    if CURRENT_HANDLED_THREAD is not None and CURRENT_HANDLED_THREAD.is_alive():
        return
    CURRENT_HANDLED_THREAD = threading.Thread(target=handle, daemon=True)
    CURRENT_HANDLED_THREAD.start()

def connect():
    global connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, vars.EGA_PORT))
    sock.listen()
    if vars.VERBOSE:
        print(f"[ EGA | Info ] Listening on Port {vars.EGA_PORT}")
    connection, addr = sock.accept()


def disconnect():
    global connection
    if connection is not None:
        connection.close()
        connection = None
        print("[ EGA | Error ] Disconnected")
        if session.get_session() is not None:
            session.exit_session()
        else:
            print("[ EGA | Error ] Session already Exited")


def start_connect_thread():
    if connection is None:
        connect()


def start_handle_thread():
    time_started = int(time.time())
    thread = threading.Thread(target=start_connect_thread, daemon=True)
    thread.start()
    while connection is None:
        if not thread.is_alive():
            break
        elif int(time.time()) - time_started > 60:
            print("[ EGA | Error ] Connection Timeout")
            disconnect()
            break

def start():
    handle_thread = threading.Thread(target=start_handle_thread, daemon=True)
    handle_thread.start()
