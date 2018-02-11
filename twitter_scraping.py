import tweepy
from textblob import TextBlob
import sys
import matplotlib.pyplot as plt
import pprint

consumer_key=''
consumer_secret=''
access_token=''
access_token_secret=''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)
 
a=int(input('''What you want to do
		1)Display tweets having particular term
		2)Tweet something
		3)Sentimental Analysis of a term/Hashtag
		4)timeline of a particular user'''))


			

def update_status():
	tweet=input('Enter your tweet in 140 words')
	if len(tweet)>140:
		print('Maximum length exceded')
	else:
		api.update_status(tweet)
		print('Tweeted')


def stream_tweets():
	search_for=input('Enter the term/hastag')
	noOfterms=int(input('Number of tweets'))

	tweets=tweepy.Cursor(api.search,q=search_for,lang='English').items(noOfterms)

	for tweet in tweets:
		pprint.pprint(tweet.text)

def timeline():
	screen=input('Enter the username of the user ')
	a='' 
	for status in tweepy.Cursor(api.user_timeline, screen_name=screen).items():
		
		c=status._json['text']
		a=a+c
	with open('all_tweets.txt','w') as f:
		f.write(a)
		f.close()	
	print('Tweets stored in all_tweets.txt file')		


def percentage(part,whole):
	return 100*(float(part)/float(whole))

def sentimental_analysis():
	
	search_for=input('Enter the term/hastag')
	
	noOfterms=int(input('Number of tweets'))
	
	tweets=tweepy.Cursor(api.search,q=search_for,lang='English').items(noOfterms)
	
	positive=0
	negative=0
	neutral=0
	polarity=0

	for tweet in tweets:
		analysis=TextBlob(tweet.text)
		polarity+=analysis.sentiment.polarity

		if analysis.sentiment.polarity==0:
			neutral+=1
		elif analysis.sentiment.polarity>0.00:
			positive+=1
		elif analysis.sentiment.polarity<0.00:
			negative+=1	

	labels = 'Positive', 'Negative', 'Neutral'
	sizes = [positive,negative, neutral]
	colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
	explode = (0.1, 0, 0)  
	 
	
	plt.pie(sizes, explode=explode, labels=labels, colors=colors,
	        autopct='%1.1f%%', shadow=True, startangle=140)
	 
	plt.axis('equal')
	plt.show()
if a==1:
	stream_tweets()
	
elif a==2:
	update_status()
	
elif a==3:
	sentimental_analysis()
	
elif a==4:
	timeline()
else:
	print('Not a Valid')
