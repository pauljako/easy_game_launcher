import socket

SEPERATOR = ":-:"
PORT = 45432
VERBOSE = False


class Connection(socket.socket):

    def __init__(self, connect: bool = True):
        super().__init__()
        self.connected = False
        if connect:
            self.reconnect()

    def reconnect(self):
        super().connect(("127.0.0.1", PORT))
        self.connected = True

    def disconnect(self):
        self.close()
        self.connected = False

    def is_connected(self) -> bool:
        return self.connected

    def add_achievement(self, name: str, description: str) -> list[str]:
        data = f"achievement{SEPERATOR}{name}{SEPERATOR}{description}"
        self.sendall(data.encode())
        return self.receive()

    def receive(self) -> list[str]:
        try:
            data = self.recv(4096)

            if not data:
                self.disconnect()
            else:
                received_data: list[str] = data.decode().replace("\n", "").replace("\r", "").split(SEPERATOR)
                if VERBOSE:
                    print(f"[ EGA | Info ] Received: {received_data}")
                return received_data

        except:
            if VERBOSE:
                print("[ EGA | Error ] Error receiving Data")
            self.disconnect()



