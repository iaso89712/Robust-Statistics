'''
FIGURE 3.2

In this code we graph what a N(0,1) distribution raised to various powers looks like.

'''


import numpy as np
from scipy.stats import norm

import matplotlib.pyplot as plt


# Generate values
x = np.linspace(-8, 8, 1000)

# Return the PDF for a N(0,1)
pdf = norm.pdf(x)

# Raise the PDF to various powers
pdf_05 = pdf ** 0.5

pdf_01 = pdf ** 0.1

pdf_005 = pdf ** 0.05

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(x, pdf, label='Normal PDF')
plt.plot(x, pdf_05, label='Normal PDF ^ 0.5')
plt.plot(x, pdf_01, label='Normal PDF ^ 0.1')
plt.plot(x, pdf_005, label='Normal PDF ^ 0.05')

plt.xlabel('x')
plt.ylabel('Density')
plt.title('Normal PDF and its Powers')
plt.legend()

plt.show()