from logging import DEBUG, debug
from typing import Text
from flask.templating import render_template
import requests
import re
import statistics


from flask import Flask

app = Flask(__name__)

# GET THE API
covid = requests.get('https://api.covid19api.com/dayone/country/bangladesh/status/confirmed')
#MAKE THE API INTO A DICTIONARY
data = covid.json()
#INDEX THE LIST OF DICTIONARIES TO GET ONE WEEK OF SAID API
week_data = data[-7::1]

#this takes in a list of dictionaries and goes through the dictionaires to index it to find the cases and then appends it to a list
def data_finder(data,slice="Cases"):
    result = []
    for dict in data:
        result.append(dict[slice])
    return result

#y axis of all cases
all_y_axis = data_finder(data)
#used a pattern of the date to find the x axis (or labels)
pattern = re.compile(r"\d\d\d\d-\d\d-\d\d")
all_x_axis = re.findall(pattern, str(data))

#y axis of one week of data(the actual cases)
week_y = all_y_axis[-7::1]
#x axis of one week of data (the dates)
week_x = re.findall(pattern,str(week_data))

data_14 = all_y_axis[-14::1]

def sevenday(data):
    result = []
    for x in range(len(data)):
        result.append(statistics.mean(data[x:(7+x)]))
    return result
all_average =sevenday(all_y_axis)


        

def indexer(data):
    result = []
    for x in range(1,8):
        seven = data[x:(7+x)]
        mean = statistics.mean(seven)
        result.append(mean)
    return result
    
mean_data = indexer(data_14)


@app.route("/")
def hello_world():
    return render_template('all.html', x = all_x_axis, y = all_y_axis,all = all_average)

@app.route("/week")
def week():
    return render_template('week.html',  x = week_x, y = week_y, mean_data = mean_data)

if __name__ == "__main__":
    app.run(debug=True)

