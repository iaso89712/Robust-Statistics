'''
FIGURE 1.2

Here we plot the (expected) variance for the three different estimators (\bar{X}, \bar{X}_t and \bar{X}_w) 
of location described in our project. We define the alpha and beta parameters as shown in the report, and 
then calculate the expected variance of each estimator for multiple values of epsilon (e) and k. This gives 
three 3 dimensional surfaces which we plot on the same set of axes.

'''


import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

# We will store variances in these lists
X_t = []
X_c = []
X_bar = []
X_w = []

# Here I will compare the (expected) variances for the three estimators at different values of epsilon and k
for e in range(1,31):
    for k in range(1,6):
        eps = e/150   # Scale epsilons to be between 0 and 0.2
        
        # define the alpha and betas as shown in the report
        alpha = k/(k+eps-eps*k)

        beta = 1/(k+eps-eps*k)

        # For the given epsilon and k, calculate expected variances and store these in a list.
        Var_X_t = 1/(1-eps)
        X_t.append(Var_X_t)

        Var_X_c = k/eps
        X_c.append(Var_X_c)

        Var_X_bar = 1-eps + k*eps
        X_bar.append(Var_X_bar)

        Var_X_w = alpha**2*(1-eps) + beta**2 * eps * k 
        X_w.append(Var_X_w)



K = np.arange(1, 6)
E = np.arange(1, 31) / 150

# Reshape the data into a 2D grid, so that we can plot properly
X_c = np.array(X_c).reshape((len(E), len(K)))
X_t = np.array(X_t).reshape((len(E), len(K)))
X_bar = np.array(X_bar).reshape((len(E), len(K)))
X_w = np.array(X_w).reshape((len(E), len(K)))

K_grid, E_grid = np.meshgrid(K, E)

fig = plt.figure()
ax = plt.axes(projection='3d')


# Plot everything

surface_t = ax.plot_surface(K_grid, E_grid, X_t, color='red', alpha=0.8, label=r'$X_t$')
surface_bar = ax.plot_surface(K_grid, E_grid, X_bar, color='green', alpha=0.8, label=r'$\bar{X}$')
surface_w = ax.plot_surface(K_grid, E_grid, X_w, color='blue', alpha=0.8, label=r'$X_w$')

# Set axis labels
ax.set_zlim(0.8, 1.5)
ax.set_xlabel('K')
ax.set_ylabel('Epsilon')
ax.set_zlabel('Variance')

# Add a floating legend with LaTeX-formatted labels
fig.legend([surface_t, surface_bar, surface_w], [r'$\bar{X_t}$', r'$\bar{X}$', r'$\bar{X_w}$'],
           loc='upper center', bbox_to_anchor=(0.4, 0.9), ncol=3, frameon=True)

plt.show()


