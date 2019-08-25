import requests
import json
from bs4 import BeautifulSoup as bs
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_tooltips(query):
    url = "https://api.urbandictionary.com/v0/tooltip?term={}&key=ab71d33b15d36506acf1e379b0ed07ee".format(query)
    r = requests.get(url)
    return json.loads(r.text)['string']

URBAN = "https://www.urbandictionary.com"
r = requests.get(URBAN)
b = bs(r.text, 'html.parser')
section = b.find('div', 'trending-words-panel')
title = section.contents[0].text
li = section.contents[1].contents
words_by_rank = [{x.a.text: [URBAN + x.a.attrs['href'],
                             get_tooltips(x.a.text)]} for x in li]

# Send email
from_email = "yoonoh930@gmail.com"
to_email = "yoonoh930@gmail.com"

msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = title
body_format = """<div><h3><a href={url}>{word}</a></h3></div>
                 <div>{definition}</div>"""
body_list = list(map(lambda x: body_format.format(
                                                  word=next(iter(x)), 
                                                  definition=next(iter(x.values()))[1],
                                                  url=next(iter(x.values()))[0]
                                                  ),
                     words_by_rank))
body = "".join(body_list)
body.replace("\n", "")

html = """\
<html>
  <head></head>
  <body>
    {body}
  </body>
</html>
"""

msg.attach(MIMEText(html.format(body=body), 'html'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(from_email, "DHdbstjr930!")
text = msg.as_string()
server.sendmail(from_email, to_email, text)
server.quit()

    
