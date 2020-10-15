import matplotlib.pyplot as plt


def line(df, type):
    df.plot(kind='line', y=type, figsize=(12, 10), linewidth=1.5, color='maroon')
    plt.xlabel("Date", fontsize=18)
    plt.ylabel(type, fontsize=18)
    plt.title(type + " - line graphic", fontsize=21)
    plt.show()


def scatter(df, type):
    df.reset_index().plot(kind='scatter', y=type, x='Date', figsize=(12, 12), s=100)
    plt.title(type + " - scatter graphic", fontsize=21)
    plt.xticks(rotation=90)
    plt.legend(type)
    plt.show()


def histogram(df, type):
    df[type].plot(kind='hist', legend=True)
    plt.xlabel(type)
    plt.title(type + " - histogram graphic", fontsize=20)
    plt.show()


def bar(df, type):
    df[type].value_counts().plot(kind='bar', figsize=(12, 10), rot=0, legend=True)
    plt.xlabel(type)
    plt.xticks(rotation=90)
    plt.title(type + " - bar graphic", fontsize=21)
    plt.show()


def pie(df, type):
    df[type].value_counts().plot.pie(y=type, figsize=(15, 15),
                                     autopct='%1.1f%%', fontsize=22, legend=True)
    plt.title(type + " - pie graphic", fontsize=24)
    plt.xlabel(type, fontsize=24)
    plt.legend(fontsize=24)
    plt.show()


def visualization(df):
    while True:
        print('-------------------------------\nIf you want to exit - press 999:\n-------------------------------')
        types_all = ['Temperature', 'Dew Point', 'Humidity', 'Wind Speed', 'Wind Gust', 'Wind', 'Condition']
        print('Choose data which you want to visualize:\n')
        for index, i in enumerate(types_all):
            print(index + 1, ' - ', i)
        temp = list(map(int, input('Types separated by space\n').split(' ')))
        if temp[0] == 999:
            break
        types = [types_all[i - 1] for i in temp]
        graphics_all = ['line', 'scatter', 'histogram', 'bar']
        for i in types:
            if i != 'Wind' and i != 'Condition':
                print('Avaliable graphics for ---', i, '--- :\n')
                for index, j in enumerate(graphics_all):
                    print(index + 1, ' - ', j)
                print('Which graphics do you want to display for type ---: ', i, '---')
                graphics_to_plot = list(map(int, input('Graphics separated by space\n').split(' ')))
                for j in graphics_to_plot:
                    if j == 1:
                        line(df, i)
                    elif j == 2:
                        scatter(df, i)
                    elif j == 3:
                        histogram(df, i)
                    elif j == 4:
                        bar(df, i)
            elif i == 'Wind' or i == 'Condition':
                print('Which graphics do you want to display for type: ', i)
                print('Avaliable types for ---', i, '--- :\n', 'Pie')
                pie(df, i)