import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import spline
import numpy as np

data = np.genfromtxt("data_samples_error_iter0.csv",delimiter=",")
data2 = np.genfromtxt("data_samples_error_iter50.csv",delimiter=",")
data3 = np.genfromtxt("data_samples_error_iter98.csv",delimiter=",")
data4 = np.genfromtxt("data_samples_error_iter25.csv",delimiter=",")
X = data[:,0]
Y = data[:,1]
#Z = data[:,2]
X2 = data2[:,0]
Y2 = data2[:,1]
X3 = data3[:,0]
Y3 = data3[:,1]


#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.contour(X, Y, Z)
plt.plot(X,Y,X2,Y2,X3,Y3, linewidth=2.0)
plt.show()