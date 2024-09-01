import zmq
import sys
import json
from rich import print

from . import common as cm



class Server:
    def __init__(self, port):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        endpoint = "tcp://*:{}".format(port)
        print("{} - TEMServer binding to {} ".format(cm.now(), endpoint))
        self.socket.bind(endpoint)

        #Find all commands
        self._commands = [it for it in dir(self) if callable(getattr(self, it)) and not it.startswith('_')]
        self._members = [it for it in dir(self) if not callable(getattr(self, it)) and not it.startswith('_')]

        self._run()

    def _has_function(self, cmd):
        return cmd in self._commands
    
    def _has_member(self, member):
        return member in self._members
    
    def exit_server(self):
        """
        Function is here to appear on the list of commands. Logic for exiting the server is in the _run method
        """
        return "Server is exiting"
    
    def ping(self):
        return "pong"

    def _run(self):
        while True:
            msgs = self.socket.recv_multipart()
            
            #If we didn't get two messages something is really wrong so lets 
            #just exit and debug the caller
            if len(msgs) != 2:
                print("TEMServer got: {} messages. Should always be 2 -> EXIT".format(len(msgs)))
                sys.exit(1)
            cmd = msgs[0].decode(cm.encoding)
            args = json.loads(msgs[1].decode(cm.encoding))
            print("{} - REQ: {}, {}".format(cm.now(), cmd, args))

            if self._has_function(cmd):
                # if the function in found we try to call it
                try:
                    res = getattr(self, cmd)(*args)
                    rc = cm.STATUS_OK
                except Exception as e:
                    rc = cm.STATUS_ERROR
                    res = "Exception occurred when calling: {}. Error message: {}".format(cmd, e)
            elif self._has_member(cmd):
                #Check if we should set or get
                if len(args) == 0:
                    #If no arguments we assume we want to get the value
                    res = getattr(self, cmd)
                    rc = cm.STATUS_OK
                else:
                    #If we have arguments we assume we want to set the value
                    try:
                        setattr(self, cmd, args[0])
                        res = "OK"
                        rc = cm.STATUS_OK
                    except Exception as e:
                        rc = cm.STATUS_ERROR
                        res = "Exception occurred when setting: {}. Error message: {}".format(cmd, e)
            else:
                #Otherwise we return an error
                rc = cm.STATUS_ERROR
                res = "Function: {} not implemented".format(cmd)

            rc = json.dumps(rc).encode(cm.encoding)
            res = json.dumps(res).encode(cm.encoding)
            
            # Reply to the client
            print("{} - REP: {}, {}".format(cm.now(), rc, res))
            self.socket.send_multipart([rc, res])


            if cmd == 'exit_server':
                break
