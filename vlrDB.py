import pandas as pd
from bs4 import BeautifulSoup
import re 
import requests


### --------- TODO ---------
# Make grabbing team name vs team short name automatic (really only matters for the map veto. right now i can only do champs teams)

na_short = ["100T", "C9", "EG", "NRG", "SEN"]
na_teams = ["100 Thieves", "Cloud9", "Evil Geniuses", "NRG Esports", "Sentinels"]
br_short = ["FUR", "LOUD", "MIBR"]
br_teams = ["Furia", "LOUD", "MIBR"]
lt_short = ["KRÜ", "LEV"]
lt_teams = ["KRÜ Esports", "Leviatán"]
fr_short = ["KC","VIT"]
fr_teams = ["Karmine Corp","Team Vitality"]
es_short = ["GIA","KOI","TH"]
es_teams = ["Giants Gaming", "KOI", "Team Heretics"]
tk_short = ["BBL","FUT"]
tk_teams = ["BBL Esports","FUT Esports"]
nl_short = ["TL"]
nl_teams = ["Team Liquid"]
uk_short = ["FNC"]
uk_teams = ["FNATIC"]
ua_short = ["NAVI"]
ua_teams = ["Natus Vincere"]
kr_short = ["DRX","GEN","T1"]
kr_teams = ["DRX","Gen.G","T1"]
jp_short = ["DFM","ZETA"]
jp_teams = ["DetonatioN FocusMe","ZETA DIVISION"]
sg_short = ["PRX"]
sg_teams = ["Paper Rex"]
ph_short = ["TS"]
ph_teams = ["Team Secret"]
th_short = ["TLN"]
th_teams = ["Talon Esports"]
id_short = ["RRQ"]
id_teams = ["Rex Regum Qeon "]
in_short = ["GE"]
in_teams = ["Global Esports"]
cn_short = ["EDG","FPX","BLG"]
cn_teams = ["EDward Gaming","FunPlus Phoenix","Bilibili Gaming"]
team_names = dict(zip(na_short,na_teams))
team_names.update(dict(zip(br_short,br_teams)))
team_names.update(dict(zip(lt_short,lt_teams)))
team_names.update(dict(zip(fr_short,fr_teams)))
team_names.update(dict(zip(es_short,es_teams)))
team_names.update(dict(zip(tk_short,tk_teams)))
team_names.update(dict(zip(nl_short,nl_teams)))
team_names.update(dict(zip(uk_short,uk_teams)))
team_names.update(dict(zip(ua_short,ua_teams)))
team_names.update(dict(zip(kr_short,kr_teams)))
team_names.update(dict(zip(jp_short,jp_teams)))
team_names.update(dict(zip(sg_short,sg_teams)))
team_names.update(dict(zip(ph_short,ph_teams)))
team_names.update(dict(zip(th_short,th_teams)))
team_names.update(dict(zip(id_short,id_teams)))
team_names.update(dict(zip(in_short,in_teams)))
team_names.update(dict(zip(cn_short,cn_teams)))

teams = na_teams+br_teams+lt_teams+fr_teams+es_teams+tk_teams+uk_teams+ua_teams+nl_teams
short = na_short+br_short+lt_short+fr_short+es_short+tk_short+uk_short+ua_short+nl_short
class vlrDB: 
	"""Basic Structure to operate on Valorant data pulled from VLR"""


	class Match: 
		length = 3
		team1 = None
		team2 = None
		winner = None
		maps = None
		event_series = ""
		match_desc = ""
		map_veto = ""

		map_template = {
			"map" 			: ["_"],
			"winner" 		: ["_"],
			"loser"			: ["_"],
			"map_pick" 	: ["_"],
			"side_pick" : ["_"],
			"team1" 		: ["_"],
			"team1_score" : [0],
			"team2" 		: ["_"],
			"team2_score" : [0],
			"t1_team" 	: ["_"],
			"t1_rounds"	: [0],
			"ct1_team" 	: ["_"],
			"ct1_rounds" : [0],
			"t2_team" 	: ["_"],
			"t2_rounds" : [0],
			"ct2_team"	: ["_"],
			"ct2_rounds" : [0],
			"team1_ot" 	: [0],
			"team2_ot" 	: [0]
			}

		def __init__(self):
			cols = ['map','winner','loser','map_pick','side_pick','team1','team1_score','team2','team2_score','t1_team','t1_rounds','ct1_team','ct1_rounds','t2_team','t2_rounds','ct2_team','ct2_rounds','team1_ot','team2_ot']
			self.maps = pd.DataFrame(columns=cols)
			
		def __str__(self):
			ret = f'{self.event_series} - {self.match_desc} \n'
			ret += self.map_veto + '\n'
			ret += str(self.maps)
			return ret

		def parse_map(self, map_stats):
			info = {}
			map = map_stats(attrs={'class':'map'})
			map = re.search("^([\S]+)",map[0].text.strip())
			map = map.group()
			info['map'] = map
	
			teams_list = map_stats(attrs={'class':'team'})
			# ----- Team 1 -----
			team1_line = teams_list[0] # Tag object that has all the data for Team1
			# Team1 Name
			team1_name = team1_line(attrs={'class':'team-name'})[0] # Tag object for the team name
			info['team1'] = team1_name.text.strip() # Populate Dictionary
			# Team1 Score
			team1_score = team1_line(attrs={'class':'score'})
			t1_score = team1_score[0]
			if 'mod-win' in t1_score.attrs['class']:
				info['winner'] = team1_name.text.strip()
			else: 
				info['loser'] = team1_name.text.strip()
			info['team1_score'] = int(t1_score.text.strip())
			# Assign Team1 to respective sides
			team1_score_list = team1_line('span')
			if 'mod-ct' in team1_score_list[0].attrs['class']:
				info['ct1_team'] = team1_name.text.strip()
				info['ct1_rounds'] = team1_score_list[0].text.strip()
			elif 'mod-t' in team1_score_list[0].attrs['class']:
				info['t1_team'] = team1_name.text.strip()
				info['t1_rounds'] = team1_score_list[0].text.strip()
			if 'mod-ct' in team1_score_list[1].attrs['class']:
				info['ct2_team'] = team1_name.text.strip()
				info['ct2_rounds'] = team1_score_list[1].text.strip()
			elif 'mod-t' in team1_score_list[1].attrs['class']:
				info['t2_team'] = team1_name.text.strip()
				info['t2_rounds'] = team1_score_list[1].text.strip()
			if len(team1_line(attrs={'class':'mod-ot'})) > 0:
				info['team1_ot'] = int(team1_line(attrs={'class':'mod-ot'})[0].text.strip())
			else:
				info['team1_ot'] = 0
	
			# ----- Team 2 -----
			team2_line = teams_list[1]
			# Team2 Name
			team2_name = team2_line(attrs={'class':'team-name'})[0] # Tag object for the team name
			info['team2'] = team2_name.text.strip()
			# Team2 Score
			team2_score = team2_line(attrs={'class':'score'})
			t2_score = team2_score[0]
			if 'mod-win' in t2_score.attrs['class']:
				info['winner'] = team2_name.text.strip()
			else: 
				info['loser'] = team2_name.text.strip()
			info['team2_score'] = int(t2_score.text.strip())
			# Assign Team2 to respective sides
			team2_score_list = team2_line('span')
			if 'mod-ct' in team2_score_list[0].attrs['class']:
				info['ct1_team'] = team2_name.text.strip()
				info['ct1_rounds'] = team2_score_list[0].text.strip()
			elif 'mod-t' in team2_score_list[0].attrs['class']:
				info['t1_team'] = team2_name.text.strip()
				info['t1_rounds'] = team2_score_list[0].text.strip()
			if 'mod-ct' in team2_score_list[1].attrs['class']:
				info['ct2_team'] = team2_name.text.strip()
				info['ct2_rounds'] = team2_score_list[1].text.strip()
			elif 'mod-t' in team2_score_list[1].attrs['class']:
				info['t2_team'] = team2_name.text.strip()
				info['t2_rounds'] = team2_score_list[1].text.strip()
			if len(team2_line(attrs={'class':'mod-ot'})) > 0:
				info['team2_ot'] = int(team2_line(attrs={'class':'mod-ot'})[0].text.strip())
			else: 
				info['team2_ot'] = 0

			df = pd.DataFrame(info,index=[0])
			return df

		def parse_match(self, url):
			page = requests.get(url)
			soup = BeautifulSoup(page.text, 'html.parser')
			maps = soup(attrs={"class":"vm-stats-game"}) # contains m+1 items where m is the number of maps available (3 in BO3, 5 in BO5)
			for map_line in maps:
				if map_line.attrs['data-game-id']=='all':
					pass
				else:
					self.maps = pd.concat([self.maps,self.parse_map(map_line)],ignore_index=True)
			self.winner = self.maps['winner'].mode()[0]
			self.team1 = self.maps['team1'].mode()[0]
			self.team2 = self.maps['team2'].mode()[0]
			self.event_series = soup(attrs={"class":"match-header-event-series"})[0].previous_sibling.previous_sibling.text.strip()
			self.event_series = re.sub("\s+"," ",self.event_series)
			self.match_desc = soup(attrs={"class":"match-header-event-series"})[0].text.strip()
			self.match_desc = re.sub("\s+"," ",self.match_desc)
			self.map_veto = soup(attrs={"class":"match-header-note"})[0].text.strip()
			self.map_veto = re.sub("\s+"," ",self.map_veto)
			split = self.map_veto.split('; ')
			picks = []
			for entry in split:
				if 'pick' in entry:
					picks.append(entry)
			for x in range(len(self.maps.index)):
				if x == len(picks):
					self.maps.at[x,"map_pick"] = 'remains'
					self.maps.at[x,"side_pick"] = self.maps.at[0,"map_pick"]
				else:
					team = team_names[picks[x].split()[0]]
					self.maps.at[x,"map_pick"] = team
					if team == self.team1:
						self.maps.at[x,"side_pick"] = self.team2
					elif team == self.team2:
						self.maps.at[x,"side_pick"] = self.team1

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

	#def __init__(self):
	#	AMER = []
	#	for name, short in zip(self.na_teams,self.na_short):
	#		AMER.append(self.Team(name, short, "AMER","NA")) 
	#	for name, short in zip(self.br_teams,self.br_short):
	#		AMER.append(self.Team(name, short, "AMER","BR")) 
	#	for name, short in zip(self.lt_teams,self.lt_short):
	#		AMER.append(self.Team(name, short, "AMER","LT"))
#
	#	EMEA =[]
	#	for name, short in zip(self.fr_teams,self.fr_short):
	#		EMEA.append(self.Team(name, short, "EMEA","FR")) 
	#	for name, short in zip(self.es_teams,self.es_short):
	#		EMEA.append(self.Team(name, short, "EMEA","ES")) 
	#	for name, short in zip(self.tk_teams,self.tk_short):
	#		EMEA.append(self.Team(name, short, "EMEA","TK")) 
	#	for name, short in zip(self.nl_teams,self.nl_short):
	#		EMEA.append(self.Team(name, short, "EMEA","NL")) 
	#	for name, short in zip(self.uk_teams,self.uk_short):
	#		EMEA.append(self.Team(name, short, "EMEA","UK")) 
	#	for name, short in zip(self.ua_teams,self.ua_short):
	#		EMEA.append(self.Team(name, short, "EMEA","UA")) 
#
	#	#do apac...
#
	#	regions = [AMER,"APAC",EMEA]
	
