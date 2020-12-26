class Claster(object):

    def __init__(self,centerPoint,points):
        self.centerPoint=centerPoint
        self.points=points
    def setCenter(self,newCenter):
        self.centerPoint=newCenter
    def addPoint(self,x,y):
        self.points[x]=y
d=dict()
b=dict()
d["a"]={'dict': 1, 'dictionary': 2}
b["f"]={'dict': 1, 'dictionary': 2}
print(d.values()==b.values())
