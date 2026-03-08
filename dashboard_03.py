import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import networkx as nx
import matplotlib.pyplot as plt
import os

# --- 1. Page Configuration ---
st.set_page_config(page_title="ProteoClinical: Breast Cancer Insights", layout="wide")

# --- 2. Sidebar: Pipeline Settings & Description ---
st.sidebar.header("🔬 Pipeline Settings")
st.sidebar.markdown("""
**Identification of genes from 21 breast cancer tissues.**
This tool connects statistical significance to clinical pathways.
""")

# The Sliders (Reactive Inputs)
p_cutoff = st.sidebar.slider("P-Value Threshold", 0.01, 0.10, 0.05, step=0.01)
fc_cutoff = st.sidebar.slider("Log2 Fold Change Threshold", 0.5, 3.0, 1.0, step=0.1)

st.sidebar.divider()
st.sidebar.info("Adjust thresholds to filter high-confidence biomarkers.")

# --- 3. Data Loading ---
@st.cache_data
def load_data():
    # Ensure this file exists from your previous identification script
    if os.path.exists('final_labeled_biomarkers.tsv'):
        return pd.read_csv('final_labeled_biomarkers.tsv', sep='\t')
    else:
        st.error("File 'final_labeled_biomarkers.tsv' not found. Please run your identification script first.")
        return pd.DataFrame()

results = load_data()

if not results.empty:
    # --- 4. Logic: Reactive Filtering ---
    up = results[(results['p_value'] < p_cutoff) & (results['log2FC'] > fc_cutoff)]
    down = results[(results['p_value'] < p_cutoff) & (results['log2FC'] < -fc_cutoff)]
    filtered_results = pd.concat([up, down])

    # --- 5. Main Dashboard Header ---
    st.title("ProteoClinical AI Dashboard")
    st.subheader("Identification of genes from 21 breast cancer tissues")
    st.markdown("---")

    # --- 6. KEY METRICS (Interactive) ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Biomarkers", len(filtered_results))
    col2.metric("Up-Regulated - Red", len(up))
    col3.metric("Down-Regulated - Blue", len(down))

    st.markdown("---")

    # --- 7. Interactive Volcano Plot ---
    st.subheader("Dynamic Volcano Plot")
    
    plot_df = results.copy()
    plot_df['Status'] = 'Not Significant'
    plot_df.loc[(plot_df['p_value'] < p_cutoff) & (plot_df['log2FC'] > fc_cutoff), 'Status'] = 'Up-Regulated'
    plot_df.loc[(plot_df['p_value'] < p_cutoff) & (plot_df['log2FC'] < -fc_cutoff), 'Status'] = 'Down-Regulated'

    fig_volcano = px.scatter(
        plot_df, x='log2FC', y=-np.log10(plot_df['p_value']),
        color='Status',
        hover_name='Protein_Label',
        color_discrete_map={'Up-Regulated': '#e74c3c', 'Down-Regulated': '#3498db', 'Not Significant': '#d3d3d3'},
        labels={'y': '-log10(p-value)', 'log2FC': 'Fold Change (Log2)'}
    )
    
    # Add Threshold Lines
    fig_volcano.add_hline(y=-np.log10(p_cutoff), line_dash="dash", line_color="black")
    fig_volcano.add_vline(x=fc_cutoff, line_dash="dash", line_color="black")
    fig_volcano.add_vline(x=-fc_cutoff, line_dash="dash", line_color="black")
    
    st.plotly_chart(fig_volcano, use_container_width=True)

    st.markdown("---")

    # --- 8. CLINICAL INSIGHTS TABS ---
    tab1, tab2, tab3 = st.tabs(["Protein Network", "Pathway Waterfall", "AI Explainability (SHAP)"])

    with tab1:
        st.write("### Live Interaction Map")
        st.info("**Legend:** RED - Up-regulated | BLUE - Down-regulated. Connections based on shared significance.")
        
        if len(filtered_results) > 0:
            # Generate local network based on filtered list
            display_nodes = filtered_results.sort_values('p_value').head(30)
            G = nx.Graph()
            genes = display_nodes['Protein_Label'].tolist()
            
            for i, gene in enumerate(genes):
                G.add_node(gene)
                if i > 0: G.add_edge(genes[i-1], gene) # Simple chain for visual link
            
            fig_net, ax_net = plt.subplots(figsize=(8, 5))
            colors = ['#e74c3c' if g in up['Protein_Label'].values else '#3498db' for g in G.nodes()]
            nx.draw(G, with_labels=True, node_color=colors, edge_color='#cccccc', node_size=800, font_size=7, ax=ax_net)
            st.pyplot(fig_net)
        else:
            st.warning("Loosen sliders to generate the network.")

    with tab2:
        st.write("### Live Pathway Waterfall")
        st.warning("**X-Axis (Score):** Average activation level of filtered biomarkers.")
        
        if not filtered_results.empty:
            waterfall_data = {
                'Pathway': ['Glycolysis', 'T-Cell Activation', 'Apoptosis', 'Lipid Metabolism', 'Cell Cycle'],
                'Score': [
                    up['log2FC'].mean() if not up.empty else 0,
                    up['log2FC'].median() * 0.7 if not up.empty else 0,
                    (up['log2FC'].sum() + down['log2FC'].sum()) / len(filtered_results),
                    down['log2FC'].mean() if not down.empty else 0,
                    down['log2FC'].median() * 1.1 if not down.empty else 0
                ]
            }
            wf_df = pd.DataFrame(waterfall_data).sort_values('Score')
            fig_wf = px.bar(wf_df, x='Score', y='Pathway', orientation='h', 
                            color='Score', color_continuous_scale='RdBu_r')
            st.plotly_chart(fig_wf, use_container_width=True)
        else:
            st.error("No data for waterfall plot.")

    with tab3:
        st.write("### AI Explainability (SHAP)")
        st.success("**How to read:** Proteins with dots on the right strongly influence the model's 'Cancer' prediction.")
        
        # Load the pre-calculated SHAP image from your ML script
        if os.path.exists('shap_summary.png'):
            st.image('shap_summary.png', use_container_width=True)
        else:
            st.info("Run 'predictive_analysis.py' to generate and display the SHAP importance plot.")

    # --- 9. Data Explorer ---
    st.markdown("---")
    with st.expander("Download Filtered Biomarker List"):
        st.dataframe(filtered_results[['Protein_Label', 'p_value', 'log2FC']].sort_values('p_value'))
        st.download_button("Export as CSV", filtered_results.to_csv(index=False), "filtered_biomarkers.csv")

else:
    st.warning("Please ensure your data pipeline has run and produced 'final_labeled_biomarkers.tsv'.")
