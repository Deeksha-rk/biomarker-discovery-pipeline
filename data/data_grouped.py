import pandas as pd
import os

# Input file path (change to your actual path)
input_path = "data/E-PROT-149.condensed-sdrf.tsv"
folder = os.path.dirname(input_path)

# Load TSV safely
metadata = pd.read_csv(
    input_path,
    sep="\t",
    header=None,
    engine='python',
    on_bad_lines='warn'
)

# Column 5 (0-based index 5) contains the value we want for Group
metadata['Value_for_Group'] = metadata.iloc[:, 5]  # exactly column 5

# Convert to lowercase and strip spaces
metadata['Value_lower'] = metadata['Value_for_Group'].astype(str).str.lower().str.strip()

# Function to categorize Disease / Control / Unknown
def categorize(value):
    disease_keywords = ['breast cancer', 'lum', 'basal', 'her2', 'estrogen receptor', 'progesterone receptor']
    if any(k in value for k in disease_keywords):
        return 'Disease'
    elif 'normal' in value:
        return 'Control'
    elif 'not available' in value:
        return 'Unknown'
    else:
        return 'Unknown'

# Apply categorization
metadata['Group'] = metadata['Value_lower'].apply(categorize)

# Save full original data with Group column
output_path = os.path.join(folder, "E-PROT-149_grouped_full.tsv")
metadata.to_csv(output_path, sep="\t", index=False)

print(f"Saved grouped metadata to: {output_path}")
