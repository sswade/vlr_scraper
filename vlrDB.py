import pandas as pd
from bs4 import BeautifulSoup
import re 
import requests


class vlrDB: 
	"""Basic Structure to operate on Valorant data pulled from VLR"""
	na_short = ["100T", "C9", "EG", "NRG", "SEN"]
	na_teams = ["100 Thieves", "Cloud 9", "Evil Geniuses", "NRG", "Sentinels"]
	br_short = ["FUR", "LOUD", "MIBR"]
	br_teams = ["Furia", "LOUD", "Made In Brazil"]
	lt_short = ["KRU", "LEV"]
	lt_teams = ["KRU", "Leviatan"]

	fr_short = ["KC","VIT"]
	fr_teams = ["Karmine Corp","Team Vitality"]
	es_short = ["GIA","KOI","TH"]
	es_teams = ["Giants", "KOI", "Team Heratics"]
	tk_short = ["BBL","FUT"]
	tk_teams = ["BBL","FUT"]
	nl_short = ["TL"]
	nl_teams = ["Team Liquid"]
	uk_short = ["FNC"]
	uk_teams = ["FNATIC"]
	ua_short = ["NAVI"]
	ua_teams = ["Natus Vincere"]

	teams = na_teams+br_teams+lt_teams+fr_teams+es_teams+tk_teams+uk_teams+ua_teams+nl_teams
	short = na_short+br_short+lt_short+fr_short+es_short+tk_short+uk_short+ua_short+nl_short

	class Match: 
		length = 3
		team1 = None
		team2 = None
		winner = None
		maps = None
		event_series = ""
		match_desc = ""
		map_veto = ""

		def __init__(self):
			map_template = {
				"map" : ["_","_","_"],
				"winner" : ["_","_","_"],
				"loser"  : ["_","_","_"],
				"map_pick" : ["_","_","_"],
				"side_pick" : ["_","_","_"],
				"team1" : ["_","_","_"],
				"team1_score" : [0,0,0],
				"team2" : ["_","_","_"],
				"team2_score" : [0,0,0],
				"attack1_team" : ["_","_","_"],
				"attack1_rounds" : [0,0,0],
				"defense1_team" : ["_","_","_"],
				"defense1_rounds" : [0,0,0],
				"attack2_team" : ["_","_","_"],
				"attack2_rounds" : [0,0,0],
				"defense2_team": ["_","_","_"],
				"defense2_rounds" : [0,0,0],
				"team1_ot" :  [0,0,0],
				"team2_ot" : [0,0,0]
				}
			self.maps = pd.DataFrame(map_template)
			
		def __str__(self):
			ret = f'{self.event_series} - {self.match_desc} \n'
			ret += self.map_veto + '\n'
			ret += str(self.maps)
			return ret

		def parse_map(self, map_number, map_stats):
			map = map_stats(attrs={'class':'map'})
			map = re.search("^([\S]+)",map[0].text.strip())
			map = map.group()
			self.maps.loc[self.maps.index[map_number], 'map'] = map
	
			teams_list = map_stats(attrs={'class':'team'})
			# ----- Team 1 -----
			team1_line = teams_list[0] # Tag object that has all the data for Team1
			# Team1 Name
			team1_name = team1_line(attrs={'class':'team-name'})[0] # Tag object for the team name
			self.maps.loc[self.maps.index[map_number], 'team1'] = team1_name.text.strip() # Populate Dictionary
			# Team1 Score
			team1_score = team1_line(attrs={'class':'score'})
			t1_score = team1_score[0]
			if 'mod-win' in t1_score.attrs['class']:
				self.maps.loc[self.maps.index[map_number], 'winner'] = team1_name.text.strip()
			else: 
				self.maps.loc[self.maps.index[map_number], 'loser'] = team1_name.text.strip()
			self.maps.loc[self.maps.index[map_number], 'team1_score'] = int(t1_score.text.strip())
			# Assign Team1 to respective sides
			team1_score_list = team1_line('span')
			if 'mod-ct' in team1_score_list[0].attrs['class']:
				self.maps.loc[self.maps.index[map_number], 'defense1_team'] = team1_name.text.strip()
				self.maps.loc[self.maps.index[map_number], 'defense1_rounds'] = team1_score_list[0].text.strip()
			elif 'mod-t' in team1_score_list[0].attrs['class']:
				self.maps.loc[self.maps.index[map_number], 'attack1_team'] = team1_name.text.strip()
				self.maps.loc[self.maps.index[map_number], 'attack1_rounds'] = team1_score_list[0].text.strip()
			if 'mod-ct' in team1_score_list[1].attrs['class']:
				self.maps.loc[self.maps.index[map_number], 'defense2_team'] = team1_name.text.strip()
				self.maps.loc[self.maps.index[map_number], 'defense2_rounds'] = team1_score_list[1].text.strip()
			elif 'mod-t' in team1_score_list[1].attrs['class']:
				self.maps.loc[self.maps.index[map_number], 'attack2_team'] = team1_name.text.strip()
				self.maps.loc[self.maps.index[map_number], 'attack2_rounds'] = team1_score_list[1].text.strip()
			if len(team1_line(attrs={'class':'mod-ot'})) > 0:
				self.maps.loc[self.maps.index[map_number], 'team1_ot'] = int(team1_line(attrs={'class':'mod-ot'})[0].text.strip())
	
			# ----- Team 2 -----
			team2_line = teams_list[1]
			team2_name = team2_line(attrs={'class':'team-name'})[0] # Tag object for the team name
			self.maps.loc[self.maps.index[map_number], 'team2'] = team2_name.text.strip()
			#team2_it = team2_line.contents
			team2_score = team2_line(attrs={'class':'score'})
			t2_score = team2_score[0]
			if 'mod-win' in t2_score.attrs['class']:
				self.maps.loc[self.maps.index[map_number], 'winner'] = team2_name.text.strip()
			else: 
				self.maps.loc[self.maps.index[map_number], 'loser'] = team2_name.text.strip()
				self.maps.loc[self.maps.index[map_number], 'team2_score'] = int(t2_score.text.strip())
			# Assign Team2 to respective sides
			team2_score_list = team2_line('span')
			if 'mod-ct' in team2_score_list[0].attrs['class']:
				self.maps.loc[self.maps.index[map_number], 'defense1_team'] = team2_name.text.strip()
				self.maps.loc[self.maps.index[map_number], 'defense1_rounds'] = team2_score_list[0].text.strip()
			elif 'mod-t' in team2_score_list[0].attrs['class']:
				self.maps.loc[self.maps.index[map_number], 'attack1_team'] = team2_name.text.strip()
				self.maps.loc[self.maps.index[map_number], 'attack1_rounds'] = team2_score_list[0].text.strip()
			if 'mod-ct' in team2_score_list[1].attrs['class']:
				self.maps.loc[self.maps.index[map_number], 'defense2_team'] = team2_name.text.strip()
				self.maps.loc[self.maps.index[map_number], 'defense2_rounds'] = team2_score_list[1].text.strip()
			elif 'mod-t' in team2_score_list[1].attrs['class']:
				self.maps.loc[self.maps.index[map_number], 'attack2_team'] = team2_name.text.strip()
				self.maps.loc[self.maps.index[map_number], 'attack2_rounds'] = team2_score_list[1].text.strip()
			if len(team2_line(attrs={'class':'mod-ot'})) > 0:
				self.maps.loc[self.maps.index[map_number], 'team2_ot'] = int(team2_line(attrs={'class':'mod-ot'})[0].text.strip())

		def parse_match(self, url):
			page = requests.get(url)
			soup = BeautifulSoup(page.text, 'html.parser')
			maps = soup(attrs={"class":"vm-stats-game"}) # contains m+1 items where m is the number of maps available (3 in BO3, 5 in BO5)
			self.parse_map(0, maps[0]) # index 1 is "all map stats"
			self.parse_map(1, maps[2])
			self.parse_map(2, maps[3])
			self.winner = self.maps['winner'].mode()
			self.team1 = self.maps['team1'].mode()
			self.team2 = self.maps['team2'].mode()
			self.event_series = soup(attrs={"class":"match-header-event-series"})[0].previous_sibling.previous_sibling.text.strip()
			self.event_series = re.sub("\s+"," ",self.event_series)
			self.match_desc = soup(attrs={"class":"match-header-event-series"})[0].text.strip()
			self.match_desc = re.sub("\s+"," ",self.match_desc)
			self.map_veto = soup(attrs={"class":"match-header-note"})[0].text.strip()
			self.map_veto = re.sub("\s+"," ",self.map_veto)

	class Team:
		name = ""
		short = ""
		region = ""
		subregion = ""
		players = []
		matches = []
		def __init__(self,name, short,region,subregion):
			self.name = name
			self.short = short
			self.region = region
			self.subregion = subregion

	def __init__(self):
		AMER = []
		for name, short in zip(self.na_teams,self.na_short):
			AMER.append(self.Team(name, short, "AMER","NA")) 
		for name, short in zip(self.br_teams,self.br_short):
			AMER.append(self.Team(name, short, "AMER","BR")) 
		for name, short in zip(self.lt_teams,self.lt_short):
			AMER.append(self.Team(name, short, "AMER","LT"))

		EMEA =[]
		for name, short in zip(self.fr_teams,self.fr_short):
			EMEA.append(self.Team(name, short, "EMEA","FR")) 
		for name, short in zip(self.es_teams,self.es_short):
			EMEA.append(self.Team(name, short, "EMEA","ES")) 
		for name, short in zip(self.tk_teams,self.tk_short):
			EMEA.append(self.Team(name, short, "EMEA","TK")) 
		for name, short in zip(self.nl_teams,self.nl_short):
			EMEA.append(self.Team(name, short, "EMEA","NL")) 
		for name, short in zip(self.uk_teams,self.uk_short):
			EMEA.append(self.Team(name, short, "EMEA","UK")) 
		for name, short in zip(self.ua_teams,self.ua_short):
			EMEA.append(self.Team(name, short, "EMEA","UA")) 

		#do apac...

		regions = [AMER,"APAC",EMEA]
	
