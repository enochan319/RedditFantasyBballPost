import praw
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
import smtplib
import schedule as schedule
import time


stat_date = (datetime.datetime.today()  + datetime.timedelta(-1)).strftime("%A, %B %d, %Y")

post_title = 'NBA box score rankings for ' + str(stat_date) # this is the post title
post_intro = 'Hello r/fantasybball, here are the box scores sorted by 9 CAT rankings for last night! These stats have been scraped from BBM\'s box score page! \n\n' # this is the post text/body


#scrapes BBM box scores and sorts by ranking
def BBM_Webscrape():
	global post_body 
	post_body = ''
	post_body += post_intro
	post_body += 'Rank | Player | Points | 3PTM | Rebounds | Assists | Steals | Blocks | Turnover | FG% | FT% \n :--|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--| \n '
	my_url = 'https://basketballmonster.com/Boxscores.aspx'
	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "html.parser")
	rankings = page_soup.findAll("tr")

	stats_container = []

	for x in range(len(rankings)):

		a = {}
		# player name
		try:
			checking_ranking_integer = int(rankings[x].findAll(attrs={'class':"tdr"})[0].text.split()[0])
		except:
			continue
		if checking_ranking_integer == 0:
			continue

		try:	
			a['name'] = rankings[x].findAll("a")[0].text.strip()
			a['rank'] = rankings[x].findAll(attrs={'class':"tdr"})[0].text.split()[0]
			
			a['min'] = rankings[x].findAll(attrs={'class':"tdr"})[4].text.split()[0]
			a['pts'] = rankings[x].findAll(attrs={'class':"tdr"})[5].text.split()[0]
			a['3'] = rankings[x].findAll(attrs={'class':"tdr"})[6].text.split()[0]
			a['reb'] = rankings[x].findAll(attrs={'class':"tdr"})[7].text.split()[0]
			a['ast'] = rankings[x].findAll(attrs={'class':"tdr"})[8].text.split()[0]
			a['stl'] = rankings[x].findAll(attrs={'class':"tdr"})[9].text.split()[0]
			a['blk'] = rankings[x].findAll(attrs={'class':"tdr"})[10].text.split()[0]
			a['fg%'] = rankings[x].findAll(attrs={'class':"tdr"})[11].text.split()[0]
			a['fga'] = rankings[x].findAll(attrs={'class':"tdr"})[12].text.split()[0]
			a['ft%'] = rankings[x].findAll(attrs={'class':"tdr"})[13].text.split()[0]
			a['fta'] = rankings[x].findAll(attrs={'class':"tdr"})[14].text.split()[0]
			a['to'] = rankings[x].findAll(attrs={'class':"tdr"})[15].text.split()[0]
			a['pf'] = rankings[x].findAll(attrs={'class':"tdr"})[16].text.split()[0]
			a['USG'] = rankings[x].findAll(attrs={'class':"tdr"})[17].text.split()[0]
			a['pV'] = rankings[x].findAll(attrs={'class':"tdr"})[18].text.split()[0]
			a['3V'] = rankings[x].findAll(attrs={'class':"tdr"})[19].text.split()[0]
			a['rV'] = rankings[x].findAll(attrs={'class':"tdr"})[20].text.split()[0]
			a['aV'] = rankings[x].findAll(attrs={'class':"tdr"})[21].text.split()[0]
			a['sV'] = rankings[x].findAll(attrs={'class':"tdr"})[22].text.split()[0]
			a['bV'] = rankings[x].findAll(attrs={'class':"tdr"})[23].text.split()[0]
			a['fg%V'] = rankings[x].findAll(attrs={'class':"tdr"})[24].text.split()[0]
			a['ft%V'] = rankings[x].findAll(attrs={'class':"tdr"})[25].text.split()[0]
			a['toV'] = rankings[x].findAll(attrs={'class':"tdr"})[26].text.split()[0]
			stats_container.append(a)
		except:
			continue

	stats_container_reordered = []

	for i in range(len(stats_container)):
		for z in range(len(stats_container)):
			if i == int(stats_container[z]['rank']):
				stats_container_reordered.append(stats_container[z])

	for i in range(len(stats_container_reordered)):
		message = stats_container_reordered[i]['rank'] + ' | ' + stats_container_reordered[i]['name'] + ' | '
		keys = ['pts','3','reb','ast', 'stl', 'blk', 'to', 'fg%', 'ft%']
		unit_plural = ['points', '3PTM', 'rebounds', 'assists', 'steals', 'blocks', 'turnovers']
		unit_singular = ['point', '3PTM', 'rebound', 'assist', 'steal', 'block', 'turnover']
		for y in range(len(keys)):
			if keys[y] == 'fg%':
				message += str(round(float(stats_container_reordered[i][keys[y]])*100,0)) + '% | '
			elif keys[y] == 'ft%':
				message += str(round(float(stats_container_reordered[i][keys[y]])*100,0)) + '% '
			else:
				message += str(stats_container_reordered[i][keys[y]]) +  ' | '
		message += '\n '				
		post_body += message
	return(post_body)

#reddit api creditentials
reddit = praw.Reddit(
    client_id='##############',
    client_secret='##############',
    username='##############',
    password='##############',
    user_agent="##############")



#authenticate to reddit
def authenticate(reddit):
    print(reddit.user.me())

#posts to reddit
def self_post():
    reddit.subreddit('fantasybball').submit(title=post_title, selftext=post_body)


if __name__ == '__main__':
    authenticate(reddit)
    BBM_Webscrape()
    self_post()
    #print(post_body)