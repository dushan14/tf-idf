import re
import operator
from tabulate import tabulate
import math
import collections
import nltk
from nltk.corpus import stopwords

path1 = 'document/document1.txt'
path2 = 'document/document2.txt'
path3 = 'document/document3.txt'

with open(path1, encoding="utf8", errors='ignore') as f:
	file1=f.read()

with open(path2, encoding="utf8", errors='ignore') as f:
	file2=f.read()

with open(path3, encoding="utf8", errors='ignore') as f:
	file3=f.read()

file_list=[file1,file2,file3]



def tf_w(tf):
    if(tf==0):
        return 0
    else:
        return 1+math.log10(tf)


def idf(t,docs):
    N=len(docs)
    df_t=0;
    for key, value in docs.items():
        if t in value and value[t]>0:
            df_t+=1

    idf=math.log10(N/df_t)
    return idf

def tf_idf(t,tf,docs):
    return round(tf_w(tf)*idf(t,docs),5)

def sorted_by_tf_idf(dic,docs):
    scored={}
    for key, value in dic.items():
        scored[key]=tf_idf(key,value,docs)

    sorted_words = sorted(scored, key=scored.__getitem__, reverse=True)
    tuple_list=[]
    for k in sorted_words:
        tuple_list.append(tuple((k, scored[k])))
    return tuple_list


def do_process(file_list):
	tokenizer = nltk.RegexpTokenizer(r'\w+')
	stop_words = set(stopwords.words('english'))
	docs={}
	i=1
	for file in file_list:

		lowercased=file.lower()

		#words=re.findall(r'[a-zA-Z]+[\w\']+',lowercased)
		words = nltk.wordpunct_tokenize(lowercased)
		# words = [w for w in words if (w.isalpha() and len(w) != 1 and w not in stop_words)]
		words = [w for w in words if (w.isalpha() and len(w) != 1 )]

		words_set=sorted(set(words))

		word_dic={}

		for word in words_set:
			word_dic[word]=words.count(word)

		word_sorted=collections.OrderedDict(sorted(word_dic.items()))
		# word_sorted = sorted(word_hashmap.items(), key=operator.itemgetter(0))

		# headers=['term', 'frequency']
		# print(tabulate(word_hashmap_sorted, headers=headers))

		doc_name="document%d"%i+":"
		i+=1
		docs[doc_name]=word_sorted


		# print("\n## "+doc_name)
		# print("## full length %d" %  len(words))
		# print("## set length %d" % len(words_set)+"\n")
	
	f=open('answers.txt','w+')
    # index 140323F
	k=23
	docs=collections.OrderedDict(sorted(docs.items()))
   
	f.write("140323F\n")

	f.write('1\n')
	for key, value in docs.items():
		s=key+"%d"%len(value)
		f.write(s+"\n")
	f.write("\n")


	f.write('2\n')
	for key, value in docs.items():
		kth_key=list(value)[k]
		s=key+""+kth_key+",%.3f"%tf_w(value[kth_key])
		f.write(s+"\n")
	f.write("\n")

	f.write('3\n')
	for key, value in docs.items():
		kth_key=list(value)[k]
		s=key+""+kth_key+",%.3f"%idf(kth_key,docs)
		f.write(s+"\n")
	f.write("\n")

	f.write('4\n')
	for key, value in docs.items():
		sorted_tf_idf_tuple_list=sorted_by_tf_idf(value,docs)
		i=1
		s=key
		for item in sorted_tf_idf_tuple_list:
			if i<11:
			   
				s+=item[0]
				if i!=10:
					s+=","
				i+=1
				# print(item[0],item[1])
			else:
				continue
		f.write(s+"\n")
	f.close()
	f=open('answers.txt','r')
	written=f.read()
	f.close()
	print("wrote to file\n\n"+written)

do_process(file_list)
