class City :
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = str(name)

    def toString(self):
        return ("x : "+ str(self.x) + " | y : " + str(self.y) + " | Name : " + str(self.name) + "\n")

    