import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('target_districts_analytics.csv')

sns.set_theme(style="whitegrid")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

# Барчарт: Емкость портфеля с цветовой группировкой по районам (hue)
sns.barplot(
    data=df,
    y='Застройщик',
    x='Емкость_портфеля_млрд_руб',
    hue='Район',
    palette={'Петроградский': '#2a9d8f', 'Приморский': '#e76f51'},
    ax=ax1
)
ax1.set_title('Емкость портфеля по целевым районам', fontsize=14, pad=15)
ax1.set_xlabel('Емкость (млрд руб.)', fontsize=12)
ax1.set_ylabel('')

# Пузырьковая диаграмма: Объем площади против цены за метр
sns.scatterplot(
    data=df,
    x='Общая_жилая_площадь',
    y='Средняя_цена_кв_м',
    size='Емкость_портфеля_млрд_руб',
    sizes=(100, 2000),
    alpha=0.7,
    hue='Район',
    palette={'Петроградский': '#2a9d8f', 'Приморский': '#e76f51'},
    ax=ax2
)

# Подписи девелоперов рядом с точками
for i in range(df.shape[0]):
    ax2.text(
        df['Общая_жилая_площадь'].iloc[i] + 800,
        df['Средняя_цена_кв_м'].iloc[i],
        df['Застройщик'].iloc[i],
        fontsize=9
    )

ax2.set_title('Стратегия: Объем vs Премиальность', fontsize=14, pad=15)
ax2.set_xlabel('Общая жилая площадь (кв. м)', fontsize=12)
ax2.set_ylabel('Средняя цена (руб/кв. м)', fontsize=12)

plt.tight_layout()
plt.savefig('target_districts_analysis.png', dpi=300, bbox_inches='tight')
print("Отчет сохранен в target_districts_analysis.png")