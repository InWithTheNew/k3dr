class MyRandomModule:
    def __init__(self):
        self.me = "Hello"

    def PrintModuleName(self):
        return __name__
    
    if __name__ == "__main__":
        def PrintModuleName(self):
            print(__name__)

p = MyRandomModule()
p.PrintModuleName()