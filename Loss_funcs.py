'''
FIGURE 2.4

In this code we write functions for and plot squared loss, absolute
loss, Huber loss and Tukey loss.

'''


import numpy as np
import matplotlib.pyplot as plt

#Squared loss function
def squared_loss(x):
    return x ** 2

#Absolute loss function
def absolute_loss(x):
    return np.abs(x)

#Huber loss function, with c as a parameter
def huber_loss(x, c):
    xcopy = np.copy(x)

    for i in range(len(xcopy)):
        if np.abs(xcopy[i]) <= c:
            xcopy[i] = 0.5 * x[i] ** 2
        elif np.abs(xcopy[i]) > c:
            xcopy[i] = c * (np.abs(x[i]) - 0.5 * c)
    
    return xcopy


#Tukey's loss, with c as a parameter
def tukey_loss(x, c):
    x_copy = np.copy(x)
    for i in range(len(x_copy)):
        if np.abs(x_copy[i]) <= c:
            x_copy[i] = (c ** 2 / 6) * (1 - (1 - (x[i] / c) ** 2) ** 3)
        elif np.abs(x_copy[i]) > c:
            x_copy[i] = c ** 2 / 6
    
    return x_copy


x = np.linspace(-6, 6, 400)


set_ylim = (0, 4)

# We plot all of the functions on the same graph, using multiple c parameters for Tukey's loss
plt.figure(figsize=(10, 6))
plt.plot(x, squared_loss(x), label='Squared Loss')
plt.plot(x, absolute_loss(x), label='Absolute Loss')
plt.plot(x, huber_loss(x, 1.5), label='Huber Loss (c=1.5)')
plt.plot(x, tukey_loss(x, 2), label='Tukey Loss (c=2)')
plt.plot(x, tukey_loss(x, 4), label='Tukey Loss (c=4)')

plt.xlabel('r')
plt.ylabel('Loss')
plt.title('Comparison of Loss Functions')
plt.legend()
plt.ylim(set_ylim)
plt.show()




