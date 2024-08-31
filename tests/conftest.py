import pytest

import sys
sys.path.append('examples')
from MyServer import MyServer
from MyClient import MyClient
from threading import Thread

@pytest.fixture()
def client():
    c = MyClient('localhost', 3030)
    yield c
    c.exit_server()

@pytest.fixture()
def server():
    t = Thread(target=MyServer, args= (3030,))
    t.start()
    return t
