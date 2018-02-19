import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# JSON Structure:
# prizes - list of dicts
#     year
#     category
#     laureates - list of dicts
#         id - string number
#         firstname
#         surname
#         motivation - sentence
#         share - inverted
# laureates - list of dicts
#     id - string number - primary-foreign to above
#     firstname
#     surname
#     born - "YYYY-MM-DD"
#     died - "YYYY-MM-DD"
#     bornCountry
#     bornCountryCode
#     bornCity
#     diedCountry
#     diedCountryCode
#     diedCity
#     gender - male/female
#     prizes - list of dicts
#         year
#         category
#         share
#         motivation
#         affiliations - list of dicts
#             name - affiliation name
#             city
#             country
# countries - list of dicts
#     name - primary-foreign to above
#     code

# Questions
# What is the overall prize count for each gender  - pie/bar
#     Are certain categories different             - bar
# How many avg awards for each gender              - box/swarm
# How has % female changed over time               - tsplot
# What is the avg share for each gender            - box?
#     Effected if:
#         1) female % changed over time
#         2) overall share % changed over time
# Does one gender collaborate more than another    - box?
#     Effected if:
#         1) female % changed over time
#         2) collaboration % changed over time
# % women by region                                - pie/bar
#     Born or died as region?
#     Effected if:
#         1) female % changed over time
#         2) region % changed over time
# Are there any hot-spot universities for women    - bar/map
#     Have to check affiliations, find good way to plot

sns.set(style="darkgrid")
json_data = json.load(open("Data/Nobel/nobel.json"))

pyear = []
pcat = []
pid = []
pfirst = []
plast = []
# pmotive = []
pshare = []
pnum = []
for prize in json_data["prizes"]:
    for laureate in prize["laureates"]:
        pyear.append(prize["year"])
        pcat.append(prize["category"])
        pid.append(laureate["id"])
        pfirst.append(laureate["firstname"])
        plast.append(laureate["surname"])
        # pmotive.append(laureate["motivation"])
        pshare.append(1 / int(laureate["share"]))
        pnum.append(len(prize["laureates"]))
prizes = pd.DataFrame({"Year": pyear, "Category": pcat, "ID": pid, "First Name": pfirst, "Last Name": plast,
                       "Share": pshare, "Team Size": pnum})

cname = []
ccode = []
for country in json_data["countries"]:
    cname.append(country["name"])
    ccode.append(country["code"])
countries = pd.DataFrame({"Country": cname, "Code": ccode})

# Ignoring affiliations, one row per laureate
lid = []
lid2 = []
# lfirst = []
# llast = []
lborn = []
ldied = []
# lborncc = []
# lborncity = []
# ldiedcc = []
# ldiedcity = []
lgender = []
lgender2 = []
lnumprizes = []
lyear = []
lcat = []
lshare = []
ltshare = []
lavgshare = []
lavgteam = []
# lmotive = []
for laureate in json_data["laureates"]:
    if ("year" not in laureate["prizes"][0]):
        continue
    share_count = 0
    tshare_count = 0
    team_count = 0
    lid.append(laureate["id"])
    # lfirst.append(laureate["firstname"])
    # llast.append(laureate["surname"])
    lgender.append(laureate["gender"].title())
    lborn.append(laureate["born"])
    ldied.append(laureate["died"])
    # lborncc.append(laureate["bornCountryCode"])
    # lborncity.append(laureate["bornCity"])
    # ldiedcc.append(laureate["diedCountryCode"])
    # ldiedcity.append(laureate["diedCity"])
    num_prizes = len(laureate["prizes"])
    lnumprizes.append(num_prizes)
    for prize in laureate["prizes"]:
        lid2.append(laureate["id"])
        lgender2.append(laureate["gender"].title())
        lyear.append(prize["year"])
        lcat.append(prize["category"].title())
        lshare.append(1 / int(prize["share"]))
        # lmotive.append(prize["motivation"])
        share_count += int(prize["share"])
        tshare_count += 1 / int(prize["share"])
        team_count += len(prizes[(prizes.Year == prize["year"]) & (prizes.Category == prize["category"])])
    ltshare.append(tshare_count)
    lavgshare.append(1 / (share_count / num_prizes))
    lavgteam.append(team_count / num_prizes)
laureates = pd.DataFrame({"ID": lid, "Gender": lgender, "Birth Date": lborn, "Death Date": ldied, "Prizes": lnumprizes,
                          "Total Share": ltshare, "Average Share": lavgshare, "Average Size": lavgteam})
laureate_prizes = pd.DataFrame({"ID": lid2, "Gender": lgender2, "Year": lyear, "Category": lcat, "Share": lshare})
laureate_prizes['Team'] = np.where(laureate_prizes['Share'] == 1, 'No', 'Yes')

# What is the overall prize count for each gender
#     Are certain categories different

prize_gender_bar = sns.countplot(x='Gender', data=laureate_prizes)
prize_gender_bar.set(title='Nobel Prizes Won by Gender', ylabel='Count')
for p in prize_gender_bar.patches:
    prize_gender_bar.annotate('{:1.2f}'.format(p.get_height()/len(laureate_prizes)), (p.get_x()+.3, p.get_height()+5))
plt.tight_layout()
plt.show()

prize_category_bar = sns.countplot(x='Category', hue='Gender', data=laureate_prizes)
plt.legend(loc='upper right')
prize_category_bar.set(title='Nobel Prizes Won by Gender and Category', ylabel='Count')
plt.tight_layout()
plt.show()

# How has % female changed over time
group = laureate_prizes.groupby(['Year', 'Gender']).sum() / laureate_prizes.groupby('Year').sum()
pivot = pd.pivot_table(index='Year', columns='Gender', values='Share', data=group).fillna(0)
ax = pivot.plot()
ax.set_title("Share of Nobels Over Time")
plt.show()

# What is the avg share for each gender
share_gender = sns.boxplot(x='Gender', y='Average Share', data=laureates)
plt.tight_layout()
plt.show()

# Does one gender collaborate more than another
women_on = len(laureate_prizes[(laureate_prizes.Team == 'Yes') & (laureate_prizes.Gender == 'Female')]) / int(
    laureate_prizes.Gender.value_counts()['Female'])
women_on = '{:.2f}%'.format(women_on * 100)
men_on = len(laureate_prizes[(laureate_prizes.Team == 'Yes') & (laureate_prizes.Gender == 'Male')]) / int(
    laureate_prizes.Gender.value_counts()['Male'])
men_on = '{:.2f}%'.format(men_on * 100)
collaboration = pd.DataFrame({"Gender": ["Male", "Female"], "Percentage That Won on a Team": [men_on, women_on]})
ax = plt.subplot()
ax.axis('off')
ax.table(cellText=collaboration.values, cellLoc='center', colLabels=list(collaboration), loc='center',
         bbox=[0, 0, .95, .95],)
ax.set_title('Nobel Laureate Team Participation by Gender')
plt.tight_layout()
plt.show()
