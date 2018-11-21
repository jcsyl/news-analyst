import pandas as pd
import numpy as np
import jieba
import json
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, AffinityPropagation
from sklearn.metrics.pairwise import cosine_similarity

data_file = open('./tmp/data.json',encoding='utf8')
data_lines = data_file.readlines()
print("Total Numbers of Data is %d" % len(data_lines))

token_summary=[]
for i in range(len(data_lines)):
	item = json.loads(data_lines[i])
	comment = item['comments']
	token_summary.append([x for x in jieba.lcut(comment.encode("utf8"))])


string_summary = []
for s in token_summary:
    string_summary.append(" ".join(token for token in s))
print("Getting TFIDF...")
vectorizer = TfidfVectorizer(norm='l2')

sim_matrix = cosine_similarity(vectorizer.fit_transform(string_summary))
#print("the shape of similarity matrix: " % np.shape(sim_matrix))

print("Start clustering...")
start = time.time()
labels = AffinityPropagation().fit_predict(sim_matrix)
print("{:.2f}s".format(time.time() - start))

labels = labels.tolist()
# print(labels)

dict = {}
for i in labels:
	if i not in dict:
		dict[i]=1
	else:
		dict[i]+=1

def dict2list(dic:dict):
	''' 将字典转化为列表 '''
	keys = dic.keys()
	vals = dic.values()
	lst = [(key, val) for key, val in zip(keys, vals)]    
	return lst
list1 = sorted(dict2list(dict), key=lambda x:x[1], reverse=True)
print("按照聚类数量排序:..............................................")
for i, value in list1:
	print('%s %s'%(i, value))

count1=0
for i,value in list1:
	if count1==5:
		break
	for j in range(len(string_summary)):
		if labels[j] ==i:
			f = open("./tmp/AP_without_emb/group-" + str(i) + ".txt", 'a+',encoding="utf-8")
			f.write(string_summary[j])
			f.write('\n')
			f.close()
	count1+=1


# out_file = open('./tmp/data_with_lable.json','w',encoding='utf8')
# for i in range(len(data_lines)):
# 	item = json.loads(data_lines[i])
# 	item['label'] = str(labels[i])
# 	new_line = json.dumps(item,ensure_ascii=False)+'\n'
# 	out_file.write(new_line)
# data_file.close()
# out_file.close()