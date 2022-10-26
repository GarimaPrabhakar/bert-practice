import pygimli as pg
import pybert as pb
import numpy as np

def createSensorArray(inits, deltas, num_electrodes = 25, num_rows=5):
    p = pg.core.R3Vector(num_electrodes)
    #p = pg.core.RVector(2)
    xinit = inits[0]
    yinit = inits[1]
    zinit = inits[2]

    dx = deltas[0]
    dy = deltas[1]
    
    for i in range(num_electrodes): 
        col = i%num_rows
        row = (i - col)/num_rows

        p[i] = [col*dx + xinit, row*dy + yinit]
        
    return p


p = createSensorArray([-10, -10, 0], [5, 5])

#create a scheme
scheme = pb.createData(elecs=p,
                       schemeName='dd')

x = []
y = []

for n in p:
    x.append(n[0])
    y.append(n[1])

print(scheme)
scheme.save("scheme3d.shm")
