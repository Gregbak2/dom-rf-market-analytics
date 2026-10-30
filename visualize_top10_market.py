import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

top_10 = pd.read_csv('top10_market_analytics.csv')

sns.set_theme(style="whitegrid")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

# График 1: Bar chart
sns.barplot(data=top_10, y='Застройщик', x='Емкость_портфеля_млрд_руб', palette='viridis', ax=ax1)
ax1.set_title('Топ-10 застройщиков СПб по финансовой емкости', fontsize=14, pad=15)
ax1.set_xlabel('Емкость портфеля (млрд руб.)', fontsize=12)
ax1.set_ylabel('')
for container in ax1.containers:
    ax1.bar_label(container, fmt='%.1f', padding=5)

# График 2: Scatter plot
sns.scatterplot(
    data=top_10, x='Общая_жилая_площадь', y='Средняя_цена_кв_м',
    size='Емкость_портфеля_млрд_руб', sizes=(100, 2000), 
    alpha=0.7, hue='Застройщик', palette='deep', legend=False, ax=ax2
)

for i in range(top_10.shape[0]):
    ax2.text(
        top_10['Общая_жилая_площадь'].iloc[i] + 15000, 
        top_10['Средняя_цена_кв_м'].iloc[i], 
        top_10['Застройщик'].iloc[i], 
        fontsize=9
    )

ax2.set_title('Стратегия: Объем vs Премиальность', fontsize=14, pad=15)
ax2.set_xlabel('Общая жилая площадь (кв. м)', fontsize=12)
ax2.set_ylabel('Средняя цена (руб/кв. м)', fontsize=12)

plt.tight_layout()
plt.savefig('top10_market_analysis.png', dpi=300, bbox_inches='tight')
print("Глобальный отчет сохранен в top10_market_analysis.png")