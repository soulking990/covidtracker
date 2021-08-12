from logging import DEBUG, debug
from typing import Text
from flask.templating import render_template
import requests
import bs4

from flask import Flask

app = Flask(__name__)


def covid():
    global text,numbers
    text = []
    numbers = []
    url = 'https://www.worldometers.info/coronavirus/country/bangladesh/'
    covid_data = requests.get(url)
    soup = bs4.BeautifulSoup(covid_data.text,"lxml")
    content = soup.find("div",class_ = "content-inner").find_all("div", id = "maincounter-wrap")
    for x in content:
        if "<h1>" in str(x):
            iter_text = text.append(x.find("h1", class_ = None).get_text())
            iter_numbers = numbers.append(x.find("span",class_=None).get_text())

covid()

@app.route("/")
def hello_world():
    return "<p>Hey there! want to look at covid data? Try going to /total or /recovered even /deaths is available</p>"

@app.route("/total")
def total():
    return render_template('total.html',text = text,numbers = numbers)

@app.route("/deaths")
def deaths():
    return render_template('deaths.html',text = text,numbers = numbers)

@app.route("/recovered")
def recovered():
    return render_template('recovered.html',text = text,numbers = numbers)


if __name__ == "__main__":
    app.run(debug=True)

