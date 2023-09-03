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


file = open("vlrtest.html","w")
f = db.process_event(url,file)

url = 'https://www.vlr.gg/167393/loud-vs-fnatic-champions-tour-2023-lock-in-s-o-paulo-gf'
url = 'https://www.vlr.gg/235556/trace-esports-vs-bilibili-gaming-champions-tour-2023-champions-china-qualifier-ubsf/?game=135287&tab=overview' # won't work due to team name not exsiting, fix it so it pulls the keys automatically from the team page
url = "https://www.vlr.gg/247096/zeta-division-vs-nrg-esports-valorant-champions-2023-group-stage-elim-c/?game=137389&tab=overview"

#EG_EDG = db.Match(url)

#file.write(str(EG_EDG))
file.close()

tst = "EDG ban Lotus; PRX ban Haven; EDG pick Fracture; PRX pick Pearl; EDG ban Split; PRX ban Ascent; Bind remains"

