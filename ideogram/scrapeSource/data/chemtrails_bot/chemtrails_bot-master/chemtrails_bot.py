import tweepy,random,api_keys,topusers


#		crime   = getRandomLine('crimes.txt')
#		enemy   = getRandomLine('enemies.txt')
#		lair    = getRandomLine('lairs.txt')
#		motive  = getRandomLine('motives.txt')
#		hashtag = getRandomLine('hashtags.txt')


def twitterSetup():
	CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET = api_keys.getKeys()
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)
	return api

def getRandomLine(file):
	with open(file,'r') as f:
		lines = list(f.readlines())
		return random.choice(lines).strip('\n')
		
def gen0(crime,enemy,lair,motive,hashtag):
	tweet=(enemy.capitalize()+' living in '+lair.upper()
			+' '+crime+'! Hurry before they '
			+motive+'! '+hashtag)
	return tweet
	
def gen1(crime,enemy,lair,motive,hashtag):
	tweet=(enemy.capitalize()+' are going to '+motive+'! '
			+'We MUST ambush them at '+lair+". Who's with me?!")
	return tweet
	
def gen2(crime,enemy,lair,motive,hashtag):
	tweet=('Stop the '+enemy.upper()+'!!!!!!!! '+hashtag)
	return tweet
	
def gen3(crime,enemy,lair,motive,hashtag):
	tweet=('txt me for more info about '+enemy+' trying to '
			+motive+'. NSA is reading this')
	return tweet
	
def gen4(crime,enemy,lair,motive,hashtag):
	tweet = (enemy.capitalize()
			+" is taking over before our eyes. THEY "
			+crime+'. '+hashtag)
	return tweet

def gen5(crime,enemy,lair,motive,hashtag):
	tweet = ('Fight the system! '+hashtag)
	return tweet
	
def gen6(crime,enemy,lair,motive,hashtag):
	tweet = (enemy.capitalize()+' is the antichrist! '
			 +"Don't let them "+motive+"! "+hashtag)
	return tweet
	
def buildTweet():
	numGenerators = 6
	n = str(random.randint(0,numGenerators))
	tweet = eval('gen'+n+'(crime,enemy,lair,motive,hashtag)')
	if len(tweet)>140:
		return buildTweet()
	else:
		return tweet

if __name__=='__main__':
	api = twitterSetup()
	print(topusers.getTopUser(api,100000)) 
	tweet=buildTweet()
	print()
	print(tweet)
	print()
	ans = input("Post this tweet? y/n? ")
	if ans=='y':
		api.update_status(tweet)




 