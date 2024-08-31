from reqrep import Server

class MyServer(Server):
    def __init__(self, port):
        self._ft = 0.0
        super().__init__(port)
        

    def closeShutter(self):
        print("Closing shutter")
        return
    
    def setFilterThickness(self, val):
        print(f"Setting filter thickness to {val}um")
        self._ft = val
        return
    
    def getFilterThickness(self):
        return self._ft

if __name__ == "__main__":
    s = MyServer(3030)
