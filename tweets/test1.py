import twitter
import configparser
configFile = "config.ini"
import re

config = configparser.ConfigParser()
config.read(configFile)
api = twitter.Api(consumer_key=config['twitter']['consumer_key']
                      , consumer_secret=config['twitter']['consumer_secret']
                      , access_token_key=config['twitter']['access_token_key']
                      , access_token_secret=config['twitter']['access_token_secret'])

users = api.GetUser(screen_name='vcolliver')
#trends = api.GetTrendsWoeid(woeid=2459115)

#print(trends)
new_ = str(users)
new1 =re.search(r'^"description:"\."$' ,new_)
#new1 = new_.split("description:")
print(users.description)
#print(users)