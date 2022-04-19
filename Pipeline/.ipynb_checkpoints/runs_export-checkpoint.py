import pandas as pd
import os,sys
from datetime import datetime



topicfilepath = '/home/jovyan/playground/projects/TREC2021/NewTrack_Github/Data/Topic/trec2021/topicquery.csv' 
topicfilepath2020 = '/home/jovyan/playground/projects/TREC2021/NewTrack_Github/Data/Topic/trec2020/topicquery.csv'

def dropdupl(df,topicfilepath=topicfilepath):
    dftopic = pd.read_csv(topicfilepath)
    qid = 'Number: '+str(df['qnum'][0])
    originalid = dftopic['docid'].loc[dftopic['num'] == qid].item()
    df.drop(df[df.id == originalid].index, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def caldays(date1,date2):
    dateQ = datetime.fromtimestamp(int(date1)/1000)
    dateB = datetime.fromtimestamp(int(date2)/1000)
    distance = dateQ - dateB
    return distance.days

def recip_r(duration):
    x = abs(duration)/365
    y = 1/(x+1)
    return y


def ExportLtrRun(resultftp,resname):
    try:
        os.remove('./result/%s.csv.gz'%resname)
        print("delete old %s.csv.gz"%resname)
    except:
        print("%s.csv.gz has been removed"%resname)
    files = os.listdir(resultftp)
    try:
        files.remove('.ipynb_checkpoints')
    except:
        pass
    total = pd.DataFrame()
    print("Saving top 100 rank of %s topics to one file..."%len(files))
    for file in files:
        resdf = pd.read_csv(resultftp+file)
        resdf = dropdupl(resdf)
        resdf = resdf[['qnum','id','rank','FinalScore']]
        resdf.insert(loc=1, column='queryid', value='Q0')
        resdf['runtag'] = resname.replace(".csv","")
        total = total.append(resdf.head(100))
    print("Total length is :",len(total))
    print("quick run result look:\n",resdf.head(1))
    total.to_csv("./result/"+resname+'.csv', index=False, header = False, sep='\t')
    os.system("cd result && gzip %s"%resname+".csv")
    
    
def ExportRun2020(resultftp,resname):
    files = os.listdir(resultftp)
    try:
        files.remove('.ipynb_checkpoints')
    except:
        pass
    print("Got %s result files"%(len(files)))
    total = pd.DataFrame()
    for file in files:
        resdf = pd.read_csv(resultftp+file)
        resdf = dropdupl(resdf,topicfilepath=topicfilepath2020)
        resdf['FinalscorewT'] = resdf['BM25_score']/resdf['BM25_score'].abs().max()
        resdf['rank'] = resdf['FinalscorewT'].rank(ascending=False, method='first').astype(int)
        resdf.sort_values(by="rank",ascending=True,inplace=True)
        rundf = resdf[['qnum','id','rank','FinalscorewT']]
        rundf.insert(loc=1, column='queryid', value='Q0')
        rundf['runtag'] = resname.replace(".csv","")     
        total = total.append(rundf.head(100))
        
    print("Total length is :",len(total))
    #print("quick run result look:\n",rundf.head(2))
    if ".csv" not in resname:
        resname = resname + '.csv'
    total.to_csv('../Classifier/eval_result_2020/'+resname, index=False, header = False, sep='\t')
    os.system("cd ../Classifier/eval_result_2020 && gzip %s"%resname)

def ExportRun2020Temp(resultftp,resname,topicfilepath=topicfilepath2020):
    dftopic = pd.read_csv(topicfilepath2020)
    count_atemp=0
    files = os.listdir(resultftp)
    try:
        files.remove('.ipynb_checkpoints')
    except:
        pass
    print("Got %s result files"%(len(files)))
    total = pd.DataFrame()
    for file in files:
        resdf = pd.read_csv(resultftp+file)
        resdf = dropdupl(resdf,topicfilepath=topicfilepath2020)
        resdf['temporalW'] = 0.0
        resdf['Finalscore'] = ''
        dateQ = dftopic['published_date'].loc[dftopic['num'] == 'Number: '+str(resdf['qnum'][0])].item()
        #calculate recency weight
        if not dftopic['published_date'].loc[dftopic['num'] == 'Number: '+str(resdf['qnum'][0])].isnull().item():
            for i in range(len(resdf)):
                if resdf['published_date'][i] != 'Null':
                    resdf.at[i,'temporalW'] = recip_r(caldays(dateQ, resdf['published_date'][i]))
                else:
                    resdf.at[i,'temporalW'] = 0
        else:
            count_atemp += 1
        resdf['BM25_score'] = resdf['BM25_score']/resdf['BM25_score'].abs().max()
        resdf['FinalscorewT'] = resdf['BM25_score'] + resdf['temporalW']
        resdf['rank'] = resdf['FinalscorewT'].rank(ascending=False, method='first').astype(int)
        resdf.sort_values(by="rank",ascending=True,inplace=True)
        rundf = resdf[['qnum','id','rank','FinalscorewT']]
        rundf.insert(loc=1, column='queryid', value='Q0')
        rundf['runtag'] = resname.replace(".csv","")+"temp"      
        total = total.append(rundf.head(100))
    print("%s topics have no publish date."%str(count_atemp))   
    print("Total length is :",len(total))
    #print("quick run result look:\n",rundf.head(2))
    if ".csv" not in resname:
        resname = resname+"temp" + '.csv'
    else:
        resname = resname+"temp"
    total.to_csv('../Classifier/eval_result_2020/'+resname, index=False, header = False, sep='\t')
    os.system("cd ../Classifier/eval_result_2020 && gzip %s"%resname)