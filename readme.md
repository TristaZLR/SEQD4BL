# Selectively Expanding Queries and Documents for News Background Linking
## install requirements
### solr environment
Take references to solr guidebook.
> https://solr.apache.org/guide/8_6/solr-tutorial.html#index-the-techproducts-data

We provide a sample for solr configuration and index setting in ./Pipeline/solrconfig
You can replace it in your own solr directory
### Java environment
if you have conda: 
- conda install -c conda-forge openjdk=11
### other requirements
- pip install requirements
### Data Requirements
> [Washington Post Corpus V4](https://trec.nist.gov/data/wapost/)
>> Access permit required.
> We are using topics of News Track [2021](https://trec.nist.gov/act_part/tracks/news/newsir21-topics.txt) and [2020](https://trec.nist.gov/act_part/tracks/news/newsir20-topics.txt).

> [NTCIR Temporalia test collection](http://ntcirtemporalia.github.io/NTCIR-11/collection.html)
>> We will need their topics of Temporalia-1 for training the topic classfier
>> Need to apply for access.

### Evaluation Scripts
> https://github.com/usnistgov/trec_eval/

qrels need to be prepared in ./Evaluation/eval/
- Download repository to Evaluation Folder 
- cd ./Evaluation/scripts/trec_eval
- git clone https://github.com/usnistgov/trec_eval/


### data preprocessing tool
> [ir-dataset](https://github.com/allenai/ir_datasets)
clone it to the tookit folder. Following their installation guide.
Or you can also choose to build from our souce. Following bellow steps:
1. cd tookit/ir_datasets 
2. python setup.py bdist_wheel
3. pip install dist/ir_datasets-*.whl
4. test with import ir_datasets

## Steps for running the code

### Preprocessing
run Data_Preprocessing.ipynb
Note that "mergedoc_queries" function should be run after Expansion
### Expansion
run Model/queryprediction_ir.ipynb

### Topic Classifier
#### training data creation
1. run Classifier/Temporalia_Query_Reformat.ipynb
2. Classifier/traindata_scprits.ipynb
#### training model and classifying
run classifier/topic_clsfer.ipynb

### Retrieval&Evaluation
run Pipeline/retrieval_pipeline.ipynb

## Notification
### filepaths
Users should access those files though organizers
TREC
> ./NewTrack_Github/Evaluation/eval/2021/qrels.background
> ./NewTrack_Github/Evaluation/eval/2020/qrels.background
> ./NewTrack_Github/Data/Topic/trec2021/newsir21-topics.txt
> ./NewTrack_Github/Data/Topic/trec2020/newsir20-topics.txt

NTCIR
> ./NewTrack_Github/Data/Topic/Temporalia-1/NTCIR-11TIRTopicsFormalRun.txt