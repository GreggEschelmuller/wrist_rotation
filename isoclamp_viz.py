import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


data_ = pd.read_csv('testing_output_data.csv')

sns.set_theme(style='white', palette='pastel')

sns.catplot(data=data_, x="target_positions", y="error", kind="swarm")
sns.despine(offset=10)
plt.title('Angular Error Scores')
plt.tight_layout()
plt.show()
