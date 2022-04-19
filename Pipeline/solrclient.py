import pysolr
import pandas as pd
from ast import literal_eval
import nltk,string,re,sys

nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))


def text_preprocess(text):
    tokens = nltk.word_tokenize(text)
    text_no_stop_words = ''
    for t in tokens:
        if t not in stop and t not in string.punctuation:
            text_no_stop_words += t + ' '
    return text_no_stop_words.strip()
def getpredictquery(querystring):
    qs = literal_eval(querystring) #qs = literal_eval(query['Query'])
    qs = list(qs)
    return qs
def splitquery(querystring):
    queries = querystring.replace("{'",'').replace("'}",'')
    queries = [i.strip().strip("'") for i in queries.split(',')]
    return queries


class SolrClient():
    
    def __init__(self, server_url='http://localhost', server_port='8983', server_core='WashingtonNews'):
        self.server_url = server_url
        self.server_port = server_port
        self.server_core = server_core
        self.solr = pysolr.Solr(
            server_url + ':' + server_port + '/solr/' + server_core)
        self.results = {
            'qnum' : [],   #1
            'id' : [],      #2
            'title' : [],   #3
            'author' : [],  #4
            'published_date' : [], #5
            'body' : [], #6
            'body_paras_html' : [],
            'body_media' : [],
            'Query' : [],   #7
            'keywords' : [],#8
            'originalrank' : [], #9
            'BM25_score' : [],  #10
        }
    
    def text_preprocess(self, text):
        tokens = nltk.word_tokenize(text)
        text_no_stop_words = ''
        for t in tokens:
            if t not in stop and t not in string.punctuation:
                text_no_stop_words += t + ' '
        return text_no_stop_words.strip()
    
    def search(self, querytext, rows):
        return self.solr.search(self.text_preprocess(querytext), **{"rows": rows, "fl": '*, score'})
        #return self.solr.search(self.text_preprocess(querytext), **{"rows": rows, "fl": 'id,content,source,published_date,title,author,score'})
    
    def preserve_results(self, query, results):
        
        qid = query['qnum'][-3:]
        
        if results.hits == 0:
            self.results['qnum'].append(qid)
            self.results['id'].append("Null")
            self.results['title'].append("Null")
            self.results['author'].append("Null")
            self.results['published_date'].append("Null")
            self.results['body'].append("Null")
            self.results['body_paras_html'].append("Null")
            self.results['body_media'].append("Null")
            self.results['Query'].append("Null")
            self.results['keywords'].append("Null")
            self.results['originalrank'].append("Null")
            self.results['BM25_score'].append("Null")

        rank = 1
        for result in results:
            self.results['qnum'].append(qid)
            self.results['id'].append(result['id'])
            try:
                self.results['title'].append(result['title'][0])
            except KeyError:
                self.results['title'].append("Null")
                
            try:
                self.results['author'].append(result['author'][0])
            except KeyError:
                self.results['author'].append("Null")
                
            try:   
                self.results['published_date'].append(result['published_date'][0])
            except KeyError:
                self.results['published_date'].append("Null")
                
            try:
                self.results['body'].append(result['body'][0])
            except KeyError:
                self.results['body'].append("Null")
                
            self.results['body_paras_html'].append(result['body_paras_html'][0])
            
            self.results['body_media'].append(result['body_media'][0])
            
            try:
                self.results['Query'].append(splitquery(result['Query'][0]))
            except KeyError:
                self.results['Query'].append("Null")
            
            try:
                self.results['keywords'].append(splitquery(result['Key_Words'][0]))
            except KeyError:
                self.results['keywords'].append("Null")
                
            self.results['originalrank'].append(rank)
            self.results['BM25_score'].append(result['score'])
            rank += 1
   
    def get_results(self, query, querytext, rows):
        results = self.search(querytext, rows)
        self.preserve_results(query, results)
#         print('search query {0}'.format(query['qnum']))
#         print("found {0} result(s)".format(results.hits))
#         print("----------------------------------------------------------")
        
    def export_results(self, path, rows):
        rs = pd.DataFrame(self.results)
        rs = rs.drop_duplicates(subset=['id'], keep='first')
#         if len(rs) < 100:
#             print(rs['qnum'][0])
        rs.head(rows).to_csv(path, index = False)
    
    
    
class SolrClient2020():
    
    def __init__(self, server_url='http://localhost', server_port='8983', server_core='WashingtonNews'):
        self.server_url = server_url
        self.server_port = server_port
        self.server_core = server_core
        self.solr = pysolr.Solr(
            server_url + ':' + server_port + '/solr/' + server_core)
        self.results = {
            'qnum' : [],   #1
            'id' : [],      #2
            'title' : [],   #3
            'author' : [],  #4
            'published_date' : [], #5
            'content' : [], #6
            'Query' : [],   #7
            'keywords' : [],#8
            'originalrank' : [], #9
            'BM25_score' : [],  #10
            'source' : [] #11
        }
    
    def text_preprocess(self, text):
        tokens = nltk.word_tokenize(text)
        text_no_stop_words = ''
        for t in tokens:
            if t not in stop and t not in string.punctuation:
                text_no_stop_words += t + ' '
        return text_no_stop_words.strip()
    
    def search(self, querytext, rows):
        return self.solr.search(self.text_preprocess(querytext), **{"rows": rows, "fl": '*,score'})
        #return self.solr.search(self.text_preprocess(querytext), **{"rows": rows, "fl": 'id,content,source,published_date,title,author,score'})
    
    def preserve_results(self, query, results):
        
        qid = query['qnum'][-3:]
        
        if results.hits == 0:
            self.results['qnum'].append(qid)
            self.results['id'].append("Null")
            self.results['title'].append("Null")
            self.results['author'].append("Null")
            self.results['published_date'].append("Null")
            self.results['source'].append("Null")
            self.results['content'].append("Null")
            self.results['Query'].append("Null")
            self.results['keywords'].append("Null")
            self.results['originalrank'].append("Null")
            self.results['BM25_score'].append("Null")

        rank = 1
        for result in results:
            self.results['qnum'].append(qid)
            self.results['id'].append(result['id'])
            try:
                self.results['title'].append(result['title'][0])
            except KeyError:
                self.results['title'].append("Null")
                
            try:
                self.results['author'].append(result['author'][0])
            except KeyError:
                self.results['author'].append("Null")
                
            try:   
                self.results['published_date'].append(result['published_date'][0])
            except KeyError:
                self.results['published_date'].append("Null")
                
            try:
                self.results['source'].append(result['source'][0])
            except KeyError:
                self.results['source'].append("Null")
                
            self.results['content'].append(result['content'][0])
            
            try:
                self.results['Query'].append(splitquery(result['Query'][0]))
            except KeyError:
                self.results['Query'].append("Null")
            
            try:
                self.results['keywords'].append(splitquery(result['Key_Words'][0]))
            except KeyError:
                self.results['keywords'].append("Null")
                
            self.results['originalrank'].append(rank)
            self.results['BM25_score'].append(result['score'])
            rank += 1
   
    def get_results(self, query, querytext, rows):
        results = self.search(querytext, rows)
        self.preserve_results(query, results)
#         print('search query {0}'.format(query['qnum']))
#         print("found {0} result(s)".format(results.hits))
#         print("----------------------------------------------------------")
        
    def export_results(self, path):
        rs = pd.DataFrame(self.results)
        rs = rs.drop_duplicates(subset=['id'], keep='first')
        if len(rs) < 100:
            print(rs['qnum'][0])
        rs.to_csv(path, index = False)
    
