import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Настройки шрифта (кириллица)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 12

df = pd.read_csv('data/rfm_result.csv')

# Сортируем по RFM-группе (по возрастанию — 111 слева, 333 справа)
df = df.sort_values('rfm_group').reset_index(drop=True)
df['rfm_group'] = df['rfm_group'].astype(str)

# Считаем сумму рангов R+F+M для каждого клиента
df['score'] = df['rfm_group'].apply(lambda x: int(x[0]) + int(x[1]) + int(x[2]))

# --- Раскраска по категориям ---
def color_by_score(score):
    if score <= 5:
        return '#2ecc71'   # зелёный — ценные
    elif score <= 7:
        return '#f1c40f'   # жёлтый — средние
    else:
        return '#e74c3c'   # красный — теряемые

colors = df['score'].apply(color_by_score)

# Создаём папку для картинки
os.makedirs('images', exist_ok=True)

# Позиции по X 
positions = range(len(df))

# Построение графика
plt.figure(figsize=(14, 6))
plt.bar(positions, df['customers'], color=colors, edgecolor='black', linewidth=0.4)

plt.title('Распределение клиентов по RFM-группам', fontsize=14, pad=15)
plt.xlabel('RFM-группа')
plt.ylabel('Количество клиентов')
plt.xticks(positions, df['rfm_group'], rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.4)

# Подписи значений над столбцами
for i, v in enumerate(df['customers']):
    plt.text(i, v + max(df['customers']) * 0.01, str(v),
             ha='center', fontsize=8, rotation=90)

# Легенда
legend_elements = [
    Patch(facecolor='#2ecc71', edgecolor='black', label='Ценные (R+F+M = 3–5)'),
    Patch(facecolor='#f1c40f', edgecolor='black', label='Средние (R+F+M = 6–7)'),
    Patch(facecolor='#e74c3c', edgecolor='black', label='Теряемые (R+F+M = 8–9)'),
]
plt.legend(handles=legend_elements, loc='upper center', fontsize=10, framealpha=0.9)

# Сохранение
plt.tight_layout()
plt.savefig('images/rfm_distribution.png', dpi=150)
plt.close()
