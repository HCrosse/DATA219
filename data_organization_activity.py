import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

original = pd.read_csv("Data/Activity/activity.csv")

students = original[['name', 'year', 'major', 'school', 'creds']].copy()
temp = original[['name', 'GPAFr', 'GPASo', 'GPAJr', 'GPASr']].copy()
temp.columns = ['name', 'Fr', 'So', 'Jr', 'Sr']
gpas = pd.melt(temp, ['name'], var_name='year', value_name='GPA')
gpas = gpas[pd.notnull(gpas['GPA'])]
schools = original[['school', 'type', 'mascot']].copy().drop_duplicates().reset_index()
schools = schools[['school', 'type', 'mascot']]

del original, temp


def urban_or_rural(row):
    urban_schools = ['UVA', 'UMW', 'Richmond']
    if row['school'] in urban_schools:
        return 'urban'
    else:
        return 'rural'


schools['urban_rural'] = schools.apply(urban_or_rural, axis=1)

# #5
print('Number of students: ' + str(len(students)))

# #6
print('Total end-of-year GPA measurements: ' + str(len(gpas)))

# #7
print('Average EOY GPA: ' + str(gpas.GPA.mean()))

# #8
students_schools = pd.merge(students, schools, on='school')
print(students_schools.urban_rural.value_counts())

# #9
freshman_gpa = pd.merge(students_schools, gpas, on='name')
freshman_gpa = freshman_gpa[freshman_gpa.year_y == 'Fr'][['GPA', 'urban_rural']]
rural_freshman_gpa = freshman_gpa[freshman_gpa.urban_rural == 'rural'].GPA.mean()
urban_freshman_gpa = freshman_gpa[freshman_gpa.urban_rural == 'urban'].GPA.mean()
print('Average Freshman rural GPA:' + str(rural_freshman_gpa))
print('Average Freshman urban GPA:' + str(urban_freshman_gpa))

# #10
all_gpas = pd.merge(students, gpas, on='name')
all_gpas['year_y'] = np.where(all_gpas.year_y == 'Fr', 'Fr', 'Other')
gpa_plot = sns.boxplot(x='year_y', y='GPA', data=all_gpas)
gpa_plot.set(xlabel='Year', title='Freshman vs Other GPA')
plt.tight_layout()
plt.show()

# #11
all_gpas = pd.merge(students, gpas, on='name')
major_plot = sns.boxplot(x='major', y='GPA', data=all_gpas)
major_plot.set(xlabel='Major', title='Major vs GPA')
plt.tight_layout()
plt.show()

# #12
school_plot = sns.boxplot(x='school', y='GPA', data=all_gpas)
school_plot.set(xlabel='School', title='School vs GPA')
plt.tight_layout()
plt.show()

# #13
all_gpas = all_gpas[['name', 'creds', 'year_y', 'GPA']]
one_gpa = pd.pivot_table(all_gpas, values='GPA', index='name', columns='year_y')
one_gpa['average'] = one_gpa.mean(axis=1)
one_gpa = one_gpa.reset_index()
student_creds = students[['name', 'creds']]
one_gpa = pd.merge(one_gpa, student_creds, on='name')
credits_plot = sns.lmplot(x='creds', y='average', data=one_gpa, lowess=True, scatter_kws={"s": 1, 'alpha': .5},
                          line_kws={'color': 'red'})
credits_plot.set(xlabel='Number of Credits', ylabel='Average GPA', title='Number of Credits vs GPA')
plt.tight_layout()
plt.show()
