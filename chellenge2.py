import pandas as pd
import urllib.request
from bs4 import BeautifulSoup

f = urllib.request.urlopen("http://remush.be/tezauro/Kontakto.html")
raw = f.read()
soup = BeautifulSoup(raw, "html5lib").find_all('tr')[1]

root = soup.get_text().split()
pos = []
common = []

for i, li in enumerate(soup.find_all('li')):
    if root[i][0] == '-':
        pos.append('suf')
    elif root[i][-1] == '-':
        pos.append('pre')
    elif root[i][-1] == 'o':
        pos.append('N')
    elif root[i][-1] == 'a':
        pos.append('A')
    elif root[i][-1] == 'i':
        attributes = li.find('a').attrs
        if 'style' in attributes and attributes['style'] == 'color: rgb(255, 0, 0);':  # red
            pos.append('VI')
        elif 'style' in attributes and attributes['style'] == 'color: rgb(51, 204, 0);':  # green:
            pos.append('VTI')
        else:
            pos.append('VT')
    else:
        pos.append('misc')

    if 'style' in li.attrs and li.attrs['style'] == 'font-weight: bold;':
        common.append(True)
    else:
        common.append(False)

df = pd.DataFrame({'root': root, 'pos': pos, 'common': common})[['root', 'pos', 'common']]
df.to_csv('Data/Esperanto/esperanto.csv', index=False)
