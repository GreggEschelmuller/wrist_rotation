import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# To do:
# 1. make visualization in time
# 2. make visualization in space (birdseye view)


df = pd.read_excel('testing_output_data.xlsx', sheet_name=0, engine='openpyxl')

sns.set_theme(style='white', palette='pastel')

sns.catplot(data=df, x="target_positions",
            y="error", kind="swarm", hue='rotation', col='condition')
sns.despine(offset=10)
plt.title('Angular Error Scores')
plt.tight_layout()
plt.show()
