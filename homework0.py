import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import re

pokemon = pd.read_csv("Data/Pokemon/pokemon_species.csv")
excel_file = pd.ExcelFile("Data/Dresses_Attribute_Sales/Attribute DataSet.xlsx")
dresses = excel_file.parse('Sheet1')
narcissism = pd.read_csv("Data/NPI/data.csv")

# Cleaning
# Dresses
dresses.Price = dresses.Price.str.title()
dresses.Price.replace(to_replace='Average', value='Medium', inplace=True)

dresses.Season = dresses.Season.str.title()
dresses.Season.replace(to_replace='Automn', value='Autumn', inplace=True)

dresses.SleeveLength = dresses.SleeveLength.str.title()
dresses.SleeveLength.replace(to_replace=re.compile('^Cap.*'), value='Cap', inplace=True)
dresses.SleeveLength.replace(to_replace='Halfsleeve', value='Half', inplace=True)
dresses.SleeveLength.replace(to_replace=re.compile('.*less$'), value='Sleeveless', inplace=True)
dresses.SleeveLength.replace(to_replace=re.compile('^Thre.*'), value='Three Quarter', inplace=True)
dresses.SleeveLength.replace(to_replace=re.compile('^.*rndowncollor$'), value='Turndown Collar', inplace=True)

dresses.Style = dresses.Style.str.title()

# Narcissism
age_cutoff = narcissism.age.median()  # 30


def categorize_age(row):
    if row.age < age_cutoff:
        return 'Young'
    else:
        return 'Old'


narcissism['age_category'] = narcissism.apply(categorize_age, axis=1)

# Plotting

# Pokemon
# -- DONE --
hatch_hist = sns.distplot(pokemon.hatch_counter, kde=False, hist_kws={'alpha': 1})
hatch_hist.set_xlabel('Gestation Period')
hatch_hist.set_ylabel('Number of Pokemon')
hatch_hist.set_title('Gestation Period Distribution')
plt.tight_layout()
plt.show()

# -- DONE --
catch_hist = sns.distplot(pokemon.capture_rate, kde=False, hist_kws={'alpha': 1})
catch_hist.set_xlabel('Catch Rate')
catch_hist.set_ylabel('Number of Pokemon')
catch_hist.set_title('Catch Rate Distribution')
plt.tight_layout()
plt.show()

# -- DONE --
hatch_vs_capture = pokemon.plot.scatter(x='hatch_counter', y='capture_rate')
hatch_vs_capture.set_xlabel('Gestation Period')
hatch_vs_capture.set_ylabel('Catch Rate')
hatch_vs_capture.set_title('Catch Rate vs Gestation Period')
plt.tight_layout()
plt.show()

# Dresses
# -- DONE --
dress_styles = dresses.Style.value_counts()[:10]
style_frame = pd.DataFrame({'Style': dress_styles.index, 'Count': dress_styles.values})[['Style', 'Count']]
ax = plt.subplot()
ax.axis('off')
ax.table(cellText=style_frame.values, cellLoc='center', colLabels=list(style_frame), colWidths=[.3, .2], loc='center',
         bbox=[0, 0, .95, .95])
ax.set_title('Popular Dress Styles')
plt.tight_layout()
plt.show()

# -- DONE --
pop_dresses = dresses.Style.value_counts()[:10].plot.bar()
pop_dresses.set_xlabel('Style');
pop_dresses.set_ylabel('Number Sold')
pop_dresses.set_title('Popular Dress Styles')
plt.tight_layout()
plt.show()

# -- DONE --
season_order = ['Spring', 'Summer', 'Autumn', 'Winter']
sleeve_frame = pd.crosstab(dresses.SleeveLength, columns=dresses.Season)[season_order]
sleeve_frame = sleeve_frame.reset_index().rename(columns={'SleeveLength': 'Sleeve Length'})
ax = plt.subplot()
ax.axis('off')
ax.table(cellText=sleeve_frame.values, cellLoc='center', colLabels=list(sleeve_frame), loc='center',
         bbox=[0, 0, .95, .95])
ax.set_title('Sleeve Lengths by Season')
plt.tight_layout()
plt.show()


# -- DONE --
price_order = ['Low', 'Medium', 'High', 'Very-High']
price_rating = sns.swarmplot(x='Price', y='Rating', data=dresses, order=price_order)
price_rating.set_title('Dress Price vs Rating')
plt.tight_layout()
plt.show()


# Narcissism
# -- DONE --
gender_df = narcissism[(narcissism.gender == 1) | (narcissism.gender == 2)]
narc_gender = sns.boxplot(x='gender', y='score', data=gender_df, width=.2, notch=True)
narc_gender.set(xlabel='Gender', ylabel='Score', xticklabels=['Male', 'Female'])
narc_gender.set_title('Gender Comparison of Narcissism')
plt.tight_layout()
plt.show()

# -- DONE --
age_compare = sns.boxplot(x='age_category', y='score', data=narcissism, order=['Young', 'Old'], width=.2, notch=True)
age_compare.set(xlabel='Age', ylabel='Score')
age_compare.set_title('Age Comparison of Narcissism')
plt.tight_layout()
plt.show()

# -- DONE --
score_vs_time = narcissism.sort_values(by='elapse')[:-16].plot.scatter(x='score', y='elapse')
score_vs_time.set_xlabel('Score')
score_vs_time.set_ylabel('Elapsed Time (s)')
score_vs_time.set_title('Narcissism Score vs Time Taken')
plt.tight_layout()
plt.show()
