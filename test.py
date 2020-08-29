import matplotlib.pyplot as plt
import numpy as np

a = 1
b = 2

for i in np.linspace(0,2*np.pi,180):
    r = np.sqrt((a*np.sin(i))**2 + (b*np.cos(i))**2)

    x = r*np.cos(i)
    y = r*np.sin(i)

    plt.scatter(x,y)

    x = 1*np.cos(i)
    y = 1*np.sin(i)

    plt.scatter(x,y)


    x = 2*np.cos(i)
    y = 2*np.sin(i)

    plt.scatter(x,y)


plt.show()

    