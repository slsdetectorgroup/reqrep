import zmq
import json
from rich import print
from functools import partial
from . import common as cm

class Client:
    def __init__(self, host, port, wraps, verbose = True):
        self.host = host
        self.port = port
        self.verbose = verbose
        self._commands = [it for it in dir(wraps) if callable(getattr(wraps, it)) and not it.startswith('_')]
        self._members = [it for it in dir(wraps) if not callable(getattr(wraps, it)) and not it.startswith('_')]
        
        if self.verbose:
            print(f"Client for {wraps.__name__} at {self.host}:{self.port}")

    def __setattr__(self, name, value):
        if name in ['host', 'port', 'verbose', '_commands', '_members']:
            self.__dict__[name] = value
        else:
            self._send_message(name, value)

    def __getattr__(self, name):
        if name in self._commands:
            return partial(self._send_message, name)
        elif name in self._members:
            if self.ping():
                return self._send_message(name)
            else:
                raise TimeoutError(f"Timeout while waiting for reply from {self.host}:{self.port}")
        else:
            return self.__getattribute__(name)
        
    def ping(self):
        try:
            return self._send_message('ping', timeout_ms=100) == 'pong'
        except TimeoutError:
            return False
    
    def __dir__(self):
        return self._commands + self._members
    
    def _send_message(self, cmd, *args, timeout_ms = -1):
        cmd = cmd.encode(cm.encoding)
        args = json.dumps(args).encode(cm.encoding)
        if self.verbose:
            print(f'[spring_green4]{cm.now()} - REQ: {cmd}, {args}[/spring_green4]')

        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.setsockopt(zmq.SNDTIMEO, timeout_ms)
        socket.setsockopt(zmq.RCVTIMEO, timeout_ms)
        socket.setsockopt(zmq.LINGER, 0)
        socket.connect(f"tcp://{self.host}:{self.port}")

        try:
            socket.send_multipart([cmd, args])
            reply = socket.recv_multipart()
            status, message = self._decode_reply(reply)
            if self.verbose:
                print(f'[dark_orange3]{cm.now()} - REP: {status}:{message}[/dark_orange3]')
            self._check_error(status, message)
        
        except zmq.error.Again:
            raise TimeoutError(f"Timeout while waiting for reply from {self.host}:{self.port}")
        
        finally:
            socket.disconnect(f"tcp://{self.host}:{self.port}")
            context.destroy()
        
        return message
    
    def _decode_reply(self, reply):
        return (json.loads(r) for r in reply)
  
    def _check_error(self, status, message):
        if status != cm.STATUS_OK:
            raise ValueError(f"Unexpected reply: {status}:{message}")
        
    