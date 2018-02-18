import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats.stats
import seaborn as sns
import urllib.request


def tax_calculator(salary):
    tax = 0

    if (salary <= 9325):
        tax += salary * .1
    elif (salary <= 37950):
        tax += (salary * .15) - 466.25
    elif (salary <= 91900):
        tax += (salary * .25) - 4261.25
    elif (salary <= 191650):
        tax += (salary * .28) - 7018.25
    elif (salary <= 416700):
        tax += (salary * .33) - 16600.75
    elif (salary <= 418400):
        tax += (salary * .35) - 24934.75
    else:
        tax += (salary * .396) - 44181.15

    return tax


vtax_calculator = np.vectorize(tax_calculator)

# Songs
song_lengths = np.random.normal(180, 30, 10000)
plays = np.random.normal(500000, 100000, 10000)
songs = pd.DataFrame(data={'Length (s)': song_lengths, 'Plays': plays})
song_plot = sns.regplot(x='Length (s)', y='Plays', data=songs, scatter_kws={"s": 5})
song_plot.set_title('Song Length vs Plays')
plt.tight_layout()
plt.show()
song_kernal = sns.jointplot(x='Length (s)', y='Plays', data=songs, kind="kde")
plt.tight_layout()
plt.show()
print(scipy.stats.stats.pearsonr(song_lengths, plays))

# Taxes
salaries = np.random.normal(50000, 15000, 5093).clip(min=0)
taxes = vtax_calculator(salaries)
tax_df = pd.DataFrame(data={'Salary': salaries, 'Taxes': taxes})
tax_plot = sns.regplot(x='Salary', y='Taxes', data=tax_df, scatter_kws={"s": 5})
tax_plot.set_title('Salary vs Taxes (US$)')
tax_plot.set_ylim(bottom=0)
plt.tight_layout()
plt.show()

# Accidents
accident_speeds = np.random.normal(40, 10, 1935)
damages = (accident_speeds * 100) + 500 + np.random.normal(1000, 500, 1935)
accident_df = pd.DataFrame(data={'Speed (mph)': accident_speeds, 'Damages (US$)': damages})
accident_plot = sns.regplot(x='Speed (mph)', y='Damages (US$)', data=accident_df, scatter_kws={"s": 10})
accident_plot.set_title("Accident Speed vs Damages")
plt.tight_layout()
plt.show()
print(scipy.stats.stats.pearsonr(accident_speeds, damages))

# Students
university = np.random.choice(['UMW', 'JMU', 'Richmond', 'VATech'], p=[.15, .38, .06, .41], size=8932)
mascot = np.where(university == 'UMW', 'eagle', np.where(university == 'JMU', 'duke',
                                                         np.where(university == 'Richmond', 'spider', 'hoakie')))
fave_food = np.random.choice(['pizza', 'sushi', 'falafel'], p=[.6, .3, .1], size=8932)

choices = ['partier', 'scholar', 'rebel', 'dropout']
umw_types = np.random.choice(choices, p=[.3, .4, .2, .1], size=8932)
jmu_types = np.random.choice(choices, p=[.6, .1, .2, .1], size=8932)
richmond_types = np.random.choice(choices, p=[.2, .3, .3, .2], size=8932)
tech_types = np.random.choice(choices, p=[.6, .2, .1, .1], size=8932)
student_type = np.where(university == 'UMW', umw_types, np.where(university == 'JMU', jmu_types,
                                                                 np.where(university == 'Richmond', richmond_types,
                                                                          tech_types)))
uni_vs_mascot = pd.crosstab(university, mascot)
print(uni_vs_mascot)
print(scipy.stats.chi2_contingency(uni_vs_mascot))

uni_vs_food = pd.crosstab(university, fave_food)
print(uni_vs_food)
print(scipy.stats.chi2_contingency(uni_vs_food))

uni_vs_type = pd.crosstab(university, student_type)
print(uni_vs_type)
print(scipy.stats.chi2_contingency(uni_vs_type))

# JSON
data = json.load(urllib.request.urlopen("http://data.consumerfinance.gov/api/views.json"))
print(data[3]['description'])
for i in data:
    if(i['viewCount'] >= 4000):
        print(i['name'])
