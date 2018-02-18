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
lavgshare = []
lavgteam = []
# lmotive = []
for laureate in json_data["laureates"]:
    if ("year" not in laureate["prizes"][0]):
        continue
    share_count = 0
    team_count = 0
    lid.append(laureate["id"])
    # lfirst.append(laureate["firstname"])
    # llast.append(laureate["surname"])
    lgender.append(laureate["gender"])
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
        lgender2.append(laureate["gender"])
        lyear.append(prize["year"])
        lcat.append(prize["category"])
        lshare.append(1 / int(prize["share"]))
        # lmotive.append(prize["motivation"])
        share_count += int(prize["share"])
        team_count += len(prizes[(prizes.Year == prize["year"]) & (prizes.Category == prize["category"])])
    lavgshare.append(1 / (share_count / num_prizes))
    lavgteam.append(team_count / num_prizes)
laureates = pd.DataFrame({"ID": lid, "Gender": lgender, "Birth Date": lborn, "Death Date": ldied,
                          "Average Share": lavgshare, "Average Size": lavgteam})
laureate_prizes = pd.DataFrame({"ID": lid2, "Gender": lgender2, "Year": lyear, "Category": lcat, "Share": lshare})

# What is the overall prize count for each gender  - pie/bar
#     Are certain categories different             - bar
prize_gender_pie = laureate_prizes.Gender.value_counts().plot(kind='pie')
plt.tight_layout()
plt.show()
