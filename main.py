from logging import DEBUG, debug
from typing import Text
from flask.templating import render_template
import requests
import re
from matplotlib import pyplot as plt
import seaborn as sns


from flask import Flask

app = Flask(__name__)


covid = requests.get('https://api.covid19api.com/live/country/bangladesh')
data = covid.json()
week_data = data[-7::1]

def deaths(data):
    result = []
    for day in data:
        result.append(day['Deaths'])
    return result

x_axis =deaths(week_data)

pattern = re.compile(r"\d\d\d\d-\d\d-\d\d")
y_axis = re.findall(pattern, str(week_data))

@app.route("/")
def hello_world():
    return render_template('layout.html', x = x_axis, y = y_axis)



if __name__ == "__main__":
    app.run(debug=True)

