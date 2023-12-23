#выполним предобработку датасета. уберем дубли, строчки с
# отрицательным количеством посетителей и даты с нереально большой выручкой
# очищенные данные сохраним в csv файл

import pandas as pd

def clear_data(csv_file_name):
    # загрузка датасета
    df = pd.read_csv(csv_file_name, index_col='date', parse_dates=True)

    # запомним сколько записей было в начале
    begin_rec_cnt = len(df)

    # удаление дубликатов
    df = df[~df.index.duplicated(keep='first')]
    rec_wo_doubles = len(df)
    # удаление аномальных значений
    initial_anomalies = len(df)

    df = df[(df['number_visitors'] >= 0)]
    df = df[(df['daily_revenue'] <= 501000)]


    # сохранение файла
    df.to_csv(csv_file_name)

    # распечатаем результаты работы
    print(f"Обработан файл: {csv_file_name}")
    print(f"Первоначальное количество строк: {begin_rec_cnt}")
    print(f"Удалено дубликатов: {begin_rec_cnt - rec_wo_doubles}")
    print(f"Удалено строк с аномальными значения: {rec_wo_doubles- len(df)}")
    print(f"Ощищенный датасет содержит строк: {len(df)}")

# сохранение файлов
clear_data('train/train.csv') #  очистка тренировочного набора
clear_data('test/test.csv') # очистка тестового набора