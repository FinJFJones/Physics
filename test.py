from physics import *
import time
 
myEnv = screen(simEnvironment([Object(5, (100, 100), (0, 0), vectors=[Vector((50, 50))]), Object(5, (100, 100), (0, 0), vectors=[Vector((25, 100))]), Object(5, (100, 100), (0, 0), vectors=[Vector((75, 25))])], [Vector((0, -9.8))], dimensions=2))
myEnv.draw(10, 100)
