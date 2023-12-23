# Сгенерируем набор данных, который описывает количество посетителей
# и выручку в магазине для садоводов, расположенном в ТЦ
# в выходные дни посетителей больше, в будни меньше.
# сезонные колебания (посевная, зима) при генерации не учитываются 
import os
import csv
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import shutil
from sklearn.model_selection import train_test_split

def data_gen(start_date, end_date, csv_filename):
  date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
  # словарь искажающих коэфициентов
  # если выпало 58 количестов посетителей сделаем отрицательным
  # если выпало 59 увеличим дневную выручку в сто тысяч раз
  anm_knd = {58:[-1, 1], 59: [1, 100000]} 
  try:
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Запись заголовка Дата, количество посетителей, Выручка (руб.)
        writer.writerow(['date', 'number_visitors', 'daily_revenue'])
        # Запись данных
        for date in date_range:
            k1 = 1 # коэффициент для внесения аномалий/шумов количества посетителей
            k2 = 1 # коэффициент для внесения аномалий/шумов выручки
            # с вероятностью 5% внесем аномалии
            anm_p = random.randint(0, 59)
            if  anm_p > 57: # с вероятностью 5% внесем аномалии
                k1 = anm_knd[anm_p][0]
                k2 = anm_knd[anm_p][1]
                #print(k1,k2)
            if 6 <= date.isoweekday() <= 7: # если выходные, то добавим 30%
                number_visitors = int(random.randint(0, 99) * 1.3) * k1
                daily_revenue = number_visitors * int(random.randint(0, 5000) * k2)
            else:
                number_visitors = random.randint(0, 99) * k1
                daily_revenue = number_visitors * int(random.randint(0, 5000) * k2)
            # Запись строки в CSV файл
            if anm_p == 57: # если выпало 57 занесем данные дважды
                writer.writerow([date.strftime('%d.%m.%Y'), number_visitors, daily_revenue])
            writer.writerow([date.strftime('%d.%m.%Y'), number_visitors, daily_revenue])
    return True
  except Exception as e:
    print(f'Произошла ошибка при записи файла: {e}')
    return False

folder_names = ['train', 'test']
for f in folder_names:
    # Проверка наличия папки
    if not os.path.exists(f):
    # Если папки нет, создаем ее
        os.makedirs(f)

# Генерация списка дат с 01.01.2021 по 31.12.2022 
start_train = datetime(2021, 1, 1)
end_train = datetime(2022, 12, 31)
data_fn = 'data.csv'

if data_gen(start_train, end_train, data_fn):
    print(f'Данные сохранены в файл: {data_fn}')


# Разделим данные на тренировочный и тестовый наборы
data_df = pd.read_csv(data_fn, index_col='date', parse_dates=True)

train_df, test_df = train_test_split(data_df, test_size=0.2, random_state=42)


# Сохраняем данные в соответствующие папки
train_df.to_csv('train/train.csv')
test_df.to_csv('test/test.csv')

# Посмотрим информацию о размере тренировочного и тестового наборов
print('Размер тренировочного набора:', len(train_df))
print('Размер тестового набора:', len(test_df))