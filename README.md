[ProteoClinical _ Study of 21 Breast Tissues for Biomarker Identification.md](https://github.com/user-attachments/files/25821679/ProteoClinical._.Study.of.21.Breast.Tissues.for.Biomarker.Identification.md)# biomarker-discovery-pipeline[Uploading ProteoClinical _ Study o**ProteoClinical : Study of 21 Breast Tissues for Biomarker Identification** 

**Objective**  
Trying to find biomarkers to distinguish between breast cancer and healthy (controls) using Bioinformatic tools and AI, so that it will provide us concrete results regarding disease progression and early diagnosis of breast cancer.

**Data**  
The raw data was downloaded from a public platform called Expression Atlas and the project was named as  DIA-MS analysis of 21 breast cancer tissues. The data contained an E-PROT-149.tsv file which I started working with. Proteomics data had a lot of gaps where proteins were not detected, methods like `.fillna(0)` or `.dropna()` were used so that the Machine Learning model had a complete matrix to learn from.   
I had to normalize the data so that all the samples had the same scale.  
The data did not contain any information about the category (disease or Control), I had to modify the data by taking into consideration the lumA column and then categorising them. 

**Differential Expression**  
Once the data was cleaned, I did a Differential expression analysis using the T- test approach along with log2 Fold Change, the data here is continuous and it does not have any RNA counts, a T test is mathematically suitable, this also allowed me to upload the results to scikit-learn and streamlit which is used for ML model and Dashboard. 

**Visualization of statistical finding**  
The Protein network shows a relationship between the up and down regulated proteins *(Figure.2)*. Here the red nodes which are up-regulated are in the form of a cluster and they are responsible for the growth of tumor, while the blue nodes try to keep these tumor cells from growing which might lead to a better chance of survival. 

The Waterfall Graph *( Figure.2)*  shows how these proteins interact with the tumor. When we look at the bars which are present on the right side we can say that there is a rise in cancerous cells because they are hyper-active and that is leading to a surge in nucleic acid synthesis and glycolytic flux.   
Now, if we observe the left side of the graph which has the blue bars, we can say that these proteins are trying to curb the tumor, but due to the high number of up-regulated protein, the body has lost the ability to fight against the tumor and also its interferon signalling. 

SHAP model : This is a Machine learning outcome after using a Random Forest model on the data *(Figure.3)*. If we have a new input, this model will help us in identifying whether the tissue is going to be benign or malignant by looking at the features. Since the data contains only 21 samples the model may not be able to predict the tissue very accurately. Here the analysis between A1GB vs A2M) shows how they are interacting with each other. In this data,  the 21 samples do not have any strong influence on either boosting or suppressing the tumor. If the dots are present towards   
\+1.0 or \-1.0 they are considered noise and these proteins were confusing for the ML model to categorize them leading them to overfitting. 

*Figure.1 Protein network mapping                        Figure.2 Pathway Graph which gives information regarding how the protein behaves* 

*Figure.3 SHAP model which is used for understanding how the Ml model categorizes the proteins*

**Statistical Analysis**  
I was able to find out that 71 samples had a high significance, with p-value less than 0.5 and log2 Fold value of more than 1.0. Out of which 54 were up-regulated and 17 were down-regulated. *(Figure.4)*  
Up-regulated : These proteins are over-expressed and are trying to grow rapidly by cell division and also consuming energy through glycolysis.  
Down-regulated : These proteins try to prevent the growth of the cancerous cells, they tell the body to undergo Apoptosis and also try to curb the cancer through immune signaling.

![][image1]  
*Figure.4 Volcano Plot showing the distribution of protein significance vs. magnitude of change across 21 samples.*

**Biomarker Identification**  
The top 5 biomarkers which were obtained during the differential analysis were categorized based on its p-value and log2 Fold value.

| Row indices  | Protein name  | p value | log2FC  | Up/Down regulated |
| :---- | :---- | :---- | :---- | :---- |
| 2694 | IGHG3 | 0.000563  | \-1.682792  | Down  |
| 84 | ACOT7 | 0.001343  | 1.062958  | Up |
| 6138 | TRIM32 | 0.003214 | 1.762156  | Up |
| 2993 | KRT80 | 0.003773  | 1.109614  | Up |
| 5807 | ITGB3 | 0.006767  |  3.976143  | Up |

*Table.1 Information about the proteins which are being Up or Down regulated based on the statistical values.*

Looking at the table above, there is only one protein, IGHG3, an antibody which is being down regulated, where the plasma cells are trying to replace the tumor cells.   
The rest of the proteins ACOT7, TRIM32, KRT80 and ITGB3 are all up regulated in the body. ACOT7 is involved in fatty acid metabolism which is helping rapid cell division.   
TRIM32 is often associated with degrading the tumor suppressor which is leading the tumor cells to pass through the stop signals.  
KRT80 Keratin 80 is a cytoskeletal protein leading to structural changes, which is influencing the tumor cells to be mobile and invasive.   
ITGB3 has the highest intensity with 3.97, this suggests that the tissue cells are on the verge of developing new blood vessels and spreading and they are hidden from the immune system which may not lead to any detection of the tumor.

**Result**   
Despite the inherent noise in the proteomic data, using robust computational methods and ML, we can see that the 21 tissue samples helped in obtaining 71 strong molecular fingerprints, where the tissues are undergoing significant structural remodelling and are immune invasive (hiding from the body's immune system). Out of the top 5 biomarkers, IGHG3 is a strong candidate for diagnostic biomarker and ITGB3 can be a primary candidate for targeted therapy. By looking at the proteins we can provide concrete results for disease progression and early diagnosis which can be used in the future for clinical screening. 

**Note: An interactive Streamlit Dashboard has been attached to this project to allow for real-time exploration of the biomarker network and pathway analysis.**



A reproducible bioinformatics and AI pipeline for breast cancer biomarker discovery. This project utilizes public proteomics datasets to identify protein signatures that distinguish between disease and control samples for early diagnosis and progression tracking
