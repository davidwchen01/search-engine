from flask import Flask,render_template,request,flash
import forms
import os
import json
import math
import time
import retriever
SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

num_docs = 33876
mi = open("mergedindex.txt","r")
pos = open("tokenpos.txt","r")
tfidf = open("tfdf.txt","r")
urls = open("urls4.txt","r")
pos_dict = eval(pos.read())
tfidf_dict = eval(tfidf.read())
urls_dict = eval(urls.read())

@app.route('/', methods = ['GET','POST'])
def form():
    form = forms.SearchForm(request.form)
    links = list()
    if form.validate_on_submit():
        query = form.search.data.split()
        n_score = dict()
        start_time = time.time()
        counter = 0
        unique_query = list() #Only get the unique tokens (Note: we still give extra weighting to duplicate words in the scoring during retrieval)
        for i in query:
            if i in retriever.stop_words:
                counter+=1
        if counter/len(query) < 0.60: #If stop words comprise less than 60% of the query, ignore them
            for i in query:
                if i not in retriever.stop_words and i in pos_dict.keys():
                    unique_query.append(i)
        else:
            unique_query = [i for i in set(query) if i in pos_dict.keys()]
        if len(unique_query) > 6: #If the query is longer than 6 words, shorten the query
            new_length = int(len(unique_query)//2)
            terms = sorted([i for i in unique_query if i in pos_dict.keys()],key = lambda x:tfidf_dict[x][1])[0:new_length] #Get the top-half of the query words
        else:
            terms = unique_query
        doc_vector = dict()
        for i in terms:
            doc_len = 0
            query_weight = (1+ math.log(query.count(i),10) * (1 + math.log(num_docs/tfidf_dict[i][1])))
            t_pos = pos_dict[i]
            mi.seek(t_pos) #Read the line that contains the token's dictionary
            t_dict = eval(mi.readline())
            #Calculate tf-idf score for each document that has at least 1 word in the query
            for k,v in t_dict.items():
                for doc,freq in v.items():
                    if doc not in doc_vector.keys():
                        doc_vector[doc] = 0
                    term_weight = (1 + math.log(freq,10)) * (1 + math.log(num_docs/tfidf_dict[i][1]))
                    doc_vector[doc]+=(term_weight*query_weight)
            url_list = sorted([(k,v) for k,v in doc_vector.items()],key = lambda x:x[1],reverse = True)[0:10] #Get top 10 results and sort by score
            links = [urls_dict[link_num[0]] for link_num in url_list] #Get the url links
        print("--- %s ms ---" % (time.time()*1000 - start_time*1000)) #Used for timing the program, units are in milliseconds
        mi.seek(0) #Reset file pointer
        return render_template('search.html',form = form,links = links)
    return render_template('search.html',form = form)

        
app.run(host='localhost', port=5000,debug = True)