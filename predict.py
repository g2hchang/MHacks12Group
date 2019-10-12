import fbprophet
import pandas
import matplotlib.pyplot as plt
import csv
from datetime import datetime, timedelta

THRESHOLD = 160

def get_prediction(timestamp):
    df = pandas.read_csv('data.csv')
    m = fbprophet.Prophet()
    m.fit(df)
    per = 120
    future = m.make_future_dataframe(periods=per, freq="H")
    forecast = m.predict(future)
    prediction, hour = None, None
    distance = float("inf")
    for time in forecast.ds[per:]:
        ts_hour = timestamp.hour
        t_hour = time.hour
        diff = ts_hour - t_hour if ts_hour > t_hour else t_hour - ts_hour
        if diff < distance:
            distance = diff
            hour = time.hour
    for hour, health in enumerate(forecast.yhat):
        if health < THRESHOLD:
            return hour

"""
data = [["ds", "y"]]
for date in ("10", "11", "12", "13", "14"):
    health = 200
    for hour in ("00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"):
        data.append(["2019-10-" + date + " " + hour + ":00:00", health])
        health -= 2
with open("data.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(data)
"""



"""
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
m.plot(forecast)
plt.show()
"""
