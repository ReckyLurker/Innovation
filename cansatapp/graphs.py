
import numpy as np
import matplotlib.pyplot as plt
  
# initialize x and y coordinates
x = [0.1, 0.2, 0.3, 0.8, 0.6]
y = [6.2, -8.4, 8.5, 9.3, -3.6]
  
# set the title of a plot
plt.title("Tilt_y")
  
# plot scatter plot with x and y data
plt.scatter(x, y)
  
# plot with x and y data
plt.plot(x, y)


plt.savefig("test.png")
plt.show()

#Code for the reference
