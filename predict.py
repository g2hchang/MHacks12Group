import fbprophet
import pandas
import requests
import matplotlib.pyplot as plt
import csv
from datetime import datetime, timedelta

THRESHOLD = 120
per = 120

def get_prediction(timestamp, predict = True):
    forecast = pandas.read_json('forecast.json')
    if predict:
        data = requests.get("https://mhacks12-c37e8.firebaseio.com/users/.json")

        df = pandas.read_json(data.content)
        #df = pandas.read_csv("data2.csv")
        m = fbprophet.Prophet()
        m.fit(df)
        future = m.make_future_dataframe(periods=per, freq="H")
        forecast = m.predict(future)
        forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
        m.plot(forecast)
        #plt.show()
        forecast.to_json("forecast.json")
    prediction, hour = None, None
    distance = float("inf")
    for time in forecast.ds[per:]:
        ts_hour = timestamp.hour
        t_hour = time.hour
        diff = ts_hour - t_hour if ts_hour > t_hour else t_hour - ts_hour
        if diff < distance:
            distance = diff
            hour = time.hour
    for hour, health in enumerate(forecast.yhat if predict else forecast.y):
        if health < THRESHOLD:
            return hour

import random
data = [["ds", "y"]]
for date in ("07", "08", "09", "10", "11"):
    health = 95
    for hour in ("00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"):
        data.append(["2019-10-" + date + " " + hour + ":00:00", health])
        health -= random.randrange(1, 5)

with open("data2.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(data)


if __name__ == '__main__':
    get_prediction(datetime.now())
    pass



