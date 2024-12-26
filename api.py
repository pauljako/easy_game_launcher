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

@tick.on_tick(61, 1)
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

def connect():
    global connection
    if connection is not None:
        print("[ EGA | Error ] Another EGA instance is already running")
        return
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(60)
    sock.bind((HOST, vars.EGA_PORT))
    sock.listen()
    if vars.VERBOSE:
        print(f"[ EGA | Info ] Listening on Port {vars.EGA_PORT}")
    try:
        connection, addr = sock.accept()
    except socket.timeout:
        print("[ EGA | Error ] Connection Timeout")


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
