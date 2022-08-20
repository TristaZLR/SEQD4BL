# Selectively Expanding Queries and Documents for News Background Linking
## 1. Install requirements
### 1.1 solr environment
You need to install solr based on your operation system.
Take references to solr guidebook.
> https://solr.apache.org/guide/8_6/solr-tutorial.html#index-the-techproducts-data         

We provide a sample of solr configuration and indexing setting in **./Pipeline/solrconfig**        
You can replace it in your own solr directory

### 1.2 Java environment
If you have conda: 
``` conda install -c conda-forge openjdk=11```        
or use pip command. Please check java installation guide.

### 1.3 other requirements
``` pip install requirements```       
All required packages are listed in **./requirements.txt**      

### 1.4 Data Requirements
> a. [Washington Post Corpus V4](https://trec.nist.gov/data/wapost/)
>> Access permit required.
> We are using topics of News Track [2021](https://trec.nist.gov/act_part/tracks/news/newsir21-topics.txt) and [2020](https://trec.nist.gov/act_part/tracks/news/newsir20-topics.txt).

> b. [NTCIR Temporalia test collection](http://ntcirtemporalia.github.io/NTCIR-11/collection.html)
>> We will need their topics of Temporalia-1 for training the topic classfier
>> Need to apply for access permission.

### 1.5 Evaluation Scripts
This is TREC official evaluation scripts. 
> https://github.com/usnistgov/trec_eval/

qrels need to be prepared in ./Evaluation/eval/
- Download repository to Evaluation Folder 
```
cd ./Evaluation/scripts/trec_eval
git clone https://github.com/usnistgov/trec_eval/
```

### 1.6 Data preprocessing tool

This dataset preprocessing tool is commonly used in TREC datasets. It provides scripts for Wapo V2 and V3.
We changed some codes to let it be able to deal with Wapo V4. You can download it and make changes by yourself or build on our revised version.
> [ir-dataset](https://github.com/allenai/ir_datasets)        

Clone it to the folder named **tookit**. Following their installation guide.
Or you can also choose to build from our souce. Following bellow steps:
```
1. cd tookit/ir_datasets 
2. python setup.py bdist_wheel
3. pip install dist/ir_datasets-*.whl
4. test with import ir_datasets
```

## 2. Steps for running the code

### 2.1 Preprocessing
```
Run Data_Preprocessing.ipynb
```
Note that "mergedoc_queries" function should be run after Expansion

### 2.2 Document Expansion
```
Run Model/queryprediction_ir.ipynb
```

### 2.3 Topic Classifier
#### 2.3.1 Create training data
```
1. Run Classifier/Temporalia_Query_Reformat.ipynb
2. Run Classifier/traindata_scprits.ipynb
```
#### 2.3.2 Training model and Classifying
```
Run classifier/topic_clsfer.ipynb
```

### 2.4 Retrieval&Evaluation
```
Run Pipeline/retrieval_pipeline.ipynb
```

## Notification
### filepaths
Users should access those files though organizers and put them in the following directories.       
**TREC**
```
Path for 2021's query-doc-relevance file: ./NewTrack_Github/Evaluation/eval/2021/qrels.background          
Path for 2020's query-doc-relevance file: ./NewTrack_Github/Evaluation/eval/2020/qrels.background                    
Path for 2021's topic file: ./NewTrack_Github/Data/Topic/trec2021/newsir21-topics.txt               
Path for 2020's topic file: ./NewTrack_Github/Data/Topic/trec2020/newsir20-topics.txt     
```

**NTCIR**
``` 
Path for Temporalia-1 topic file: ./NewTrack_Github/Data/Topic/Temporalia-1/NTCIR-11TIRTopicsFormalRun.txt        
```
