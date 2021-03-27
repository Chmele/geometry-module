class testClass:
    def __init__(self, n):
        self.N = n

def changeList(l):
    l.append(0)

l = [1, 2, 4]
changeList(l)
print(l)


