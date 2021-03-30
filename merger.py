import json
import re
import linecache
f1 = "findex1.txt"
f2 = "findex2.txt"
f3 = "findex3.txt"
f4 = "findex4.txt"
f5 = "findex5.txt"
t1 = "titles2.txt"
t2 = "titles3.txt"
t3 = "titles4.txt"
t4 = "titles5.txt"
t5 = "titleslast.txt"

merged_index = "mindex2.txt"

def get_term(item):
    return list(item.keys())[0]


def merge():
    '''Merges the indices in alphabetical order by reading line by line'''
    mi = open("mergedindex.txt","a")
    o1 = open(f1,"r")
    o2 = open(f2,"r")
    o3 = open(f3,"r")
    o4 = open(f4,"r")
    o5 = open(f5,"r")
    l1 = o1.readline()
    l2 = o2.readline()
    l3 = o3.readline()
    l4 = o4.readline()
    l5 = o5.readline()
    while True:
        index_dict = dict()
        term_list = list()
        ind_map = [dict(),dict(),dict(),dict(),dict()]
        c_list = [0,0,0,0,0]
        if l1 == l2 == l3 == l4 == l5:
            #The only scenario where this evaluates to True is if all files reached EOF
            break
        if l1:
            temp1 = eval(l1)
            term_list.append(get_term(temp1))
            ind_map[0] = temp1
        else:
            term_list.append("")
        if l2:
            term_list.append(get_term(eval(l2)))
            ind_map[1] = eval(l2)
        else:
            term_list.append("")
        if l3:
            term_list.append(get_term(eval(l3)))
            ind_map[2] = eval(l3)
        else:
            term_list.append("")
        if l4:
            term_list.append(get_term(eval(l4)))
            ind_map[3] = eval(l4)
        else:
           term_list.append("")
        if l5:
            term_list.append(get_term(eval(l5)))
            ind_map[4] = eval(l5)
        else:
           term_list.append("")
        minterm = sorted(term_list)[4]
        for i in term_list:
            if i != "" and i < minterm:
                minterm = i
        if term_list.count(minterm) > 1:
            ind_list = list()
            for i in range(len(term_list)):
                if term_list[i] == minterm:
                    c_list[i] = 1
                    ind_list.append(i)
            for i in ind_list:
                for k,v in ind_map[i].items():
                    if k not in index_dict.keys():
                        index_dict[k] = dict()
                    for k2,v2 in v.items():
                        index_dict[k][k2] = v2
        else:
            t_index = term_list.index(minterm)
            c_list[t_index] = 1
            for k,v in ind_map[t_index].items():
                if k not in index_dict.keys():
                    index_dict[k] = dict()
                for k2,v2 in v.items():
                    index_dict[k][k2] = v2
        try:
            mi.write(str(index_dict) + "\n")
        except:
            pass
        if c_list[0] == 1:
            l1 = o1.readline()
        if c_list[1] == 1:
            l2 = o2.readline()
        if c_list[2] == 1:
            l3 = o3.readline()
        if c_list[3] == 1:
            l4 = o4.readline()
        if c_list[4] == 1:
            l5 = o5.readline()
    mi.close()





def convert_to_str():
    '''Converts a file representing a dictionary into individual lines for each key,value pair for easier processing'''
    with open(f5,"r") as f:
        a = f.read()
        a = a.strip("}{")
        c = a.split("}, ")
        temp = open("findex5.txt","w")
        for i in c:
            temp.write("{" + i + "}" + "}\n")


def merge_titles():
    main_dict = dict()
    t1 = open("titles2.txt","r")
    t2 = open('titles3.txt',"r")
    t3 = open('titles4.txt','r')
    t4 = open('titles5.txt','r')
    t5 = open('titleslast.txt','r')
    d1 = json.load(t1)
    d2 = json.load(t2)
    d3 = json.load(t3)
    d4 = json.load(t4)
    d5 = json.load(t5)
    for k,v in d1.items():
        temp = str(int(k)-1)
        main_dict[temp] = v
    for k,v in d2.items():
        temp = str(int(k)-1)
        main_dict[temp] = v
    for k,v in d3.items():
        temp = str(int(k)-1)
        main_dict[temp] = v
    for k,v in d4.items():
        temp = str(int(k)-1)
        main_dict[temp] = v
    for k,v in d5.items():
        temp = str(int(k)-1)
        main_dict[temp] = v
    with open("mtitle.txt",'w') as tf:
        json.dump(main_dict,tf)



def get_tfdf():
    '''Gets term-frequency and document frequency for each token'''
    tfidf_dict = dict()
    with open("mergedindex.txt","r") as f:
        while True:
            a = f.readline()
            if a == "":
                break
            d = eval(a)
            for k,v in d.items():
                freq = 0
                for v2 in v.values():
                    freq+=v2
                tfidf_dict[k] = (freq,len(v.keys()))
    with open("tfdf.txt","w") as tf:
        json.dump(tfidf_dict,tf)

def position():
    '''Assigns terms their respective positions in the merged index file'''
    pos_dict = dict()
    with open("mergedindex.txt","r") as f:
        pos = 0
        while True:
            a = f.readline()
            if a == "":
                break
            d = eval(a)
            term = list(d.keys())[0]
            pos_dict[term] = pos
            pos+=len(a)+1
        a = open("tokenpos.txt","w")
        a.write(str(pos_dict))
    
    

if __name__ == "__main__":
    position()