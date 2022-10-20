from flask import Flask,jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime
app= Flask(__name__)

@app.route('/getstories')
def get_response():
  res = requests.get("https://www.time.com")
  soup = BeautifulSoup(res.text,'html.parser')
  stories_li = soup.find('div',{'class':'latest-stories'}).find_all('li')
  title_links = [(el.find('h3').text,f"https://time.com{el.find('a')['href']}") for el in stories_li ]
  timest = [datetime.strptime(el.find('time').text.strip()[:-4],'%B %d, %Y • %I:%M %p') for el in stories_li ]
  k = []
  for i in zip(timest,title_links):
    k.append(i)
  res = []
  for m in sorted(k,reverse=True):
    res.append({
        'title':m[1][0],
        'link':m[1][1]
    })
  return jsonify(res[:5])
app.run(debug=True,port=5000)