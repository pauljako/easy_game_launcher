import time

import messages
import session
import tick
import socket

import vars

HOST = "127.0.0.1"
PORT = 45432

connection: socket.socket = None


@tick.on_tick(61, 3)
def handle():
    global connection
    if connection is not None:
        try:
            data = connection.recv(4096)

            if not data:
                disconnect()
            else:
                received_data: list[str] = data.decode().split(vars.EGA_SEPERATOR)
                if vars.VERBOSE:
                    print(f"[ EGA | Info ] Received: {received_data}")
                answer = vars.EGA_SEPERATOR.join(messages.process_ega_messages(received_data))
                connection.sendall(answer.encode())

        except:
            print("[ EGA | Error ] Error receiving Data")
            disconnect()


def connect():
    global connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen()
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
