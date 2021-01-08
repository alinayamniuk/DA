import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from tabulate import tabulate

data = pd.read_csv('covid19_by_area_type_hosp_dynamics.csv', delimiter=',')
areas = data['registration_area'].unique()


def crosscorr(x, y, lag):
    corr = x.corr(y)
    max_lag, max_corr = 0, 0
    for i in range(-lag, lag + 1):
        if i == 0:
            continue
        max_corr = x.corr(y.shift(i))
        if corr < max_corr:
            corr = max_corr
            max_lag = i
    return corr, max_lag


def heat(df):
    sns.heatmap(df, cmap=sns.color_palette("magma", as_cmap=True))
    plt.show()


def print_df(df, heading):
    print(f"{heading}\n{tabulate(df, headers='keys', tablefmt='fancy_grid')}")


def parse_df(df):
    sick_by_area = pd.DataFrame()
    for a in df['registration_area'].unique():
        sick_by_area = pd.concat([sick_by_area, df.loc[df['registration_area'] == a].groupby(
            'zvit_date').sum()['active_confirm'].to_frame(name=a)], axis=1).sort_index().fillna(method='ffill').fillna(
            0.0)

    return sick_by_area


def corr_lag_table(df, lag, lag_corr, corr):
    for row in areas:
        for col in areas:
            corr.at[row, col], lag_corr.at[row, col] = crosscorr(df[row], df[col], lag)
    return lag_corr, corr


def chooser(lags, leader):
    avaliable_areas = []
    print('1 - all areas\n2 - selected areas')
    cmd = int(input())

    for area in areas:
        lag = lags.at[leader, area]
        if lag < 0:
            avaliable_areas.append(area)

    if cmd == 1:
        return avaliable_areas
    elif cmd == 2:
        for index, i in enumerate(avaliable_areas):
            print(f"{index + 1} - {i}")
        n = list(map(int, input().split(' ')))
        return [avaliable_areas[i - 1] for i in n]


def scatter(x, y, color):
    plt.scatter(x, y, color=color)


def line(x, y, area, title, color, leg, leader, label=False):
    if label:
        plt.plot(x, y, color=color, label=leg)
        plt.legend()
    else:
        plt.plot(x, y, color=color)
    plt.title(title + ' ' + leader)
    plt.ylabel(area)


def predict_df(sicked, predicted, area):
    dates = sicked.reset_index()['index'].tail(7)
    actual = sicked.reset_index()[area].tail(7)
    pred = list(np.asarray(predicted).flatten())
    df = pd.DataFrame(data={'Date': dates, 'Predicted': pred, 'Actual': actual})
    return df


def make_prediction(lag_table, sick, leader):
    for i in leader:
        print(i)
        leader_area = sick[i]
        selected = chooser(lag_table, i)

        for area in selected:
            analyzed_area = sick[area]

            lag = int(lag_table.at[i, area])

            shifted_area, shifted_leader = analyzed_area.shift(lag)[:lag], leader_area[:lag]

            leader_train, leader_test, shifted_train, shifted_test = train_test_split(shifted_leader, shifted_area,
                                                                                      test_size=7, shuffle=False)
            regression = LinearRegression().fit([[i] for i in leader_train], [[i] for i in shifted_train])

            predict = regression.predict([[i] for i in leader_test])
            line_df = predict_df(analyzed_area, predict, area)

            line(line_df['Date'], line_df['Predicted'], area, '', 'red', 'Predicted', i, True)
            line(line_df['Date'], line_df['Actual'], area, 'Predicted - actual', 'orange', 'Actual', i, True)
            plt.grid()
            plt.xticks(rotation=45)
            plt.show()

            err = np.sqrt(metrics.mean_squared_error(shifted_test, predict)) / np.mean(shifted_area)

            leader_pred = regression.predict([[i] for i in shifted_leader])
            scatter(leader_train, shifted_train, '#8e44ad')
            line(shifted_leader, leader_pred, area, 'Regression - ' + area, 'black', '', ', by leader - ' + i)
            plt.show()

            if err <= 0.25 and abs(lag) >= 8:
                leader_future = leader_area[lag:lag + 7]
                future_pred = regression.predict([[i] for i in leader_future])
                scatter(leader_future, future_pred, '#f1c40f')
                scatter(leader_train, shifted_train, '#8e44ad')
                line(shifted_leader, leader_pred, area, 'Future pred - ' + area, 'black', '', ', by leader - ' + i)
                plt.show()


def main():
    lag_corr, corr = pd.DataFrame(columns=areas, index=areas, dtype='float64'), pd.DataFrame(columns=areas, index=areas,
                                                                                             dtype='float64')
    sick_by_area = parse_df(data)
    # print_df(sick_by_area, 'Sick people by areas: ')
    # print_df(sick_by_area.corr(), 'Correlation (sick by area): ')
    # lag_corr, corr = corr_lag_table(sick_by_area, 250, lag_corr, corr)
    #
    # lag_corr.to_csv('lag_corr.csv')
    # corr.to_csv('corr.csv')
    lag_corr = pd.read_csv('lag_corr.csv', index_col=0)
    corr = pd.read_csv('corr.csv', index_col=0)
    print_df(lag_corr, 'Lag correlation table: ')
    print_df(corr, 'Correlation table: ')
    heat(lag_corr)
    heat(corr)

    top_4 = list(sick_by_area.iloc[-1:].apply(pd.Series.nlargest, axis=1, n=4).columns)
    make_prediction(lag_corr, sick_by_area, top_4)


if __name__ == '__main__':
    main()
