import numpy as np
import json
from sklearn import svm

embed_file = open('./tmp/used_embedding_50.txt',encoding='utf8')
data_file = open('./tmp/data_with_id.json',encoding = 'utf8')

embed_lines = embed_file.readlines()
data_lines = data_file.readlines()

embeddings = np.zeros((len(embed_lines),50),dtype=float)
for i in range(len(embed_lines)):
	embedding_item = json.loads(embed_lines[i])
	embeddings[i] = embedding_item['embedding'].split(',')


idf_dict =dict()
word_to_index =dict()
count=0
for i in range(len(data_lines)):
	item = json.loads(data_lines[i])
	for word in item['comment_id']:
		if word not in idf_dict:
			word_to_index[word] = len(idf_dict)
			idf_dict[word] = []
		if count not in idf_dict[word]:
			idf_dict[word].append(count)
	count+=1

doc_num = len(data_lines)
for key in idf_dict.keys():
	idf_dict[key] = np.log(doc_num * 1.0 / len(idf_dict[key]))

out_file = open('./tmp/data_with_embedding.json','w',encoding='utf8')
for i in range(len(data_lines)):
	item = json.loads(data_lines[i])
	word_id = item['comment_id']
	tmp_embedding = np.zeros((1,50),dtype=float)
	for word in word_id:
		tf = word_id.count(word)*1.0/len(word_id)
		tf_idf = tf*idf_dict[word]
		tmp_embedding+=tf_idf*embeddings[word]

	embedding_str = str(tmp_embedding[0,0])
	for j in range(1,50):
		embedding_str += ',' + str(tmp_embedding[0, j])
	item['embedding'] = embedding_str
	new_line = json.dumps(item, ensure_ascii=False) + '\n'
	out_file.write(new_line)
out_file.close()