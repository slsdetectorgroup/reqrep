from reqrep import Client
from MyServer import MyServer


class MyClient(Client):
    def __init__(self, host, port, wraps = MyServer, verbose=False):
        super().__init__(host, port, wraps = wraps, verbose=verbose)


if __name__ == "__main__":
    c = MyClient('localhost', 3030)
