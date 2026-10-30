import pandas as pd
import numpy as np

df = pd.read_csv('real_spb_dom_rf.csv')
df['Проектная_площадь_кв_м'] = pd.to_numeric(df['Проектная_площадь_кв_м'], errors='coerce').fillna(0)
df['Цена_за_кв_м'] = pd.to_numeric(df['Цена_за_кв_м'], errors='coerce').fillna(0)
df['Застройщик'] = df['Застройщик'].fillna('Неизвестный девелопер')

# Разметка целевых районов
regex_petrograd = r"(?i)(Петроградск|Каменноостровск|Большой.*П\.С\.|Малый.*П\.С\.|Чкаловск|Песочная|Медиков|Карповк|Аптекарск|Крестовск|Петровск|Пионерск|Зеленина)"
regex_primorsk = r"(?i)(Приморск|Комендантск|Богатырск|Савушкина|Оптиков|Глухарск|Планерн|Королева|Испытателей|Туристск|Мебельная|Беговая)"

df['Район'] = np.select(
    [df['Адрес'].str.contains(regex_petrograd, na=False), df['Адрес'].str.contains(regex_primorsk, na=False)],
    ['Петроградский', 'Приморский'],
    default='Другой'
)

# Фильтруем целевые локации
target_df = df[df['Район'] != 'Другой'].copy()

# Изолируем нули через NaN, чтобы средняя цена считалась корректно
target_df['Цена_за_кв_м'] = target_df['Цена_за_кв_м'].replace(0, np.nan)
target_df['Проектная_площадь_кв_м'] = target_df['Проектная_площадь_кв_м'].replace(0, np.nan)

# Агрегация с разбивкой по районам
analytics = target_df.groupby(['Застройщик', 'Район']).agg(
    Количество_ЖК=('ID_Объекта', 'count'),
    Средняя_цена_кв_м=('Цена_за_кв_м', 'mean'),
    Общая_жилая_площадь=('Проектная_площадь_кв_м', 'sum')
).reset_index()

analytics['Емкость_портфеля_млрд_руб'] = ((analytics['Общая_жилая_площадь'] * analytics['Средняя_цена_кв_м']) / 1_000_000_000).round(2)
analytics = analytics.sort_values(by='Емкость_портфеля_млрд_руб', ascending=False).dropna(subset=['Емкость_портфеля_млрд_руб'])

analytics.to_csv('target_districts_analytics.csv', index=False)
print("Витрина сохранена в target_districts_analytics.csv")