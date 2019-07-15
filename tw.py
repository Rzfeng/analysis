import tweepy as tw
import pandas as pd
import sys
sys.path.append(".")
import config
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

####################################################################
####################################################################
#########################  GET TWEETS  #############################
####################################################################
####################################################################

# OAuth process, using the keys and tokens
auth = tw.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_key, config.access_secret)
# Creation of the actual interface, using authentication
api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
# collect tweets on     #MRT
# for tweet in tweepy.Cursor(api.search,q="MRT",count=100,
#                        lang="en",rpp=100).items():
#     print (tweet.created_at, tweet.text)

# results = api.search(q="quadgraphics")
# for result in results:
#     print(result.place)


#write text file
print("")
print("Choose a twitter key word:")
theInput = input("Key Word: ")
print("")
f= open(str(theInput)+"_twitter.txt","w+")
search_words = str(theInput)
date_since = "2008-6-8"

tweets = tw.Cursor(api.search,
			  q=search_words,
			  lang="en",
			  since=date_since).items(40) #100 items
tweets
dateList = []
locationList = []
tweetList = []
for tweet in tweets:
	locationList.append(tweet.user.location)
	tweetList.append(tweet.text)
	dateList.append(tweet.created_at)
	print(tweet.created_at)
	print(tweet.text)
	print(tweet.user.location)
	print("_______________")

print("")
print(str(len(locationList))+" tweets were found.")
print("")




'''
This function will take a list of strings and return a list of matching polarity score
arg: list of strings
returns: list of polarity scores
'''
def listToSentiment(theList):
	sia = SIA()
	sentimentList = []
	for i in range(len(theList)):
		pol_score = sia.polarity_scores(theList[i])
		sentimentList.append(pol_score["compound"])
	return sentimentList        


'''
Converts a city to a data frame with city, address, and coordinates
Args: locationList (list of cities)
returns: data frame (3 columns: city, address, coordines)
'''
def convertLocationToDF(locationList):
	latitudes = []
	longitudes = []
	allCoordinates = []
	geolocator = Nominatim(user_agent="yo")
	for i in range(len(locationList)):
		if locationList[i] == "Headquarters in Sussex WI":
			locationList[i] = "Sussex, WI"
		location = geolocator.geocode(locationList[i])
		try:
			allCoordinates.append(str(location[1]))
		except:
			allCoordinates.append("No Coordinates")
		if (location != None):
			latitudes.append(location[1][0])
			longitudes.append(location[1][1])
	return allCoordinates, latitudes, longitudes
	
	# geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
	# df = pd.DataFrame(locationList, columns = ['City'])
	# df['Address']=df['City'].apply(geocode, timeout=1000000).apply(lambda x: eval_results(x))
	# df['Coordinates']=df['Address'].apply(lambda loc: tuple(loc.point) if loc else None)
	# return df

#API key to access plotly plots
plotly.tools.set_credentials_file(username='rdundun', api_key='QkSi8PBLrWXRh2pzmzec')

# #get data into latitudes and logitudes
# df = convertLocationToDF(locationList)
# coordinatesList = df['Coordinates'].tolist()
# print(coordinatesList)

# print('a')
# for i in range(len(coordinatesList)):
#   try:
#       latitudes.append(coordinatesList[i][0])
#       longitudes.append(coordinatesList[i][1])
#   except:
#       pass


sentimentList = listToSentiment(tweetList)
total = 0
for i in range(len(sentimentList)):
	total = total + sentimentList[i]

avgSentiment = total/len(sentimentList)



allCoordinates, latitudes, longitudes = convertLocationToDF(locationList)
# with open(str(theInput)+"_twitter.txt", 'w') as f:
#   for i in range(len(tweetList)):
#       f.write("%s\n" % dateList[i])
#       f.write("%s\n" % tweetList[i])
#       f.write("Sentiment: ")
#       f.write("%s\n" % sentimentList[i])
#       f.write("%s\n" % locationList[i])
#       f.write("%s\n" % allCoordinates[i])
#       f.write("%s\n" % "_____________")
#       f.write("%s\n" % "")

with open(str(theInput)+"_twitter.txt", 'w') as f:
	for i in range(len(tweetList)):
		f.write("Date: ")
		f.write(str(dateList[i])+"\n")
		f.write("Tweet Contents: ")
		f.write(str(tweetList[i])+"\n")
		f.write("Tweet Sentiment: ")
		f.write(str(sentimentList[i])+"\n")
		f.write(str(locationList[i])+"\n")
		f.write(str(allCoordinates[i])+"\n")
		f.write("_________________________"+"\n")
		f.write("\n")
	f.write("_________________________"+"\n")
	f.write("\n")
	f.write("%s\n" % "Average Sentiment was: " + str(avgSentiment))

####################################################################
####################################################################
#######################  USA ON MAP ONLY  ##########################
####################################################################
####################################################################
data = [ go.Scattergeo(
		#locationmode = 'USA-states',
		#locationmode = 'ISO-3',
		lon = longitudes,
		lat = latitudes,
		#text = names[:1000],
		mode = 'markers',
		marker = dict( 
			size = 10,
			opacity = 0.8
		))]

layout = dict(
		title = 'Quad Graphics Tweet Locations', 
		geo = dict(
			#scope='usa',
			scope='world',
			projection=dict(type = 'albers usa'),
			#projection=dict(type = 'natural earth'),
			showland = True,
			landcolor = "rgb(250, 250, 250)",
			subunitcolor = "rgb(217, 217, 217)",
			countrycolor = "rgb(217, 217, 217)",
			countrywidth = 0.5,
			subunitwidth = 0.5        
		),
	)


fig = go.Figure(data = data, layout = layout)
py.iplot(fig, filename='business') #plot is at: https://plot.ly/~rdundun/0



# ####################################################################
# ####################################################################
# #####################  WHOLE WORLD ON MAP  #########################
# ####################################################################
# ####################################################################

# data = [ go.Scattergeo(
#         #locationmode = 'USA-states',
#         #locationmode = 'ISO-3',
#         lon = longitudes,
#         lat = latitudes,
#         #text = names[:1000],
#         mode = 'markers',
#         marker = dict( 
#             size = 10,
#             opacity = 0.8
#         ))]

# layout = dict(
#         title = 'Quad Graphics Tweet Locations', 
#         geo = dict(
#             #scope='usa',
#             scope='world',
#             #projection=dict(type = 'albers usa'),
#             projection=dict(type = 'natural earth'),
#             showland = True,
#             landcolor = "rgb(250, 250, 250)",
#             subunitcolor = "rgb(217, 217, 217)",
#             countrycolor = "rgb(217, 217, 217)",
#             countrywidth = 0.5,
#             subunitwidth = 0.5        
#         ),
#     )


# fig = go.Figure(data = data, layout = layout)
# py.iplot(fig, filename='business') #plot is at: https://plot.ly/~rdundun/0

####################################################################
####################################################################
#######################  EUROPE ON MAP  ############################
####################################################################
####################################################################

