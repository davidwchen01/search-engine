import json
import math
import time

stop_words = {"a","about","above","after","again","against","all","am","an",
"and","any","are","aren't","as","at","be","because","been","before","being","below","between",
"both","both","but","by","can't","cannot","could","couldn't","did","didn't","do","does","doesn't",
"doing","don't","down","during","each","few","for","from","further","had","hadn't","has","hasn't",
"have","haven't","having","he","he'd","he'll",'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 
'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 
'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 
"that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 
'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 
'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under',
 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 
 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
  "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn'
  , "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 
'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't","may","also"}


def query(query:list):
    pos_dict = eval(pos.read())
    tfidf_dict = eval(tfidf.read())
    urls_dict = eval(urls.read())
    n_score = dict()
    start_time = time.time()
    unique_query = set(query) #Only get the unique tokens
    doc_vector = dict()
    for i in unique_query:
        doc_len = 0
        if i in pos_dict.keys(): #If a document contains i
            query_weight = (1+ math.log(query.count(i),10) * (1 + math.log(num_docs/tfidf_dict[i][1])))
            t_pos = pos_dict[i]
            mi.seek(t_pos)
            t_dict = eval(mi.readline())
            for k,v in t_dict.items():
                for doc,freq in v.items():
                    if doc not in doc_vector.keys():
                        doc_vector[doc] = 0
                    term_weight = (1 + math.log(freq,10)) * (1 + math.log(num_docs/tfidf_dict[i][1]))
                    doc_vector[doc]+=(term_weight*query_weight)
    url_list = sorted([(k,v) for k,v in doc_vector.items()],key = lambda x:x[1],reverse = True)[0:10]
    links = list()
    for i in url_list:
        links.append(urls_dict[i[0]])
    print("--- %s seconds ---" % (time.time() - start_time))
    links.reverse()
    return links