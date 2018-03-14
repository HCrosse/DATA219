import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats
import seaborn as sns
import urllib.request

raw = json.load(urllib.request.urlopen("http://cs.umw.edu/~stephen/data219/meteorites.json"))

masses = []
years = []
for meteor in raw:
    if 'mass' in meteor and 'year' in meteor:
        masses.append(float(meteor['mass']))
        years.append(int(meteor['year'][:4]))

meteors = pd.DataFrame({'Mass': masses, 'Year': years})
meteors.Mass = meteors.Mass * 0.00220462262185

year_plot = sns.kdeplot(meteors.Year, shade=True)
year_plot.set(xlabel='Year', ylabel='Frequency')
year_plot.set_title('Meteorite Distribution by Year')
plt.tight_layout()
plt.show()

mass_plot = sns.kdeplot(meteors.Mass, shade=True, bw=6)
mass_plot.set(xlabel='Mass (lbs)', ylabel='Frequency')
mass_plot.set_title('Meteorite Mass Distribution')
plt.tight_layout()
plt.show()

year_mass = sns.lmplot(x='Year', y='Mass', data=meteors, lowess=True, line_kws={'color': 'red'})
year_mass.set(xlabel='Year', ylabel='Mass (lbs)')
plt.title('Meteorite Mass by Year')
plt.yscale('log')
plt.tight_layout()
plt.show()
