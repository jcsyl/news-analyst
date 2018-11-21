import numpy as np
import json
import jieba
from sklearn.cluster import KMeans, AffinityPropagation
from sklearn.metrics.pairwise import cosine_similarity
data_file = open('./tmp/data_with_embedding.json',encoding='utf8')
data_lines = data_file.readlines()

X = np.zeros((len(data_lines),50),dtype=float)
for i in range(len(data_lines)):
	item = json.loads(data_lines[i])
	X[i]=item['embedding'].split(',')


sim_matrix = cosine_similarity(X)
ap = AffinityPropagation()
labels = ap.fit_predict(sim_matrix)


cluster_centers_indices = ap.cluster_centers_indices_
n_clusters_ = len(cluster_centers_indices)

# print(labels, len(labels))

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
	for j in range(len(data_lines)):
		token_summary=[]
		if labels[j] ==i:
			item = json.loads(data_lines[j])
			comment = item['comments']
			token_summary.append([x for x in jieba.lcut(comment.encode("utf8"))])
			string_summary = " ".join(token for token in token_summary[0])
			f = open("./tmp/AP_with_emb/group-" + str(i) + ".txt", 'a+',encoding="utf-8")
			f.write(string_summary)
			f.write('\n')
			f.close()
	count1+=1

# data_file2 = open('./tmp/data.json',encoding='utf8')
# data_lines2 = data_file2.readlines()
# out_file = open('./tmp/data_with_lable.json','w',encoding='utf8')
# for i in range(len(data_lines2)):
# 	item = json.loads(data_lines2[i])
# 	item['label'] = str(labels[i])
# 	new_line = json.dumps(item,ensure_ascii=False)+'\n'
# 	out_file.write(new_line)
# data_file.close()
# data_file2.close()

