import matplotlib.pyplot as plt
import numpy as np

y = np.random.rand(30,80,100)
z = np.random.rand(30,80,100)
x = np.arange(100)

plt.figure(0)
plt.plot(x, y, label='back')
plt.plot(x, y, label='neck')
plt.legend()
plt.ylabel('Angle')
plt.xlabel('Time')
