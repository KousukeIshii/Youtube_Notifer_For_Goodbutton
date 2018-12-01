from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup as bs4

last_good = "0"
cur_good = "0"


app = Flask(__name__)

@app.route('/')
def hello_world():
	global last_good
	global cur_good
	last_good = cur_good
	url = "https://www.youtube.com/channel/UCyMW-_pfjsTG76c9tP5SErg"
	html = requests.get(url)
	soup = bs4(html.text, "lxml")
	a = soup.select_one(".expanded-shelf > .branded-page-module-title > a > span > span")
	if format(a.text == "ライブ配信中") :
		live_element = soup.select_one("div.expanded-shelf.shelf-item > ul > li > div > div.yt-lockup-dismissable > div.yt-lockup-content > h3 > a")
		stream_url = "https://www.youtube.com" + live_element.get("href")
		html = requests.get(stream_url)
		soup = bs4(html.text, "lxml")
		b = soup.select_one("#watch8-sentiment-actions > span > span:nth-of-type(2) > button > span")
		cur_good = b.text
		return render_template('kameme.html', last_good = last_good, cur_good = cur_good)


if __name__ == '__main__':
    app.run()
