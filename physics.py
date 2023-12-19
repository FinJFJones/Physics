import math
from graphics import *

class screen:
    def __init__(self, environment):
        self.__environment = environment
        self.__window = GraphWin(title='Physics Sim', width=1000, height=800)

    def getEnvironment(self):
        return self.__environment

    def step(self, timeJump=1):
        self.clear()
        for object in self.__environment.getObjects():
            object.updateShape()
            object.getShape().draw(self.__window)
        self.__environment.timeStep(timeJump)

    def clear(self):
        for item in self.__window.items[:]:
            item.undraw()
        self.__window.update()

    def draw(self, resolution, duration):
        for i in range(int(round(duration/(1/resolution)))):
            print(f'------------------\nStep: {i}\n')
            print(self.__environment)
            self.step(1/resolution)
            time.sleep(1/resolution)
        self.__window.getMouse()
        self.__window.close()

class simEnvironment:
    def __init__(self, objects, globalForces, dimensions=2) -> None:
        self.__dimensions = dimensions
        self.__globalForces = globalForces
        self.calcGlobalResultantForces()
        for object in objects:
            object.changeParent(self)
        self.__objects = objects
        for force in globalForces:
            force.changeParent(self)
 
    def __str__(self) -> str:
        objectCoords = 'Object Coordinates:\n'
        for i in range(len(self.__objects)):
            objectCoords += f' {i+1}. {[round(objectFlo, 4) for objectFlo in self.__objects[i].getCoordinates()]}\n'
        return objectCoords
 
    def getDimensions(self):
        return self.__dimensions
   
    def getGlobalForce(self):
        return self.__globalResultantForces
    
    def getObjects(self):
        return self.__objects
   
    def calcGlobalResultantForces(self):
        self.__globalResultantForces = Vector([0 for i in range(self.__dimensions)], isPersistant=True, parentObject=self)
        for force in self.__globalForces:
            self.__globalResultantForces = self.__globalResultantForces.addVector(force)
 
    def timeStep(self, timeJump=1):
        for object in self.__objects:
            object.timeStep(timeJump)
 
class Object:
    def __init__(self, mass, coordinates, measurements, environment=None, vectors=[]) -> None:
        if environment != None and len(coordinates) != environment.__dimensions:
            raise Exception('Wrong number of dimensions.')
        else:
            self.__coordinates = coordinates
        for vector in vectors:
            vector.changeParent(self)
        self.__vectors = vectors
        self.__mass = mass
        self.__measurements = measurements
        self.__environment = environment
        self.__velocity = None
        self.__shape = None
 
    def addVector(self, vector):
        self.__vectors.append(vector)
 
    def removeVector(self):
        menu = 'Select a vector to be removed:\n'
        for i in range(len(self.__vectors)):
            menu += f' {i+1}. {self.__vectors[i]}\n'
        menu += ' X. Cancel'
        userInput = None
        inputs = range(len(self.__vectors)).append('x')
        while userInput.lower() not in inputs:
            userInput = input(menu)
        if userInput != 'X':
            del self.__vectors[int(userInput)]
   
    def initVelocity(self):
        self.__velocity = Vector([0 for i in range(self.__environment.getDimensions())], isPersistant=True, parentObject=self)
        for vector in self.__vectors:
            self.__velocity = self.__velocity.addVector(vector)
           
        for i in range(len(self.__vectors)-1, -1, -1):
            if not self.__vectors[i].getIsPersistant():
                del self.__vectors[i]
 
    def changeParent(self, newParent):
        self.__environment = newParent
        self.initVelocity()
 
    def getCoordinates(self):
        return self.__coordinates
    
    def getShape(self):
        return self.__shape
    
    def updateShape(self):
        self.__shape = Circle(Point(self.__coordinates[0], self.__coordinates[1]), 2)
 
    def timeStep(self, timeJump):
        newCoords = list(self.__coordinates)
        for i in range(self.__environment.getDimensions()):
            newCoords[i] += (self.__velocity.getForces()[i]*timeJump)+((1/2)*(self.__environment.getGlobalForce().getForces()[i])*(timeJump**2))
        self.__coordinates = tuple(newCoords)
        for i in range(self.__environment.getDimensions()):
            self.__velocity.setForce(i, (self.__velocity.getForces()[i]+(self.__environment.getGlobalForce().getForces()[i]*timeJump)))

#class Particle(Object):
#    def __init__(self, mass, coordinates, environment=None, vectors=[]) -> None:
#        super().__init__(mass, coordinates, None if environment==None else tuple(0 for i in range(environment.getDimensions())), environment, vectors)
#    
#    def changeParent(self, newParent):
#        self.__environment = newParent
#        self.__measurements = tuple(0 for i in range(self.__environment.getDimensions()))
 
class Vector:
    def __init__(self, componentForces, isPersistant=False, parentObject=None) -> None:
        self.__componentForces = componentForces
        self.__isPersistant = isPersistant
        self.__parentObject = parentObject
 
    def __str__(self) -> str:
        return self.__componentForces
   
    def addVector(self, additionalVector):
        try:
            newVector = []
            for i in range(len(self.__componentForces)):
                newVector.append(self.__componentForces[i]+additionalVector.__componentForces[i])
            return Vector(newVector, isPersistant=self.__isPersistant, parentObject=self.__parentObject)
        except:
            raise Exception('Adding these vectors have failed, ensure both have the same number of dimensions and both have dimensions consisting of only floats.')
       
    def changeParent(self, newParent):
        self.__parentObject = newParent
 
    def setForce(self, dimension, value):
        self.__componentForces[dimension] = value
       
    def getForces(self):
        return self.__componentForces
   
    def getIsPersistant(self):
        return self.__isPersistant
