import pandas as pd

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

print(len(students))

print(len(gpas))

print(gpas.GPA.mean())

print(schools.urban_rural.value_counts())

freshmen = pd.merge(students, gpas[gpas.year == 'Fr'], on='name') # fix
print(freshmen)
rural_freshman_gpa = 0
urban_freshman_gpa = 0
