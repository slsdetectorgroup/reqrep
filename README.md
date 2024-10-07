# reqrep
Simple zmq/json remote interface

### Installation

```bash
conda install reqrep -c slsdetectorgroup
```

### Implementing the server
```python
from reqrep import Server

class MyServer(Server):
    def __init__(self, port):
        #Initialize any instance variables
        #self._value = 7
        super().__init__(port)

    #Implement your functions
    def do_something(self):
        ...

```

### Implementing the client

```python
from reqrep import Client

class MyClient(Client):
    def __init__(self, host, port, wraps = MyServer, verbose=False):
        super().__init__(host, port, wraps = wraps, verbose=verbose)


```
