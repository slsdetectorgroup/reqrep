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
    
    def getSomeList(self):
        return [1, 'two', 3]
    
    def getSomeDict(self):
        return {'one': 1, 'two': 2, 'three': 3}
    
    def raiseException(self):
        raise ValueError("This is an exception")
    
    @property
    def filter_thickness(self):
        return self._ft
    
    @filter_thickness.setter
    def filter_thickness(self, val):
        self.setFilterThickness(val)
        

if __name__ == "__main__":
    s = MyServer(3030)
