#Empty print for not disturbing the unit tests output
def myPrint( str ):
    pass

def add( i,  j):
    return i + j
    
def subtract( i,  j):
    return i - j

def innerFunction():
    pass

def outerFunction():
    innerFunction()

def noParamsFunction():
    return MyClass()

def mySubstring( str,  length ):
    return str[:length]

def processList( aList ):
    myPrint( "Entered processList" )
    for elem in aList:
        myPrint ("elem: " + repr(elem) + "\n")

def processDict( aDict ):
    myPrint( "Entered processDict" )
    for elem in aDict.items():
        key,  value = elem
        myPrint( "key: " + repr(key) + "\n" )
        myPrint( "value: " + repr(value) + "\n" )
        
class MyClass:
    def f1(self):
        myPrint( "No params" )
        return self
    def f2(self, i):
        myPrint( "i:" + repr(i) )
    def f3(self, aList):
        x = aList[0]
        myPrint( "x:" + repr(x) )
    def f4(self, aDict, anObj):
        x = aDict['x']
        y = aDict['y']
        myPrint("x: " + repr(x) + ", y:" + repr(y) )
        myPrint("anObj: "  + repr(anObj))
    def f5(self, obj1, obj2):
        myPrint("obj1: " + str(obj1) + ", obj2: " + str(obj2)) 

class ClassWithDummyParameters:
    def f1(self, d):
        myPrint( "Dummy parameter" )
        
class NonAnnotatedClass:
    pass

class ClassWithConstructor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        myPrint( "No params" )
    def getX(self):
        return self.x
    def setX(self,x):
        self.x = x 
    def getY(self):
        return self.y
    def setY(self, y):
        self.y = y
        
class ClassWithStaticAndClassMethods:
    @staticmethod
    def static0():
        myPrint( "static0")
    @staticmethod
    def static1( x ):
        myPrint( "x: " + repr(x) )
    @classmethod
    def classMethod0(cls):
        myPrint( "Class is " + repr(cls) )
    @classmethod
    def classMethod1(cls,x):
        myPrint( "Class is " + repr(cls) + "x = " + str(x) )