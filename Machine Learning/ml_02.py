import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import shap
import matplotlib.pyplot as plt

# 1. Load data
expr_raw = pd.read_csv('data/E-PROT-149.tsv', sep='\t')

# 2. Create the labels
expr_raw['Protein_Label'] = expr_raw['Gene Name'].fillna(expr_raw['Gene ID'])
expr_raw = expr_raw.set_index('Protein_Label')

# 3. DYNAMICALLY find the sample columns
# Most proteomics files have the data starting after the Gene/Protein info.
# We will grab the first 10 columns that are of "numeric" type.
data_cols = expr_raw.select_dtypes(include=[np.number]).columns[:10]

print(f" Found sample columns: {list(data_cols)}")

# 4. Filter and Transpose
X = expr_raw[data_cols].T.fillna(0)

# 5. Define labels (Adjust if your data isn't 5 Control vs 5 Disease)
y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])

# 6. Train and SHAP
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

# Handle the fact that shap_values can be a list for multi-class
if isinstance(shap_values, list):
    actual_shap = shap_values[1]
else:
    actual_shap = shap_values

shap.summary_plot(actual_shap, X)
plt.savefig('shap_summary_01.png')
print("SHAP plot saved as 'shap_summary_01.png'")
shap.plots.beeswarm(explainer(X)[:,:,1])
