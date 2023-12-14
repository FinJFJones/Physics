class simEnvironment:
    def __init__(self, objects, globalForces, dimensions=2) -> None:
        for object in objects:
            object.changeParent(self)
        self.__objects = objects
        for force in globalForces:
            force.changeParent(self)
        self.__globalForces = globalForces
        self.__dimensions = dimensions

    def __str__(self) -> str:
        objectCoords = 'Object Coordinates:\n'
        for i in range(len(self.__objects)):
            objectCoords += f' {i+1}. {self.__objects[i].getCoordinates()}\n'

    def getDimensions(self):
        return self.__dimensions

    def timeStep(self, timeJump=1):
        for object in self.__objects:
            object.timeStep(timeJump)

class Object:
    def __init__(self, mass, coordinates, measurements, environment=None, vectors=[]) -> None:
        if len(coordinates) != environment.__dimensions:
            raise Exception('Wrong number of dimensions.')
        else:
            self.__coordinates = coordinates
        for vector in vectors:
            vector.changeParent(self)
        self.__vectors = vectors
        self.__mass = mass
        self.__measurements = measurements
        self.__environment = environment
        self.calculateResultantForce()

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
    
    def calculateResultantForce(self):
        resultantForce = [0 for i in range(self.__environment.getDimensions())]
        for i in range(self.__environment.getDimensions()):
            for vector in self.__vectors:
                resultantForce[i] += vector[i]
        self.__resultantForce = resultantForce

    def changeParent(self, newParent):
        self.__environment = newParent

    def getCoordinates(self):
        return self.__coordinates

    def timeStep(self, timeJump):
        for i in range(self.__environment.getDimensions()):
            for vector in self.__vectors:
                self.__coordinates[i] += vector.getForces[i]/timeJump


class Particle(Object):
    def __init__(self, mass, coordinates, environment=None, vectors=[]) -> None:
        super().__init__(mass, coordinates, tuple(0 for i in range(environment.getDimensions())), environment, vectors)

class Vector:
    def __init__(self, componentForces, parentObject=None) -> None:
        self.__componentForces = componentForces
        self.__parentObject = parentObject

    def __str__(self) -> str:
        return self.__componentForces
    
    #def addVector(self, additionalVector):
    #    try:
    #        newVector = []
    #        for i in range(self.__componentForces):
    #            newVector.append(self.__componentForces[i]+additionalVector.__componentForces[i])
    #        return tuple(newVector)
    #    except:
    #        raise Exception('Adding these vectors have failed, ensure both have the same number of dimensions and both have dimensions consisting of only floats.')
        
    def changeParent(self, newParent):
        self.__parentObject = newParent
        
    def getForces(self):
        return self.__componentForces