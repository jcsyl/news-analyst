import jieba
import logging
import json
import numpy as np

out_file = open('./tmp/data_with_id.json','w',encoding='utf8')
out_file2 = open('./tmp/used_embedding_50.txt','w',encoding='utf-8')

embedding_file = open('./data/embedding_50.txt',encoding='utf8')
embed_lines = embedding_file.readlines()
word_to_index={}
words=[]
rows,cols = len(embed_lines),len(embed_lines[2].split(' '))-2 #第一个是单词，最后一个是换行符
embedding = np.zeros((rows+1,cols),dtype=float)
embedding[rows] = np.random.uniform(-0.01, 0.01, size=(1, cols))
print('加载词向量.....................................')
for i in range(rows):
	tmp_list = embed_lines[i].split(' ')
	word_to_index[tmp_list[0]]=i
	for j in range(cols):
		embedding[i,j]=tmp_list[j+1]  #第一个是单词本身
	words.append(tmp_list[0])
print('加载词向量完成！')

data_file = open('./tmp/data.json','r',encoding='utf8')
data_lines = data_file.readlines()
dictionary = dict()
for line in data_lines:
	item = json.loads(line)
	cut_text = jieba.cut(item['comments'])
	comment_id=[]
	for word in cut_text:
		if word in words:
			if word not in dictionary:
				dictionary[str(word)]=len(dictionary)
				embedding_item=dict()
				embedding_item['word'] = word
				embedding_item['id'] = dictionary[word]
				embedding_str = str(embedding[word_to_index[word]][0])
				for j in range(1,cols):
					embedding_str += ',' + str(embedding[word_to_index[word]][j])
				embedding_item['embedding'] = embedding_str
				embedding_line = json.dumps(embedding_item, ensure_ascii=False) + '\n'
				out_file2.write(embedding_line)
			comment_id.append(dictionary[word])
	item['comment_id'] = comment_id
	comment_id=[]
	new_line = json.dumps(item,ensure_ascii=False)+'\n'
	out_file.write(new_line)

print('word count:',len(dictionary))
out_file.close()
out_file2.close()

