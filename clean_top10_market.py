import pandas as pd
import numpy as np

df = pd.read_csv('real_spb_dom_rf.csv')

df['Проектная_площадь_кв_м'] = pd.to_numeric(df['Проектная_площадь_кв_м'], errors='coerce').fillna(0)
df['Цена_за_кв_м'] = pd.to_numeric(df['Цена_за_кв_м'], errors='coerce').fillna(0)
df['Застройщик'] = df['Застройщик'].fillna('Неизвестный девелопер')

# Заменяем нули на NaN для корректного расчета средних значений по рынку
df['Цена_за_кв_м'] = df['Цена_за_кв_м'].replace(0, np.nan)
df['Проектная_площадь_кв_м'] = df['Проектная_площадь_кв_м'].replace(0, np.nan)

# Глобальная агрегация рынка Петербурга
market_analytics = df.groupby('Застройщик').agg(
    Количество_ЖК=('ID_Объекта', 'count'),
    Средняя_цена_кв_м=('Цена_за_кв_м', 'mean'),
    Общая_жилая_площадь=('Проектная_площадь_кв_м', 'sum') 
).reset_index()

market_analytics['Емкость_портфеля_млрд_руб'] = ((market_analytics['Общая_жилая_площадь'] * market_analytics['Средняя_цена_кв_м']) / 1_000_000_000).round(2)
market_analytics = market_analytics.sort_values(by='Емкость_портфеля_млрд_руб', ascending=False).dropna(subset=['Емкость_портфеля_млрд_руб'])

# Берем только Топ-10 для витрины
top_10 = market_analytics.head(10)
top_10.to_csv('top10_market_analytics.csv', index=False)
print("Витрина Топ-10 рынка сохранена в top10_market_analytics.csv")