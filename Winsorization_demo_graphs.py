'''
FIGURE 2.3

In this code we define a Winsorization function, and then apply it to two data sets,
one with corruption, and one without. We then plot each of these on seperate graphs 
against the original values to show how the two data sets are affected differently.

'''



import numpy as np
import random
import matplotlib.pyplot as plt

# This is out uncorrupted data which we will use
OGdata = np.random.normal(loc=0, scale=1, size=200)

# The corrupt data is the original data as well as a single corrupt point
OGdata_with_corrupt = np.concatenate((OGdata, [5]))


# Here we define a winsorization function which uses the median and IQR to
# construct Winsorization bounds. It takes as as input a data set, and returns
# the winsorized data set, as well as a list of colours where shifted points
# are red, and unshifted points are blue.
def winsorize(data):
    
    # Find the median and IQR
    median = np.median(data)
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1

    #Construct our bounds
    cminus = median - 1.5*IQR
    cplus = median + 1.5*IQR

    #Make a copy of the data, and make a list of the colours
    shifted_data = np.copy(data)
    colors = ['blue'] * len(data)

    # Shift data points outside of the bounds, and make them red
    for i in range(len(shifted_data)):
        if shifted_data[i] < cminus:
            shifted_data[i] = cminus
            colors[i] = 'red'
        if shifted_data[i] > cplus:
            shifted_data[i] = cplus
            colors[i] = 'red'

    return shifted_data, colors

# Apply the Winsorization function to both of our data sets
shifted_data, colors = winsorize(OGdata)
shifted_data_with_corrupt, colors_with_corrupt = winsorize(OGdata_with_corrupt)


# Plot the results, including colours to show which points have been shifted
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.scatter(OGdata, shifted_data, c=colors, label='Original vs Winsorized', marker='o')
plt.xlabel('Original Value')
plt.ylabel('Winsorized Value')
plt.title('Original Data vs Winsorized Data')

plt.subplot(1, 2, 2)
plt.scatter(OGdata_with_corrupt, shifted_data_with_corrupt, c=colors_with_corrupt, marker='o')
plt.xlabel('Original Value')
plt.ylabel('Winsorized Value')
plt.title('Original Data vs Winsorized Data with Corrupt Point')

plt.tight_layout()
plt.show()