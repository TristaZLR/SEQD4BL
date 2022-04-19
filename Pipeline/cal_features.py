import pandas as pd
import os,sys
import torch
from datetime import datetime
from ast import literal_eval
import math

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print("We are using: ",device)
from sentence_transformers import SentenceTransformer, util
qurlsimilarity = SentenceTransformer('nq-distilbert-base-v1')
qurlsimilarity.to(device)

def getpredictquery(querystring):
    qs = literal_eval(querystring) #qs = literal_eval(query['Query'])
    qs = list(qs)
    return qs

def turnstring(sentlist):
    doc=''
    for sen in sentlist:
        doc+=" "+sen
    return doc

def kwtostr(kwdf):
    temp = list(literal_eval(kwdf))
    return turnstring(temp).strip()

def cleanquery(querystr):
    querystr=querystr.replace('["',"")
    querystr=querystr.replace(']"',"")
    querystr=querystr.replace('\\',"")
    return querystr

def getsimilarity_queries(Q_queries,D_queries):
    Q_queries = [cleanquery(i) for i in getpredictquery(Q_queries)]
    D_queries = getpredictquery(D_queries)
    #print(Q_queries,D_queries)
    simscore = 0
    for q in Q_queries:
        maxium = 0
        desc_embedding = qurlsimilarity.encode(q)
        for d in D_queries:
            passage_embedding = qurlsimilarity.encode(d)
            similarity = util.pytorch_cos_sim(desc_embedding, passage_embedding)
            similarity = similarity.item()
            maxium = max(maxium,similarity)
        simscore += maxium
    return simscore
        
            
        

def getsimilarity_keywords(Q_keywords,D_Keywords):
    Q_keywords = kwtostr(Q_keywords)
    D_keywords = kwtostr(D_Keywords)
    #print(Q_keywords,",",D_keywords)
    similarities = 0
    desc_embedding = qurlsimilarity.encode(Q_keywords)
    passage_embedding = qurlsimilarity.encode(D_keywords)
    similarity = util.pytorch_cos_sim(desc_embedding, passage_embedding)
    similarity = similarity.item()
    if similarity > 0:
        similarities += similarity
    return similarities

def getsimilarity_title(Q_title,D_title):
    
    similarities = 0
    desc_embedding = qurlsimilarity.encode(Q_title)
    passage_embedding = qurlsimilarity.encode(D_title)
    similarity = util.pytorch_cos_sim(desc_embedding, passage_embedding)
    similarity = similarity.item()
    if similarity > 0:
        similarities += similarity
    return similarities

def getsimilarity_query_title(Q_title,D_queries):    
    similarities = 0
    D_queries = getpredictquery(D_queries)
    for query in D_queries:
        desc_embedding = qurlsimilarity.encode(Q_title)
        passage_embedding = qurlsimilarity.encode(query)
        similarity = util.pytorch_cos_sim(desc_embedding, passage_embedding)
        similarity = similarity.item()
        if similarity > 0:
            similarities += similarity
    return similarities


def caldays(date1,date2):
    dateQ = datetime.fromtimestamp(int(float(date1))/1000)
    dateB = datetime.fromtimestamp(int(float(date2))/1000)
    distance = dateQ - dateB
    return distance.days

def recip_r(duration):
    x = abs(duration)/365
    y = 1/(x+1)
    return y


def clean(s):
    s = s.replace("\xa0"," ")
    s = s.replace("\n","")
    s = s.replace("\t","")
    s = s.replace("\'","")
    s = s.replace('\"',"")
    s = s.replace("[...]","")
    s = re.sub(r'^https?:\/\/.*[\r\n]*', '', s, flags=re.MULTILINE)
    s = re.sub('<a[^<]+</a>', "",s)
    return s

def getDocLen(doc):
    doc = clean(doc).strip()
    doclength = len(doc.split())
    return doclength


def cal_featues(df_queries,df_result):
    df_result['hasDate'] = '' 
    df_result['TmpoR']=''
    df_result['Sim_Titles']=''
    df_result['Sim_Keywords']=''
    df_result['Sim_Queries']=''
    df_result['DocLength']=''
    df_result['IsTempo'] = ''
    
    for i in range(len(df_result)):
        
        qid = str(df_result['qnum'][0])
        df_query = df_queries[df_queries['num']=="Number: "+qid]
        
        #feature has publish Date or not
        if math.isnan(df_query['published_date'].item()) \
        or df_query['published_date'].item()=='Null':
            df_result.at[i,'hasDate'] = 0       
        else:
            df_result.at[i,'hasDate'] = 1
            
        df_result.at[i,'IsTempo'] = df_query['IsTempo'].item()
            
        #get document length
        try:
            df_result.at[i,'DocLength'] = getDocLen(df_result['content'][i])
        except:
            df_result.at[i,'DocLength'] = 0
            
        #feature temporal recency    
        if math.isnan(df_query['published_date'].item()) \
        or df_result['published_date'][i]=='Null':
            df_result.at[i,'TmpoR'] = 0
        else:
            df_result.at[i,'TmpoR'] = recip_r(caldays(df_query['published_date'].item(),df_result['published_date'][i]))
            
            
        #Feature similarity of key words
        try:
            df_result.at[i,'Sim_Keywords'] = getsimilarity_keywords(df_query['Key_Words'].item(),df_result['keywords'][i])
        except:
            df_result.at[i,'Sim_Keywords'] = 0
            
        #Feature similarity of titles    
        try:
            df_result.at[i,'Sim_Titles'] = getsimilarity_title(df_query['title'].item(),df_result['title'][i])     
        except:
            df_result.at[i,'Sim_Titles'] = 0
            
        #Feature similarity of title and predicted queries    
        try:
            df_result.at[i,'Sim_Queries'] = getsimilarity_query_title(df_query['Query'].item(),df_result['Query'][i])
            
        except:
            df_result.at[i,'Sim_Queries'] = 0
            
    #df_result['BM25_score'] = df_result['BM25_score']/df_result['BM25_score'].abs().max()  #normalization
    
    return df_result[['qnum','hasDate','IsTempo','TmpoR','Sim_Titles','Sim_Keywords','Sim_Queries','DocLength','BM25_score','id']]


def rerank_Freshness(df):
    df['Sim_Queries'] = df['Sim_Queries']/df['Sim_Queries'].abs().max()
    df['BM25_score'] = df['BM25_score']/df['BM25_score'].abs().max()
    df["FinalScore"] = 0.03*df['IsTempo']*df['TmpoR']+0*df['Sim_Titles']+0*df['Sim_Keywords']+0*df['Sim_Queries']+df['BM25_score']
    df['rank'] = df['BM25_score'].rank(ascending=False, method='first').astype(int)
    df.sort_values(by="rank",ascending=True,inplace=True)
    return df
    
def rerank_Title(df):
    df['Sim_Queries'] = df['Sim_Queries']/df['Sim_Queries'].abs().max()
    df['BM25_score'] = df['BM25_score']/df['BM25_score'].abs().max()
    df["FinalScore"] = 0*df['IsTempo']*df['TmpoR']+0.5*df['Sim_Titles']+0*df['Sim_Keywords']+0*df['Sim_Queries']+df['BM25_score']
    df['rank'] = df['BM25_score'].rank(ascending=False, method='first').astype(int)
    df.sort_values(by="rank",ascending=True,inplace=True)
    return df

def rerank_Title_Fr(df):
    df['Sim_Queries'] = df['Sim_Queries']/df['Sim_Queries'].abs().max()
    df['BM25_score'] = df['BM25_score']/df['BM25_score'].abs().max()
    df["FinalScore"] = 0.03*df['IsTempo']*df['TmpoR']+0.5*df['Sim_Titles']+0*df['Sim_Keywords']+0*df['Sim_Queries']+df['BM25_score']
    df['rank'] = df['BM25_score'].rank(ascending=False, method='first').astype(int)
    df.sort_values(by="rank",ascending=True,inplace=True)
    return df