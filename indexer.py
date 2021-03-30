import json
import os
from bs4 import BeautifulSoup
import sys
from collections import OrderedDict
import random

urlhash_dict = dict()
sim_dict = dict()
url_dict = dict()
def create_file_list():
    file_list = []
    directory = 'developer/DEV'
    files = os.listdir(directory)
    for i in files:
        sd = directory + "/" + i
        more_files = os.listdir(sd)
        for t in more_files:
            fn = sd + "/" + t
            file_list.append(fn)
    return file_list

def calculateWordScore(word):
    '''Gives a word a 30 binary score'''
    score = 0
    for i in word:
        if ord(i):
            score+=((ord(i))+3)*3
    return str(int(bin((score * 4331231917)%1073741824)[2:]))[0:30]

def calculateScore(tokens):
    '''Calculates the score of a webpage through the sum of word values and gives the page a 30 binary fingerprint'''
    sum_array = list()
    for i in range(30):
        sum_array.append(0)
    for k,v in tokens.items():
        counter = 0
        if k not in urlhash_dict.keys():
            urlhash_dict[k] = calculateWordScore(k)
        for i in urlhash_dict[k]:
            if counter == len(urlhash_dict[k]):
                break
            else:
                if i == '0':
                    sum_array[counter]-=v
                else:
                    sum_array[counter]+=v
            counter+=1
    fingerprint = list()
    for i in range(len(sum_array)):
        fingerprint.append(0)
    for i in range(len(sum_array)):
        if sum_array[i] > 0:
            fingerprint[i] = 1
        else:
            fingerprint[i] = 0
    return fingerprint


def isSimilar(score):
    '''Compares the fingerprint of one webpage with all the currently indexed webpages'''
    if score in sim_dict.values():
        return True
    for v in sim_dict.values():
        counter = 0
        union = list()
        for i in range(len(score)):
            if score[i] == v[i]:
                counter+=1
                union.append(score[i])
            else:
                union.append(score[i])
                union.append(v[i])
        sim = (float(counter)/float(len(union)))
        if sim > 0.975: #If the document is 97.5% similar ignore the doc.
            return True
    return False

def main():
    file_name = "index"
    file_ext = ".txt"
    file_list = create_file_list()
    u_counter = 1
    f_counter = 1
    u = 0
    index_dict = dict()
    token_dict = dict()
    title_dict = dict()
    for f in file_list:
        #If the indexer is about to read a large file and the current index in memory is of a certain size, empty index into memory
        if os.path.getsize(f)/1000 >= 50000 and sys.getsizeof(index_dict)/1000 >= 4000: 
            print(f"Dumping dictionary of size {sys.getsizeof(index_dict)/1000}")
            with open(file_name+file_ext,"w") as c:
                json.dump(OrderedDict(sorted(index_dict.items())),c)
                f_counter+=1
                file_name = file_name[0:6] + str(f_counter)
                index_dict = dict()
        with open(f) as of:
            u+=1
            data = json.load(of)
            token_dict = dict()
            soup = BeautifulSoup(data['content'],"html.parser")
            text = soup.get_text().split()
            for i in text: 
                if i not in token_dict.keys() and i.isalnum():
                    token_dict[i] = 1
                elif i in token_dict.keys():
                    token_dict[i]+=1
            score = calculateScore(token_dict)
            if u%5000 == 0 or (u > 20000 and u%2500 == 0): #Used for checkpoints in indexing
                print(f"Reached {u} documents")

            if not isSimilar(score):
                #If the page is not a duplicate, tokenize the page and index it
                for s in soup.find_all("strong"): #Strong tagged tokens get added twice to increase weighting
                    if s.string:
                        for i in s.string.split():
                            text.append(i)
                            text.append(i)
                for heading in soup.find_all(["h1","h2","h3"]): #Header tokens get added 4x to increase weighting
                    if heading.string:
                        for i in heading.string.split():
                            text.append(i)
                            text.append(i)
                            text.append(i)
                            text.append(i)
                for i in text: #Add tokens of the webpage to the index
                    if i in index_dict.keys() and i.isalnum():
                        if u_counter not in index_dict[i].keys():
                            index_dict[i][u_counter] = 1
                        else:
                            index_dict[i][u_counter]+=1
                    elif i.isalnum():
                        index_dict[i] = {u_counter:1}
                sim_dict[u_counter] = score
                url_dict[u_counter] = data['url'] #Map url
                u_counter+=1
                if soup.title: #(Can ignore this, is used primarily for aesthetics)
                    title_dict[u_counter] = soup.title.string
        if (sys.getsizeof(index_dict)/1000 > 5000): #IF the dictionary exceeds this size, empty the index into disk
            with open(file_name+file_ext,"w") as f:
                print(f"Dumping dictionary of size {sys.getsizeof(index_dict)/1000}")
                json.dump(OrderedDict(sorted(index_dict.items())),f)
                f_counter+=1
                file_name = file_name[0:6] + str(f_counter)
                index_dict = dict()
            with open("titles" + str(f_counter) + file_ext,"w") as tf:
                json.dump(title_dict,tf)
                title_dict = dict()

    #Offload any remaining information
    with open(file_name+file_ext,"w") as f:
        json.dump(OrderedDict(sorted(index_dict.items())),f)
    with open("urls4.txt","w") as uf:
        json.dump(url_dict,uf)
    #This is merely used to make the gui look better 
    with open("titleslast.txt","w") as tf:
        json.dump(title_dict,tf)

main()