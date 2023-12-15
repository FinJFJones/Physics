import physics as ph
import time

myEnv = ph.simEnvironment([ph.Object(5, (0, 0), (0, 0), vectors=[ph.Vector((1, 1))])], [ph.Vector((0, -9.8))])
for i in range(30):
    print(f'------------------\n{i}\n')
    print(myEnv)
    myEnv.timeStep(1)
    time.sleep(1)
