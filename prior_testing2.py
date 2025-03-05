'''
FIGURE 3.1

In this code we compare using a normal prior and using a student-t prior for robustness
in Bayesian analysis. The likelihood distributions are the same, and the two priors are a 
N(mu, 0.5) and a student-t distribution with 3 degrees of freedom, with mean mu and scale
0.289 (which gives equal variance to the two priors). The first data set is generated from
N(-0.5, 2), and the second data set is the same as the first with an additional point at 20.
The posteriors are generated and plotted on the same graph as the priors which were used to
generate them.

'''






import pymc as pm
import numpy as np
import matplotlib.pyplot as plt
import arviz as az
import scipy.stats as stats

# Generate both data sets
data1 = np.random.normal(loc=-0.5, scale=2, size=30)
data2 = np.concatenate((data1, [20]))

mu_prior_mean = 0  # Prior mean
mu_prior_sigma = 2  # Prior standard deviation

# Normal prior example
with pm.Model() as model1_normal:
    # Normal prior for the unknown mean
    mu_prior = pm.Normal("mu", mu=mu_prior_mean, sigma=0.5)
    sigma_prior = 2

    # Likelihood for the first dataset
    likelihood1 = pm.Normal("y1", mu=mu_prior, sigma=sigma_prior, observed=data1)

    # Perform inference on the first dataset
    trace1_normal = pm.sample(1000, cores=1)



# Second model with the same prior but update with the second dataset
with pm.Model() as model2_normal:
    mu_prior = pm.Normal("mu", mu=mu_prior_mean, sigma=0.5)
    sigma_prior = 2
    likelihood2 = pm.Normal("y2", mu=mu_prior, sigma=sigma_prior, observed=data2)
    trace2_normal = pm.sample(1000, cores=1)





#############################################################################
################################ STUDENT T ##################################
#############################################################################

# Student's t-distribution prior example
with pm.Model() as model1_t:
    mu_prior = pm.StudentT("mu", nu=3, mu=mu_prior_mean, sigma=0.289)

    sigma_prior = 2

    # Likelihood for the first dataset
    likelihood1_t = pm.Normal("y1", mu=mu_prior, sigma=sigma_prior, observed=data1)

    # Perform inference on the first dataset
    trace1_t = pm.sample(5000, cores=1, tune=2000)

# Second model with the same t-distribution prior but update with the second dataset
with pm.Model() as model2_t:
    mu_prior = pm.StudentT("mu", nu=3, mu=mu_prior_mean, sigma=0.289)

    sigma_prior = 2
    likelihood2_t = pm.Normal("y2", mu=mu_prior, sigma=sigma_prior, observed=data2)
    trace2_t = pm.sample(5000, cores=1, tune=2000)

# Plotting both models: Normal and Student's t Prior
fig, axs = plt.subplots(1, 2, figsize=(12, 6))







######################################################################################
################################# PLOTTING ###########################################
######################################################################################



# Generate points for the prior distribution (Normal prior)
x = np.linspace(-10, 20, 200)
prior_normal = (1/(np.sqrt(2*np.pi)*mu_prior_sigma)) * np.exp(-0.5 * ((x - mu_prior_mean) / mu_prior_sigma) ** 2)

# Plot the normal prior and posteriors
axs[0].plot(x, prior_normal, label="Normal Prior", color="blue", lw=2)
az.plot_posterior(trace1_normal, var_names=["mu"], ax=axs[0], hdi_prob=None, label="Posterior from uncontaminated data", color="green", lw=2)
az.plot_posterior(trace2_normal, var_names=["mu"], ax=axs[0], hdi_prob=None, label="Posterior from contaminated data", color="red", lw=2)
axs[0].set_title("Normal Prior with Posteriors")
axs[0].set_xlabel("mu")
axs[0].set_ylabel("Density")
axs[0].legend()


x_min, x_max = -2, 2  # Set appropriate x-axis limits


# plot everything for the student-t prior
prior_t = stats.t.pdf(x, df=2, loc=mu_prior_mean, scale=2)
axs[1].plot(x, prior_t, label="Student's t Prior", color="purple", lw=2)
az.plot_posterior(trace1_t, var_names=["mu"], ax=axs[1], hdi_prob=None, label="Posterior from uncontaminated data", color="green", lw=2)
az.plot_posterior(trace2_t, var_names=["mu"], ax=axs[1], hdi_prob=None, label="Posterior from contaminated data", color="red", lw=2)



# Remove some ugly text
for ax in axs:
    for text in ax.texts:
        if "94% HDI" in text.get_text() or (any(char.isdigit() for char in text.get_text()) and not text.get_text().startswith("mean=")):
            text.set_visible(False)






axs[1].set_title("Student's t Prior with Posteriors")
axs[1].set_xlabel("mu")
axs[1].set_ylabel("Density")
axs[1].legend()


axs[0].set_xlim(x_min, x_max)
axs[1].set_xlim(x_min, x_max)

plt.tight_layout()
plt.show()
