from reqrep import Client
from MyServer import MyServer

from multiprocessing import Process
from threading import Thread

class MyClient(Client):
    def __init__(self, host, port, wraps = MyServer, verbose=True):
        super().__init__(host, port, wraps = wraps, verbose=verbose)


if __name__ == "__main__":
    c = MyClient('localhost', 3030)