import requests
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def get_clinical_network(gene_list):
    url = "https://string-db.org/api/json/network"
    params = {
        "identifiers": "%0d".join(gene_list),
        "species": 9606,
        "required_score": 150,       # Lowering confidence to 0.15 (150/1000)
        "add_nodes": 10,             # Add 10 "Shell" proteins to connect your biomarkers
        "caller_identity": "biomarker_pipeline"
    }
    
    response = requests.post(url, data=params)
    interactions = response.json()
    
    if not interactions:
        print("Still no interactions found. Try adding more genes.")
        return

    G = nx.Graph()
    for edge in interactions:
        G.add_edge(edge['preferredName_A'], edge['preferredName_B'])

    # Highlight YOUR biomarkers in a different color
    node_colors = ['#e74c3c' if node in gene_list else '#3498db' for node in G.nodes()]

    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(G, k=0.6)
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1200, font_size=9)
    plt.title("Clinical Interaction Map (Biomarkers in Red)")
    plt.savefig('clinical_network.png')
    print("Expanded network saved as clinical_network.png")

# Use the top 50 biomarkers instead of 20 to increase chance of overlap
df = pd.read_csv('Biomarker Identification/final_identified_biomarkers.tsv', sep='\t')
top_genes = df['Protein_Label'].head(50).tolist()
get_clinical_network(top_genes)
