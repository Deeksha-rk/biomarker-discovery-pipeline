import pandas as pd
import numpy as np

# Load the files
results_path = 'final_analysis_results.tsv'
expression_path = 'data/E-PROT-149.tsv'

results = pd.read_csv(results_path, sep='\t')
expr = pd.read_csv(expression_path, sep='\t')

# 1. Direct Row Mapping
# We use the index of the results to pull the exact row from the expression file
results['Gene_Name_Fixed'] = expr['Gene Name'].iloc[results.index].values
results['Gene_ID_Fixed'] = expr['Gene ID'].iloc[results.index].values

# 2. Fill Missing Names
# If Gene Name is missing, use the Gene ID so you don't see "NaN"
results['Protein_Label'] = results['Gene_Name_Fixed'].fillna(results['Gene_ID_Fixed'])

# 3. Identify Top Biomarkers (p < 0.05 and abs(log2FC) > 1)
results['Significant'] = (results['p_value'] < 0.05) & (abs(results['log2FC']) > 1)
top_biomarkers = results[results['Significant'] == True].sort_values('p_value')

# 4. Show the results with actual names
print("\n--- TOP BIOMARKERS WITH NAMES ---")
print(top_biomarkers[['Protein_Label', 'p_value', 'log2FC']].head(10))

# 5. Save the final labeled version
top_biomarkers.to_csv('final_labeled_biomarkers.tsv', sep='\t', index=False)
