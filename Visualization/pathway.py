import pandas as pd
import matplotlib.pyplot as plt

# Simulated Enrichment Data based on your Up/Down regulated results
# In a full pipeline, you'd use GSEAPY here.
pathway_data = {
    'Pathway': ['Glycolysis', 'T-Cell Activation', 'Apoptosis', 'Lipid Metabolism', 'DNA Repair', 'Inflammation'],
    'Score': [2.8, 1.5, 0.4, -1.2, -1.9, -2.5] # Positive = Up-regulated proteins dominate
}
pathways = pd.DataFrame(pathway_data).sort_values('Score', ascending=False)

plt.figure(figsize=(10, 6))
colors = ['#e74c3c' if x > 0 else '#3498db' for x in pathways['Score']]
plt.barh(pathways['Pathway'], pathways['Score'], color=colors)
plt.axvline(0, color='black', linewidth=0.8)
plt.title("Pathway Activation Waterfall Plot")
plt.xlabel("Enrichment Score (Activated > 0 | Inhibited < 0)")
plt.savefig('pathway_waterfall.png')
print("Waterfall plot saved as pathway_waterfall.png")
