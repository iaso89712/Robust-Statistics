'''
TABLE 2.2

In this code we extract data from a file containing information on the
temperature at the JCMB building in Edinburgh every 15 minutes in the
year 2012, storing the average for each day in a list. We create a 
second list with the same data, as well as 8 extra data points, 
representing the temperature for a heatwave experienced in the UK. 
Three estimators of location were applied to each of these data sets,
and the results, as well as the difference between them were plotted in
a table.


'''



import numpy as np
from numpy import random
from scipy.stats.mstats import winsorize


# A function which takes a data set and scale and uses the median
# and IQR to create bounds, returning the Winsorized data set
def winsorize(data, scale):
    median = np.median(data)
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1

    cminus = median - scale*IQR
    cplus = median + scale*IQR

    for i in range(len(data)):
        if data[i] < cminus:
            data[i] = cminus
        if data[i] > cplus:
            data[i] = cplus    

    return data


# Access the file in read only mode (from my files)
f = open("C:\\Users\\gabri\\Downloads\\JCMB_2012.csv","r")


# We will store the mean of the temperature for each day
day_means = []

day = "2012/01/01"
day_store = []
# Extract the data from the file into the list
k = f.readlines()
for line in k[1:]:
    line_split = line.split(",")
    day_split = line_split[0].split(" ")
    #print()
    if day_split[0] == day:
        day_store.append(float(line_split[5]))
    else:
        #print(day)
        day_means.append((sum(day_store)/(len(day_store))))
        day_store = []
        day = day_split[0]


# The additional heatwave data
heatwave = [31, 27, 24, 25, 29, 31, 37, 40]

# Print out the results
print('REGULAR')
print(np.mean(day_means))
print(np.median(day_means))
wins = winsorize(np.array(day_means), 1.7)

print(np.mean(wins))

# Combine the two data sets
for i in heatwave:
    day_means.append(i)

print('HEATWAVE ADDED')
print(np.mean(day_means))
print(np.median(day_means))

wins = winsorize(np.array(day_means), 1.7)

print(np.mean(wins))