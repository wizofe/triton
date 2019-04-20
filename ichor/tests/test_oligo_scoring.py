import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.stats import norm
from scipy.stats import genextreme
import scipy
import numpy as np

score_to_test = 12

fig, ax1 = plt.subplots()

file = 'p_values_1000.txt'

df = pd.read_csv(file, sep='\t', header=None)

# the normal is not a good fit for this purpose
(mu, sigma) = norm.fit(df[1])
z_score = (score_to_test - mu) / sigma
p_values = norm.sf(abs(z_score))  #one-sided
p_values_2side = norm.sf(abs(z_score)) * 2  #twosided
p_values3 = 1 - scipy.special.ndtr(z_score)

print((
    "Mu:{0:5.2f} Sigma:{1:5.2f} z_score:{2:5.2f} p_value_one_side: {3:15.13f} p_value_two_side: {4:15.13f} p_values {5:15.13f}"
).format(mu, sigma, z_score, p_values, p_values_2side, p_values3))

# instead use extreme value distribution

#fit to data

extreme_fit = genextreme.fit(df[1])
c = extreme_fit[0]
loc = extreme_fit[1]
scale = extreme_fit[2]

print(("Extreme value fits c = {0}, loc = {1}, scale = {2}").format(
    c, loc, scale))

ax1 = sns.distplot(df[1], fit=genextreme, kde=False)
x = np.linspace(-10, 16, 1000)

extreme_to_plot = genextreme(c, loc, scale)
ax1.plot(x, extreme_to_plot.pdf(x), 'r-', lw=2, label='pdf')

p_value = extreme_to_plot.pdf(score_to_test)

ax1.axvline(score_to_test)

print(("p value of score {0} = {1}").format(score_to_test, p_value))

plt.show()
