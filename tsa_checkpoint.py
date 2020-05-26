import matplotlib.pyplot as plt

from bs4 import BeautifulSoup
from datetime import datetime
from urllib.request import Request, urlopen

req = Request('https://www.tsa.gov/coronavirus/passenger-throughput', headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(req).read()

result = []
soup = BeautifulSoup(html, 'lxml')
for row in soup.find_all('tr'):
    result_row = []
    for item in row.find_all('td'):
        result_row.append(item.getText())
    result.append(result_row)

date = []
curr = []
prev = []
xlabel = result[0][0]
y1_label = result[0][1]
y2_label = result[0][2]

for data in reversed(result[1:]):
    if len(data) != 3:
        continue
    date.append(datetime.strptime(data[0], "%m/%d/%Y").date())
    curr.append(int(data[1].replace(',', '')))
    prev.append(int(data[2].replace(',', '')))

fig = plt.figure()
plt.xlabel(xlabel)
plt.ylabel(y1_label)
plt.plot(date, curr, color='red', label='2020')
plt.plot(date, prev, color='blue', label='2019')
plt.gcf().autofmt_xdate(rotation=25)
plt.legend(loc="center right")
plt.savefig('tsa_checkpoint.png')