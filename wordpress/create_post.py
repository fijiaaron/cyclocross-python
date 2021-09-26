import os 
import base64
import json
import requests
from datetime import datetime

#url = "https://cyclocross.qazar.net/wp-json/wp/v2/posts"
#url = "https://cxmstaging.wpengine.com/wp-json/wp/v2/posts"
url = "https://www.cxmagazine.com/wp-json/wp/v2/posts"

user = "AaronEvansGuru"
password = os.getenv("CX_APPLICATION_PASSWORD")

#### GETTING 403 error but it works on my server


competition = "New Zealand National Championships"
date = "15 Aug 2021"
venue = "Lower Hutt, Wellington"
country = "New Zealand"
category = "Men Elite"
shortcode = "[table id=NewZealandNationalChampionships-MenElite-15Aug2021 /]"
d = datetime.strptime(date, "%d %b %Y")
year = str(d.year)

title = f"{year} {competition} {category} cyclocross results"

content = f'''On {date}, {competition} was hosted at {venue}, {country}. 
Here are the results for {category}.
{shortcode}
'''.format(length='multi-line')

post = {
 'title'    : title,
 'status'   : 'draft', 
 'content'  : content,
}

response = requests.post(url, auth=(user, password), json=post)
print(response)