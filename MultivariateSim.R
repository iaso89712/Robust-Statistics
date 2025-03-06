library(rrcov)
library(MASS)
library(ggplot2)

# Function to generate multivariate normal data
generate_data <- function(n, p, mean_val = 0, cov_val = 1) {
  set.seed(42)
  mu <- rep(mean_val, p)
  Sigma <- diag(rep(cov_val, p))
  mvrnorm(n, mu, Sigma)
}

# Function to contaminate data with outliers
contaminate_data <- function(X, fraction, magnitude = 20) {
  n_outliers <- round(nrow(X) * fraction)
  if (n_outliers > 0) {
    X_outliers <- matrix(runif(n_outliers * ncol(X), -magnitude, magnitude), nrow = n_outliers)
    X[1:n_outliers, ] <- X_outliers
  }
  return(X)
}

# Experiment parameters
n_samples <- 500
n_features <- 8
contamination_levels <- seq(0, 0.6, length.out = 12)

# Store results
errors_sd <- numeric(length(contamination_levels))
errors_mcd <- numeric(length(contamination_levels))
errors_mve <- numeric(length(contamination_levels))
errors_classical <- numeric(length(contamination_levels))
cov_errors_sd <- numeric(length(contamination_levels))
cov_errors_mcd <- numeric(length(contamination_levels))
cov_errors_mve <- numeric(length(contamination_levels))
cov_errors_classical <- numeric(length(contamination_levels))

for (i in seq_along(contamination_levels)) {
  contamination <- contamination_levels[i]
  X <- generate_data(n_samples, n_features)
  mu_true <- colMeans(X)
  C_true <- cov(X)
  X_contaminated <- contaminate_data(X, contamination)
  
  # Compute Classical Estimator
  mu_classical <- colMeans(X_contaminated)
  C_classical <- cov(X_contaminated)
  
  # Compute SD estimator
  sd_estimator <- CovSde(X_contaminated)
  mu_sd <- sd_estimator@center
  C_sd <- sd_estimator@cov
  
  # Compute MCD estimator
  mcd_estimator <- CovMcd(X_contaminated)
  mu_mcd <- mcd_estimator@center
  C_mcd <- mcd_estimator@cov
  
  # Compute MVE estimator
  mve_estimator <- CovMve(X_contaminated)
  mu_mve <- mve_estimator@center
  C_mve <- mve_estimator@cov
  
  # Compute location errors
  errors_sd[i] <- sum(abs(mu_sd - mu_true))
  errors_mcd[i] <- sum(abs(mu_mcd - mu_true))
  errors_mve[i] <- sum(abs(mu_mve - mu_true))
  errors_classical[i] <- sum(abs(mu_classical - mu_true))
  
  # Compute covariance errors
  cov_errors_sd[i] <- sum(abs(C_sd - C_true))
  cov_errors_mcd[i] <- sum(abs(C_mcd - C_true))
  cov_errors_mve[i] <- sum(abs(C_mve - C_true))
  cov_errors_classical[i] <- sum(abs(C_classical - C_true))
}

# Create DataFrame for plotting location deviations
results_location <- data.frame(
  Contamination = rep(contamination_levels, 4),
  Deviation = c(errors_sd, errors_mcd, errors_mve, errors_classical),
  Estimator = rep(c("Stahel-Donoho", "MCD", "MVE", "Classical"), each = length(contamination_levels))
)

# Create DataFrame for plotting covariance deviations
results_covariance <- data.frame(
  Contamination = rep(contamination_levels, 4),
  Deviation = c(cov_errors_sd, cov_errors_mcd, cov_errors_mve, cov_errors_classical),
  Estimator = rep(c("Stahel-Donoho", "MCD", "MVE", "Classical"), each = length(contamination_levels))
)


# Plot results
ggplot(results, aes(x = Contamination, y = Deviation, color = Estimator)) +
  geom_line(size = 1) +
  geom_point(size = 2) +
  labs(title = "Breakdown Behavior of Robust Estimators",
       x = "Contamination Fraction",
       y = "Location Error") +
  theme_minimal()+
  coord_cartesian(ylim=c(1, 30))

# Plot results for covariance deviation
ggplot(results_covariance, aes(x = Contamination, y = Deviation, color = Estimator)) +
  geom_line(size = 1) +
  geom_point(size = 2) +
  labs(title = "Breakdown Behavior of Robust Estimators vs Classical Estimator (Covariance)",
       x = "Contamination Fraction",
       y = "Covariance Error") +
  theme_minimal() +
  coord_cartesian(ylim = c(1, 30))
