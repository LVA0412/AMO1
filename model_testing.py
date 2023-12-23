import pandas as pd
from sklearn.metrics import mean_squared_error
import joblib

# Загрузим тестовый набора данных
test_df = pd.read_csv('test/test.csv', index_col='date', parse_dates=True)

# Загрузим сохраненую модель
model_filename = 'daily_revenue_model.joblib'
loaded_model = joblib.load(model_filename)

# Подготовим данные для предсказания
X_test = test_df.index.values.reshape(-1, 1)
y_test = test_df['daily_revenue'].values

# Предскажем на тестовом наборе
y_pred = loaded_model.predict(X_test)

# Оценка предсказаний
mse = mean_squared_error(y_test, y_pred)
print(f'Среднеквадратичная ошибка на тестовом наборе: {mse}')

# Создадим общий датафрейм  с фактическими и предсказанными значениями
predictions_df = pd.DataFrame({'Фактическое значение': y_test, 'Предсказанное значение': y_pred},
                               index=test_df.index)

# Выведим таблицы с предсказаниями
print(predictions_df)
