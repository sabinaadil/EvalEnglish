import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

CSV_PATH = 'synthetic_activity_data.csv'
if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"Файл табылмады: {CSV_PATH}")

df = pd.read_csv(CSV_PATH)
sns.set(style="whitegrid")

plt.figure(figsize=(8, 5))
sns.histplot(df['final_efficiency_score'], bins=20, kde=True)
plt.title('Соңғы тиімділік ұпайын бөлу')
plt.xlabel('Қорытынды балл')
plt.ylabel('Оқушылар саны')
plt.tight_layout()
plt.savefig('plots/final_score_distribution.png')
plt.close()

plt.figure(figsize=(10, 8))
corr = df.corr(numeric_only=True)
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Белгілердің корреляциялық матрицасы')
plt.tight_layout()
plt.savefig('plots/correlation_matrix.png')
plt.close()

plt.figure(figsize=(8, 5))
sns.scatterplot(x='time_spent', y='final_efficiency_score', data=df)
plt.title('Соңғы ұпайдың уақытқа тәуелділігі')
plt.xlabel('Курсқа жұмсалған уақыт (мин)')
plt.ylabel('Қорытынды балл')
plt.tight_layout()
plt.savefig('plots/score_vs_time_spent.png')
plt.close()

plt.figure(figsize=(8, 5))
sns.boxplot(x='late_submissions', y='final_efficiency_score', data=df)
plt.title('Соңғы ұпайдың кешігу санына тәуелділігі')
plt.xlabel('Кешігулер саны')
plt.ylabel('Қорытынды балл')
plt.tight_layout()
plt.savefig('plots/score_vs_late_submissions.png')
plt.close()

print("Барлық графиктер ml/plots қалтасында сақталады")
