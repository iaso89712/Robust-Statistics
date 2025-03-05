'''
TABLE 2.1

In this code, we define a number of estimators of scale: the sample standard deviation, absolute deviation,
MAD,Winsorized sample standard deviation, S_n and Q_n. These estimators are then applied to four data sets,
the first of which is treated as 'pure' data, and the other three having different types of corruption
present. This is repeated 100 times, for each estimator on each data set, and the mean and sample standard 
deviation of these values is stored. The percentage change in the means between the estimate for the first
and each subsequent estimate is also calculated, and everything is returned in a table.

'''



from statistics import median, mean, stdev
import numpy as np
import pandas as pd


###############################################################
#################### Define functions #########################
###############################################################

# This function returns the sample standard deviation of a data set
def empirical_SD(data):
    n = len(data)
    mu = mean(data)

    sum_sq_store = 0

    for i in range(n):
        sum_sq_store += (data[i] - mu)**2
    
    Var = 1/(n-1) * sum_sq_store

    sd = np.sqrt(Var)

    return sd



# This function returns the normalised absolute deviation of a data set
def abs_dev(data):
    n = len(data)
    mu = mean(data)

    sum_store = 0

    for i in range(n):
        sum_store += (abs(data[i]-mu))
    
    norm_const = np.sqrt(np.pi/2) * 1/(n-1)

    sd = norm_const * sum_store

    return sd


# This function returns the unnormalised MAD of a data set
def MAD(data):
    n = len(data)
    x_tilde = median(data)

    dist_store = []
    for i in range(n):
        dist_store.append(abs(data[i]-x_tilde))
    
    unnorm_sd = median(dist_store)

    return unnorm_sd


# This function Winsorizes a data set using the mean and sample SD,
# taking the parameter c as an input.
# It then calculates the sample SD of the winsorized data set.
def Winsorize_bad(data, c):
    n = len(data)
    mu = mean(data)

    sigma = empirical_SD(data)

    upper_bound = mu + c * sigma
    lower_bound = mu - c * sigma

    for i in range(n):
        if data[i] > upper_bound:
            data[i] = upper_bound
        if data[i] < lower_bound:
            data[i] = lower_bound
    
    unnorm_sd = empirical_SD(data)

    return unnorm_sd




# This function calculates the S_n estimator of scale for a data set
def S_n(data):
    n = len(data)
    med_store = []
    for i in range(0,n):
        abs_store = []
        for j in range(0,n):
            abs_store.append(abs(data[i]-data[j]))
        med_store.append(median(abs_store))
    
    return median(med_store)



# This function calculates the Q_n estimator of scale for a data set, 
# taking the parameter value k as an input
def Q_n(data, k):
    n = len(data)
    abs_store = []

    for i in range(n):
        for j in range(i+1,n):
            abs_store.append(abs(data[i]-data[j]))
    n2 = len(abs_store)
    abs_sorted = sorted(abs_store)
    ind = int(n2//(1/k))
    return (abs_sorted[ind])


###############################################################
############## Apply estimators to data sets ##################
###############################################################

# Lists to store all of our values
emp1 = []
abso1 = []
mad1 = []
win1 = []
sn1 = []
qn1 = []

emp2 = []
abso2 = []
mad2 = []
win2 = []
sn2 = []
qn2 = []

emp3 = []
abso3 = []
mad3 = []
win3 = []
sn3 = []
qn3 = []

emp4 = []
abso4 = []
mad4 = []
win4 = []
sn4 = []
qn4 = []






# Apply each estimator to each data set type 100 times
for i in range(100):
    # The original data is 200 points from a N(0,1)
    data_use = np.random.normal(size = 200)

    data = data_use

    # Apply our estimators to the data
    emp1.append(empirical_SD(data))
    abso1.append(abs_dev(data))
    mad1.append(MAD(data))
    win1.append(Winsorize_bad(data, 1.7))
    sn1.append(S_n(data))
    qn1.append(Q_n(data, 0.25))


    # This data set has an additional value at 10,000, very low level but 
    # extreme corruption
    corruption = [10000]
    data = np.concatenate((data_use, corruption))

    emp2.append(empirical_SD(data))
    abso2.append(abs_dev(data))
    mad2.append(MAD(data))
    win2.append(Winsorize_bad(data, 1.7))
    sn2.append(S_n(data))
    qn2.append(Q_n(data, 0.25))



    # This data set has the original 200 N(0,1) points as well as 10 points
    # from a N(0,9) distribution, a higher level but less extreme corruption
    # type
    corruption = np.random.normal(size = 10, scale = 9)
    data = np.concatenate((data_use, corruption))

    emp3.append(empirical_SD(data))
    abso3.append(abs_dev(data))
    mad3.append(MAD(data))
    win3.append(Winsorize_bad(data, 1.7))
    sn3.append(S_n(data))
    qn3.append(Q_n(data, 0.25))


    # The last data set has the original 200 N(0,1) points as well as 50 points
    # set at 0. This is a high level of corruption, but of a different type
    corruption = [0]*50
    data = np.concatenate((data_use, corruption))

    emp4.append(empirical_SD(data))
    abso4.append(abs_dev(data))
    mad4.append(MAD(data))
    win4.append(Winsorize_bad(data, 1.7))
    sn4.append(S_n(data))
    qn4.append(Q_n(data, 0.25))



###############################################################
############# Calculate means and Stand. Dev. #################
###############################################################

# We calculate the means and samle SDs of each of the lists above, and store them in rows

emp_m1 = round(mean(emp1),3)
emp_sd1 = round(stdev(emp1),3)
abso_m1 = round(mean(abso1),3)
abso_sd1 = round(stdev(abso1),3)
mad_m1 = round(mean(mad1),3)
mad_sd1 = round(stdev(mad1),3)
win_m1 = round(mean(win1),3)
win_sd1 = round(stdev(win1),3)
sn_m1 = round(mean(sn1),3)
sn_sd1 = round(stdev(sn1),3)
qn_m1 = round(mean(qn1),3)
qn_sd1 = round(stdev(qn1),3)

emp_msd1 = f'{emp_m1}, {emp_sd1}'
abso_msd1 = f'{abso_m1}, {abso_sd1}'
mad_msd1 = f'{mad_m1}, {mad_sd1}'
win_msd1 = f'{win_m1}, {win_sd1}'
sn_msd1 = f'{sn_m1}, {sn_sd1}'
qn_msd1 = f'{qn_m1}, {qn_sd1}'

row1 = (emp_msd1, abso_msd1, mad_msd1, win_msd1, sn_msd1, qn_msd1)




emp_m2 = round(mean(emp2),3)
emp_sd2 = round(stdev(emp2),3)
abso_m2 = round(mean(abso2),3)
abso_sd2 = round(stdev(abso2),3)
mad_m2 = round(mean(mad2),3)
mad_sd2 = round(stdev(mad2),3)
win_m2 = round(mean(win2),3)
win_sd2 = round(stdev(win2),3)
sn_m2 = round(mean(sn2),3)
sn_sd2 = round(stdev(sn2),3)
qn_m2 = round(mean(qn2),3)
qn_sd2 = round(stdev(qn2),3)

emp_msd2 = f'{emp_m2}, {emp_sd2}'
abso_msd2 = f'{abso_m2}, {abso_sd2}'
mad_msd2 = f'{mad_m2}, {mad_sd2}'
win_msd2 = f'{win_m2}, {win_sd2}'
sn_msd2 = f'{sn_m2}, {sn_sd2}'
qn_msd2 = f'{qn_m2}, {qn_sd2}'

row2 = (emp_msd2, abso_msd2, mad_msd2, win_msd2, sn_msd2, qn_msd2)


emp_m3 = round(mean(emp3),3)
emp_sd3 = round(stdev(emp3),3)
abso_m3 = round(mean(abso3),3)
abso_sd3 = round(stdev(abso3),3)
mad_m3 = round(mean(mad3),3)
mad_sd3 = round(stdev(mad3),3)
win_m3 = round(mean(win3),3)
win_sd3 = round(stdev(win3),3)
sn_m3 = round(mean(sn3),3)
sn_sd3 = round(stdev(sn3),3)
qn_m3 = round(mean(qn3),3)
qn_sd3 = round(stdev(qn3),3)

emp_msd3 = f'{emp_m3}, {emp_sd3}'
abso_msd3 = f'{abso_m3}, {abso_sd3}'
mad_msd3 = f'{mad_m3}, {mad_sd3}'
win_msd3 = f'{win_m3}, {win_sd3}'
sn_msd3 = f'{sn_m3}, {sn_sd3}'
qn_msd3 = f'{qn_m3}, {qn_sd3}'

row3 = (emp_msd3, abso_msd3, mad_msd3, win_msd3, sn_msd3, qn_msd3)


emp_m4 = round(mean(emp4),3)
emp_sd4 = round(stdev(emp4),3)
abso_m4 = round(mean(abso4),3)
abso_sd4 = round(stdev(abso4),3)
mad_m4 = round(mean(mad4),3)
mad_sd4 = round(stdev(mad4),3)
win_m4 = round(mean(win4),3)
win_sd4 = round(stdev(win4),3)
sn_m4 = round(mean(sn4),3)
sn_sd4 = round(stdev(sn4),3)
qn_m4 = round(mean(qn4),3)
qn_sd4 = round(stdev(qn4),3)

emp_msd4 = f'{emp_m4}, {emp_sd4}'
abso_msd4 = f'{abso_m4}, {abso_sd4}'
mad_msd4 = f'{mad_m4}, {mad_sd4}'
win_msd4 = f'{win_m4}, {win_sd4}'
sn_msd4 = f'{sn_m4}, {sn_sd4}'
qn_msd4 = f'{qn_m4}, {qn_sd4}'

row4 = (emp_msd4, abso_msd4, mad_msd4, win_msd4, sn_msd4, qn_msd4)


row2_5 = []

row3_5 = []

row4_5 = []


###############################################################
################# Calculate perc. changes #####################
###############################################################

# We calculate the percentage change in the means of each estimator between the first
# and each subsequent data set 


row2_5.append(100*(abs(emp_m2-emp_m1))/emp_m1)
row2_5.append(100*(abs(abso_m2-abso_m1))/abso_m1)
row2_5.append(100*(abs(mad_m2-mad_m1))/mad_m1)
row2_5.append(100*(abs(win_m2-win_m1))/win_m1)
row2_5.append(100*(abs(sn_m2-sn_m1))/sn_m1)
row2_5.append(100*(abs(qn_m2-qn_m1))/qn_m1)


row3_5.append(100*(abs(emp_m3-emp_m1))/emp_m1)
row3_5.append(100*(abs(abso_m3-abso_m1))/abso_m1)
row3_5.append(100*(abs(mad_m3-mad_m1))/mad_m1)
row3_5.append(100*(abs(win_m3-win_m1))/win_m1)
row3_5.append(100*(abs(sn_m3-sn_m1))/sn_m1)
row3_5.append(100*(abs(qn_m3-qn_m1))/qn_m1)


row4_5.append(100*(abs(emp_m4-emp_m1))/emp_m1)
row4_5.append(100*(abs(abso_m4-abso_m1))/abso_m1)
row4_5.append(100*(abs(mad_m4-mad_m1))/mad_m1)
row4_5.append(100*(abs(win_m4-win_m1))/win_m1)
row4_5.append(100*(abs(sn_m4-sn_m1))/sn_m1)
row4_5.append(100*(abs(qn_m4-qn_m1))/qn_m1)



# Return all of the results
d = {'Data A': row1, 'Data B': row2, '% diff A B': row2_5, 'Data C': row3, '% diff A C ': row3_5, 'Data D': row4, '% diff A, D': row4_5}
df = pd.DataFrame(data=d)
df.index = ['Sample standard deviation','Absolute deviation','MAD','Winsor shift','S_n','Q_n']

print(df.to_string())