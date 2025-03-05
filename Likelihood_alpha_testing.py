'''
FIGURE 3.3

In this file we test how raising the likelihood to different powers affects the posterior
distribution of some parameter mu. We use the arviz package for Bayesian inference.

'''

import pymc as pm
import numpy as np
import matplotlib.pyplot as plt
import arviz as az

# Data is generated, including corruption
data1 = np.random.normal(loc=2, scale=5, size=50)
data = np.concatenate((data1, [200]))

# Define the fixed sigma
sigma = 1.0

# Choose a range of alphas to raise the likelihood to
alpha_values = [0.01, 0.25, 0.5, 0.75, 1.0]

# Define distinct colors for each alpha
colors = plt.cm.viridis(np.linspace(0, 1, len(alpha_values)))

# We will store the traces for each posterior
traces = {}


# We define our Cauchy pdf to the power of alpha (likelihood) in this function
def custom_pdf(value, mu, sigma, alpha):
    cauchy_pdf = 1 / (np.pi * sigma * (1 + ((value - mu) / sigma) ** 2))
    return cauchy_pdf ** alpha

# Loop over alpha values
for alpha in alpha_values:
    with pm.Model() as model:
        # Prior with unknown mean
        mu = pm.Normal("mu", mu=0, sigma=1)

        # Choose our likelihood and then plot calculate and store the posterior
        log_likelihood = pm.math.log(custom_pdf(data, mu, sigma, alpha)).sum()
        pm.Potential("custom_likelihood", log_likelihood)
        trace = pm.sample(1000, cores=1, progressbar=False)
        traces[alpha] = trace

# Plot the posteriors for comparison on the same axis
fig, ax = plt.subplots(figsize=(10, 6))
for alpha, trace, color in zip(alpha_values, traces.values(), colors):
    az.plot_posterior(trace, var_names=["mu"], ax=ax, label=f"alpha = {alpha}", color=color, hdi_prob=None)
    
    # Some unnecessary text was appearing, so it was removed. We keep the mean text
    for text in ax.texts:
        if "94% HDI" in text.get_text() or (any(char.isdigit() for char in text.get_text()) and not text.get_text().startswith("mean=")):
            text.set_visible(False)

# Plot and show our results, adding labels to the graphs
ax.set_title("Posterior of mu for Different Alpha Values")
ax.set_xlabel("mu")
ax.set_ylabel("Density")
ax.legend()
plt.show()
