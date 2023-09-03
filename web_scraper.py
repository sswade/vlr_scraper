from urllib.request import urlopen
import re 

raw = open("raw_no_comments.html","w") # Not super modified so i don't have to keep pulling this HTML request every time, though I guess it really doesn't matter... 

url = "https://www.vlr.gg/248273/evil-geniuses-vs-edward-gaming-valorant-champions-2023-playoffs-ubqf/"
page = urlopen(url)

html_bytes = page.read()
html = html_bytes.decode("utf-8")

html = re.sub("<!--.*?-->", "", html) # Remove HTML comments

raw.write(html)
raw.close()
