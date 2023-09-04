from vlrDB import vlrDB
import re
import pandas as pd
from bs4 import BeautifulSoup
import requests

db = vlrDB()
url = "https://www.vlr.gg/248273/evil-geniuses-vs-edward-gaming-valorant-champions-2023-playoffs-ubqf/"
url = "https://www.vlr.gg/247077/paper-rex-vs-edward-gaming-valorant-champions-2023-group-stage-winners-a"
url = "https://www.vlr.gg/232735/kr-esports-vs-leviat-n-champions-tour-2023-americas-last-chance-qualifier-gf"
url = 'https://www.vlr.gg/167393/loud-vs-fnatic-champions-tour-2023-lock-in-s-o-paulo-gf'

url = "https://www.vlr.gg/event/matches/1657/valorant-champions-2023/?series_id=all"
#url = 'https://www.vlr.gg/event/matches/1657/valorant-champions-2023/?series_id=3264'

def ascent_champs_lcq_masters():
	file = open("vlrtest.html","w")
	champs = db.Event(url)
	champs.data.to_html('champs.html')
	
	url = 'https://www.vlr.gg/event/matches/1658/champions-tour-2023-americas-last-chance-qualifier'
	amerlcq = db.Event(url)
	amerlcq.data.to_html('amerlcq.html')
	
	url = 'https://www.vlr.gg/event/matches/1659/champions-tour-2023-emea-last-chance-qualifier'
	emealcq = db.Event(url)
	emealcq.data.to_html('emealcq.html')
	
	url = 'https://www.vlr.gg/event/matches/1660/champions-tour-2023-pacific-last-chance-qualifier'
	apaclcq = db.Event(url)
	apaclcq.data.to_html('apaclcq.html')
	
	url = 'https://www.vlr.gg/event/matches/1494/champions-tour-2023-masters-tokyo/?series_id=all'
	tokyo = db.Event(url)
	tokyo.data.to_html('tokyo.html')
	
	combined = db.combine_events([champs,amerlcq,emealcq,apaclcq,tokyo])
	ascent = combined[(combined['map'] == 'Ascent')]
	ascent.to_html('ascent.html')

#url = "https://www.vlr.gg/237267/rex-regum-qeon-vs-global-esports-champions-tour-2023-pacific-last-chance-qualifier-ubqf/?game=135652&tab=overview"
#match = db.Match(url)
#
#url = 'https://www.vlr.gg/167393/loud-vs-fnatic-champions-tour-2023-lock-in-s-o-paulo-gf'
#url = 'https://www.vlr.gg/235556/trace-esports-vs-bilibili-gaming-champions-tour-2023-champions-china-qualifier-ubsf/?game=135287&tab=overview' # won't work due to team name not exsiting, fix it so it pulls the keys automatically from the team page
#url = "https://www.vlr.gg/247096/zeta-division-vs-nrg-esports-valorant-champions-2023-group-stage-elim-c/?game=137389&tab=overview"

#EG_EDG = db.Match(url)

file.write(str(match))
file.close()
