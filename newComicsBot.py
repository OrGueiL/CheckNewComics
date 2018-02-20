import feedparser
from slackclient import SlackClient


class SlackBot():

	def __init__(self):
		# connect to Slack
		self.slack_token  = ""
		self.slack_client = SlackClient(self.slack_token)


	def send_message_to_slack(self,to,message):
		# https://api.slack.com/methods/chat.postMessage
		# send message to channel or to user
		send = self.slack_client.api_call("chat.postMessage",
			channel=to, 
			text=message,
			username="botname",
			as_user="true"
			)
		return send



class RSS():

	def __init__(self):
		self.url = 'http://feeds.feedburner.com/PlaneteBdLight-ChroniquesComics?format=xml'
		

	def checkRSSFeed(self):
		feed = feedparser.parse(self.url)
		return feed


	def checkLastUpdate(self, date):
		# check and return the last update date in a file
		# create the file if it doesn't exist

		try:
			datefile = open("lastupdate.txt", "r")
			lastupdate = datefile.read() 
		except IOError:
			datefile = open("lastupdate.txt", "w")
			lastupdate = date
			datefile.write(lastupdate)

		datefile.close()

		return lastupdate


	def updateDate(self, date):
		# update the last update date in a file

		datefile = open("lastupdate.txt", "w")
		datefile.write(date)
		datefile.close()


	def checkIfNew(self, date, infos):
		# check if there is a new post in the RSS feed

		post_update = date[0:10] + ' ' + date[11:-1]
		lastupdate = self.checkLastUpdate(post_update)

		if lastupdate < post_update:
			self.updateDate(post_update)
			return True


bot = SlackBot()
flux = RSS()

feed = flux.checkRSSFeed()

for post in reversed(feed['entries']):
	infos = '*' +post['title'] + '* ' + post['id']
	if flux.checkIfNew(post['updated'], infos):
		bot.send_message_to_slack("#exampler",infos)
