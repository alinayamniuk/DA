import pandas as pd
import datetime as dt
import KN310Yamniuk2


columns = ['Date', 'Time', 'Temperature', 'Dew Point', 'Humidity', 'Wind', 'Wind Speed', 'Wind Gust', 'Pressure', 'Precip.', 'Precip Accum', 'Condition']


def parse():
    data = pd.read_csv('DATABASE.csv', delimiter=';', names=columns, skiprows=1)
    for index, date in enumerate(data['Date']):
        data['Date'].at[index] = dt.datetime.strptime(date, '%d.%b').strftime('%d-%m-2019')

    for index, time in enumerate(data['Time']):
        data['Time'].at[index] = dt.datetime.strptime(time, '%I:%M %p').strftime('%H:%M')

    for index, hum in enumerate(data['Humidity']):
        data['Humidity'].at[index] = int(hum.replace('%', '')) / 100

    for index, wind in enumerate(data['Wind Speed']):
        data['Wind Speed'].at[index] = int(wind.replace('mph', ''))
        data['Wind Gust'].at[index] = int(wind.replace('mph', ''))

    for index, pressure in enumerate(data['Pressure']):
        data['Pressure'].at[index] = float(pressure.replace(',', '.'))
    print(data)
    data.set_index('Date', inplace=True, drop=True)
    return data


data = parse()
KN310Yamniuk2.visualization(data)