# Real Colorectal Cancer Datasets from kaggle
The data set comes from here:
https://www.kaggle.com/datasets/amandam1/colorectal-cancer-patients?select=Colorectal+Cancer+Patient+Data.csv
and consists of two files:

Patient Data for 62 patients
* Age: at Diagnosis (in Years)
* Dukes Stage: A to D (development/progression of disease)
* Gender: Male or Female
* Location: Left, Right, Colon or Rectum
* DFS: Disease-free survival, months (survival without the disease returning)
* DFS event: 0 or 1 (with 1 = event)
* AdjRadio: If the patient also received radiotherapy
* AdjChem: If the patient also received chemotherapy

Gene Expression Data for 1935 genes
* log2 transformed expression levels from Affymetrix micro array probe ids
* here are some approaches to get gene/transcript information for the probe ids: 
    * https://www.ebi.ac.uk/training/online/courses/array-express-discover-functional-genomics-data-quickly-and-easily/next-steps-towards-data-analysis/opening-and-processing-raw-data-files/microarray-experiments/tools-for-conversion-of-probe-ids/
    * probably best to do this with R/Bioconductor

# Analysis Plan
Start with EDA of patient metadata fields vs DFS and create some Kaplan-Meier curves.
* can also compute some Cox Proportional Hazards (CPH) analysis for patient metadata fields to determine if there are significant effects

Then look for individual genes whose expression levels regress well with DFS and are not highly correlated with each other. 
* this is likely also done with CPH, e.g. see https://www.biostars.org/p/344233/
* there is also an on-line tool, Survival Genie, to compare with.  See https://www.nature.com/articles/s41598-022-06841-0

Then look for sets of genes that ML can use to predict DFS
* as a start, to limit risk of overfitting we should try to limit the genes for modeling to <=50 genes
* later we can consider using more genes in a more robust modeling approach like RF or DL