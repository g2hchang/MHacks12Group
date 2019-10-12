import fbprophet
import pandas
import matplotlib.pyplot as plt
import csv

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


df = pandas.read_csv('data.csv')
m = fbprophet.Prophet()
m.fit(df)

future = m.make_future_dataframe(periods = 120, freq="H")
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
m.plot(forecast)
plt.show()