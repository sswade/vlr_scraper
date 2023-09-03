from vlrDB import vlrDB


url = "https://www.vlr.gg/248273/evil-geniuses-vs-edward-gaming-valorant-champions-2023-playoffs-ubqf/"
file = open("vlrtest.html","w")

db = vlrDB()
EG_EDG = db.Match()
EG_EDG.parse_match(url)


print(str(EG_EDG))

file.write(str(EG_EDG))
file.close()

