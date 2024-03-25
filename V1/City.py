class City:
    def __init__(self, name, x, y):
        self.name = str(name)
        self.x = x
        self.y = y

    def toString(self):
        return ("Name :" + str(self.name) + "| x :"+ str(self.x) + "| y :" + str(self.y))
