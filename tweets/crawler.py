import twitter
import configparser
from bs4 import BeautifulSoup
from selenium import webdriver
from core_algorithm import twTrends
configFile = "config.ini"

driver = webdriver.Firefox()
trend = twTrends()
#print(trend)
handles = []
usersDesc = []

config = configparser.ConfigParser()
config.read(configFile)
api = twitter.Api(consumer_key=config['twitter']['consumer_key']
                      , consumer_secret=config['twitter']['consumer_secret']
                      , access_token_key=config['twitter']['access_token_key']
                      , access_token_secret=config['twitter']['access_token_secret'])


for i in range(30):
    if(trend[i][:1] == '#'):
        url = 'https://twitter.com/hashtag/%s filter:verified' % (trend[i][1:])
    else:
        url = 'https://twitter.com/hashtag/%s filter:verified' % (trend[i])

    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    #trends = soup.findAll("span", {"class": "username u-dir"})
    #print(trends)

    #
    for span in soup.findAll("span", {"class": "username u-dir"}):
        val = span.find('b').string
        handles.append(val)
        if(val == None):
            handles.remove(val)

    handleUnique = list(set(handles))
    
#handleUnique.remove(None)
    #print(i)
for user in handleUnique:
    users = api.GetUser(screen_name=user)
    usersDesc.append(user)

print("\n".join(usersDesc))

