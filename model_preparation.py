import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# Загрузим тренировочый набор данных
train_df = pd.read_csv('train/train.csv', index_col='date', parse_dates=True)

# целевая переменная - 'daily_revenue' - дневная выручка
X = train_df.index.values.reshape(-1, 1)
y = train_df['daily_revenue'].values

# Разделим данных на обучающий и валидационный наборы
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Инициализируем модель
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Обучение модели
model.fit(X_train, y_train)

# Получение прогнозов на валидационном наборе
y_pred = model.predict(X_val)

# Оценка модели
mse = mean_squared_error(y_val, y_pred)
print(f'Среднеквадратичная ошибка на валидационном наборе: {mse}')

# Сохранение обученной модели в файл
model_filename = 'daily_revenue_model.joblib'
joblib.dump(model, model_filename)
print(f'Модель сохранена в файл {model_filename}')
