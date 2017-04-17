
from bs4 import BeautifulSoup
from selenium import webdriver
from core_algorithm import twTrends

driver = webdriver.Firefox()
trend = twTrends()
print(trend)
if(trend[0][:1] == '#'):
    url = 'https://twitter.com/hashtag/%s filter:verified' % (trend[0][1:])
else:
    url = 'https://twitter.com/hashtag/%s filter:verified' % (trend[0])

driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

#trends = soup.findAll("span", {"class": "username u-dir"})
#print(trends)

handles = []
for span in soup.findAll("span", {"class": "username u-dir"}):
    val = span.find('b').string
    handles.append(val)

handleUnique = list(set(handles))
handleUnique.remove(None)
print(handleUnique)