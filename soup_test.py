from vlrDB import vlrDB
import re


url = "https://www.vlr.gg/248273/evil-geniuses-vs-edward-gaming-valorant-champions-2023-playoffs-ubqf/"
url = "https://www.vlr.gg/247077/paper-rex-vs-edward-gaming-valorant-champions-2023-group-stage-winners-a"
url = "https://www.vlr.gg/232735/kr-esports-vs-leviat-n-champions-tour-2023-americas-last-chance-qualifier-gf"
url = 'https://www.vlr.gg/167393/loud-vs-fnatic-champions-tour-2023-lock-in-s-o-paulo-gf'
file = open("vlrtest.html","w")

db = vlrDB()
EG_EDG = db.Match()
EG_EDG.parse_match(url)


print(str(EG_EDG))

file.write(str(EG_EDG))
file.close()

tst = "EDG ban Lotus; PRX ban Haven; EDG pick Fracture; PRX pick Pearl; EDG ban Split; PRX ban Ascent; Bind remains"

