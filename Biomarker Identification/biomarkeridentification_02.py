import pandas as pd
import numpy as np

# 1. Load data
results = pd.read_csv('final_analysis_results.tsv', sep='\t')
expr = pd.read_csv('/Users/deeksharajesh/Downloads/QPIAI_input/data/E-PROT-149.tsv', sep='\t')

# 2. Fix the names BEFORE filtering
results['Gene_Name_Fixed'] = expr['Gene Name'].iloc[results.index].values
results['Gene_ID_Fixed'] = expr['Gene ID'].iloc[results.index].values
results['Protein_Label'] = results['Gene_Name_Fixed'].fillna(results['Gene_ID_Fixed'])

# 3. Define Significance
up_mask = (results['p_value'] < 0.05) & (results['log2FC'] > 1)
down_mask = (results['p_value'] < 0.05) & (results['log2FC'] < -1)

# 4. Create the biomarkers dataframe
biomarkers = results[up_mask | down_mask].copy()

# 5. Print the Summary you saw earlier
print(f"Identification Complete!")
print(f"Found {sum(up_mask)} Up-regulated biomarkers.")
print(f"Found {sum(down_mask)} Down-regulated biomarkers.")

print("\n--- TOP 5 CANDIDATE BIOMARKERS ---")
if not biomarkers.empty:
    # Now Protein_Label exists, so this won't error!
    print(biomarkers[['Protein_Label', 'p_value', 'log2FC']].sort_values('p_value').head())
else:
    print("No biomarkers found with p < 0.05 and |log2FC| > 1")

# 6. Save final file
biomarkers.to_csv('final_identified_biomarkers.tsv', sep='\t', index=False)
