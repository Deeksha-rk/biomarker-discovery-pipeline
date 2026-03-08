**Breast Cancer Proteomics Pipeline & AI Dashboard**
This project is an automated end-to-end pipeline designed to analyze breast cancer proteomics data (E-PROT-149). It processes raw SDRF metadata, performs differential expression analysis, identifies biomarkers using Machine Learning (SHAP), and visualizes results in an interactive Streamlit dashboard.


**Workflow**
<img width="349" height="613" alt="Flowchart" src="https://github.com/user-attachments/assets/a5a9241b-8b47-427c-aea4-4be40d369c4c" />


The pipeline follows a linear execution model where each script prepares data for the next:

Data Processing (data_grouped.py): Cleans SDRF metadata and labels samples (Disease vs. Control).

Differential Expression (diffanalysis_01.py): Calculates Fold-Change and p-values.

Gene Mapping (gene.py): Maps protein IDs to gene symbols.

Machine Learning (ml_02.py): Trains a Random Forest classifier and calculates SHAP values for feature importance.

Visualization Suite: Generates Volcano plots, PPI Networks, and Pathway Waterfall charts.

Dashboard (dashboard_03.py): A Streamlit interface to explore the Top 5 Biomarkers.


**Deployment with Docker**

docker build -t breast-cancer-pipeline .
docker run -p 8501:8501 breast-cancer-pipeline
Open your browser and navigate to:
http://localhost:8501

**THANK YOU**
