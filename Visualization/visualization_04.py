import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. LOAD DATA ---
# This ensures 'results' and 'expr' are defined in this specific script
results_path = 'final_analysis_results.tsv'
expression_path = '/Users/deeksharajesh/Downloads/QPIAI_input/data/E-PROT-149.tsv'

results = pd.read_csv(results_path, sep='\t')
expr = pd.read_csv(expression_path, sep='\t')

# --- 2. FIX NAMES (The logic you just confirmed) ---
results['Gene_Name_Fixed'] = expr['Gene Name'].iloc[results.index].values
results['Gene_ID_Fixed'] = expr['Gene ID'].iloc[results.index].values
results['Protein_Label'] = results['Gene_Name_Fixed'].fillna(results['Gene_ID_Fixed'])

# --- 3. IDENTIFY SIGNIFICANCE ---
# We define what is "Significant" for the plot colors
results['Significant'] = (results['p_value'] < 0.05) & (abs(results['log2FC']) > 1)
results['-log10_p'] = -np.log10(results['p_value'] + 1e-12)

# --- 4. THE VOLCANO PLOT ---
plt.figure(figsize=(12, 8))
sns.set_style("whitegrid")

# Create scatter plot
sns.scatterplot(
    data=results, 
    x='log2FC', 
    y='-log10_p',
    hue='Significant', 
    palette={True: '#e74c3c', False: '#bdc3c7'}, # Red for biomarkers, Grey for others
    alpha=0.6,
    edgecolor=None
)

# Add threshold lines
plt.axhline(-np.log10(0.05), color='blue', linestyle='--', alpha=0.5, label='p=0.05')
plt.axvline(1, color='black', linestyle='--', alpha=0.3)
plt.axvline(-1, color='black', linestyle='--', alpha=0.3)

# --- 5. ADD GENE LABELS TO THE PLOT ---
# We pick the top 10 most significant proteins to label directly on the graph
top_10 = results[results['Significant'] == True].sort_values('p_value').head(10)

for i, row in top_10.iterrows():
    plt.text(
        row['log2FC'], 
        row['-log10_p'] + 0.1, 
        str(row['Protein_Label']), 
        fontsize=9, 
        fontweight='bold',
        ha='center',
        va='bottom'
    )

# --- 6. FINAL FORMATTING ---
plt.title('Volcano Plot: Differential Protein Expression (5 vs 5 Split)', fontsize=16)
plt.xlabel('Log2 Fold Change (Direction of Change)', fontsize=12)
plt.ylabel('-Log10 p-value (Significance)', fontsize=12)
plt.legend(title='Is Biomarker?', loc='upper right')

# Save the final figure
plt.tight_layout()
plt.savefig('volcano_plot_final_labeled.png', dpi=300)
print("SUCCESS: Volcano plot saved as 'volcano_plot_final_labeled.png'")
plt.show()
