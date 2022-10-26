import vtk
import csv
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk
import numpy as np
import pandas as pd
# import sys


# inFile = sys.argv[1]
# outFile = sys.argv[2]

fileIn  = 'test.vtk'
fileOut  = 'output.csv'

reader = vtk.vtkUnstructuredGridReader()
reader.SetFileName('test.vtk')
reader.ReadAllScalarsOn()
reader.ReadAllVectorsOn()
reader.Update()

point_obj = reader.GetOutput()

#point_obj = ptdata
converter = vtk.vtkCellDataToPointData()
converter.ProcessAllArraysOn()
converter.SetInputConnection(reader.GetOutputPort())
converter.Update()
arr = vtk_to_numpy(converter.GetOutput().GetPointData().GetArray('Resistivity/Ohmm'))

points = np.array([(point_obj.GetPoint(i)[0], point_obj.GetPoint(i)[1], point_obj.GetPoint(i)[2], arr[i]) for i in range(int(point_obj.GetNumberOfPoints()))])

# Set markers for each point. Hard code for now, but figure out a way to do this from rho.map
rho_map = [5, 100]
layer = -5
marker = []
for i in range(len(points)):
    if points[i][2] < layer:
        marker.append(rho_map[1])
    elif points[i][2]>=layer:
        marker.append(rho_map[0])
    else:
        print("something's wrong getting markers for csv")
        marker.append('nan')

marker = np.reshape(np.array(marker), (len(marker), 1))
markered_points = np.concatenate((points, marker), 1)

df = pd.DataFrame(markered_points)
df.columns = ["x", "y", "z", "Resistivity/Ohmm", "Marker"]

df.to_csv("test.csv", index=False)