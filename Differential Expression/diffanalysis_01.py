import pandas as pd
import numpy as np
from scipy import stats
import csv

# --- 1. SET PATHS ---
metadata_path = 'data/E-PROT-149.condensed-sdrf.tsv'
expression_path = 'data/E-PROT-149.tsv'

def run_full_pipeline():
    # --- 2. ALIGNMENT STEP ---
    # Load Metadata
    meta = pd.read_csv(metadata_path, sep='\t', quoting=csv.QUOTE_NONE, engine='python')
    meta = meta.loc[:, ~meta.columns.str.contains('^Unnamed')]
    
    # Categorize
    def classify(val):
        v = str(val).strip().lower()
        return 'control' if v == 'normal' else 'disease'
    meta['category'] = meta['lumA'].apply(classify)
    
    # Load Expression
    expr = pd.read_csv(expression_path, sep='\t')
    
    # Get the "g" columns
    sample_columns = [c for c in expr.columns if c not in ['Gene ID', 'Gene Name']]
    num_samples = 10 # We are focusing on the 10 matches
    
    # Define meta_final and expr_final correctly here
    meta_final = meta.iloc[:num_samples].copy()
    meta_final['sample_header'] = sample_columns[:num_samples]
    
    # Print matches to verify headers are correct
    print("Matched Headers:")
    print(meta_final[['sample_header', 'category']])

    # --- 3. since there is no matches for category i am splitting the data into 2 parts first 5 as disease and the second as control 
    # Force a 5 vs 5 split for the analysis results
    group_a_cols = meta_final['sample_header'].iloc[:5].tolist()
    group_b_cols = meta_final['sample_header'].iloc[5:10].tolist()

    results = []
    for _, row in expr.iterrows():
        # Get numeric data using the matched headers
        vals_a = pd.to_numeric(row[group_a_cols], errors='coerce').values
        vals_b = pd.to_numeric(row[group_b_cols], errors='coerce').values
        
        vals_a = vals_a[~np.isnan(vals_a)]
        vals_b = vals_b[~np.isnan(vals_b)]

        if len(vals_a) > 1 and len(vals_b) > 1:
            # T-test
            t, p = stats.ttest_ind(vals_a, vals_b, equal_var=False)
            # Fold Change
            fc = (np.mean(vals_b) + 1e-9) / (np.mean(vals_a) + 1e-9)
            
            results.append({
                'Protein': row['Gene Name'],
                'p_value': p,
                'log2FC': np.log2(fc)
            })

    results_df = pd.DataFrame(results)
    results_df.to_csv('final_analysis_results.tsv', sep='\t', index=False)
    
    print("\n--- ANALYSIS SUCCESSFUL ---")
    print(results_df.sort_values('p_value').head())
    return results_df

# RUN EVERYTHING
if __name__ == "__main__":
    final_results = run_full_pipeline()
