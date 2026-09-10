import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/rfm_result.csv')
df = df.sort_values('rfm_group')
plt.figure(figsize=(12, 6)) 
plt.bar(df['rfm_group'], df['customers'], color='steelblue')
plt.title('Распределение клиентов по RFM-группам', fontsize=14)
plt.xlabel('RFM-группа', fontsize=12)
plt.ylabel('Количество клиентов', fontsize=12)
plt.xticks(rotation=45) 
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('images/rfm_distribution.png', dpi=150)
plt.show()
