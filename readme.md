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
Start with EDA of patient metadata fields vs DFS and create some Kaplan-Meier curves. - <font color="green">*DONE*</font>
* can also compute some Cox Proportional Hazards (CPH) analysis for patient metadata fields to determine if there are significant effects - <font color="green">*DONE*</font>

Then look for individual genes whose expression levels regress well with DFS and are not highly correlated with each other. 
* this is likely also done with CPH, e.g. see https://www.biostars.org/p/344233/
* there is also an on-line tool, Survival Genie, to compare with.  See https://www.nature.com/articles/s41598-022-06841-0

Then look for sets of genes that ML can use to predict DFS
* as a start, to limit risk of overfitting we should try to limit the genes for modeling to <=50 genes
* later we can consider using more genes in a more robust modeling approach like RF or DL

# Summary 
Dug into this a bit including annotating "probesets" to transcripts and genes.  Find that this affy microarray has many-to-many relationships between probesets and transcripts, which makes analysis of differential expression of transcripts challenging from this probeset data.

I emailed 
Prof. Dr. Márcio Dorn
Federal University of Rio Grande do Sul, Institute of Informatics, Center for Biotechnology
Structural Bioinformatics and Computational Biology Lab - SBCB - http://sbcb.inf.ufrgs.br
Av. Bento Gonçalves 9500
91501-970 - Porto Alegre, RS - Brasil
Prédio 72  Sala 217
Tel: +55 51 3308-6824
Lattes CV: http://lattes.cnpq.br/6355224981962273
mdorn@inf.ufrgs.br

about the data set and he kindly pointed out that his group has also posted some curated RNA-Seq data here:
https://sbcb.inf.ufrgs.br/barracurda

The RNA-Seq data provide direct access to gene-sample normalized and transformed (to remove heteroskedacity) counts.  See full description in 
Benchmarking and Testing Machine Learning
Approaches with BARRA:CuRDa, a Curated RNA-Seq Database for Cancer Research
BRUNO CE ́ SAR FELTES,1,2 JOICE DE FARIA POLONI,1,3 and MA ́ RCIO DORN1,4,5,i
JOURNAL OF COMPUTATIONAL BIOLOGY
Volume 28, Number 9, 2021
Pp. 931–944
DOI: 10.1089/cmb.2020.0463