import jieba
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import jieba.analyse
import re

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

def count_similarity(sen1,sen2):
    sentence1 = sen1
    line = sen2.strip().encode('utf-8').decode('utf-8', 'ignore')  # 去除每行首尾可能出现的空格，并转为Unicode进行处理
    line1 = re.sub("[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）]+".encode('utf-8').decode("utf8"), "".encode('utf-8').decode("utf8"),
                   line)
    wordList = list(jieba.cut(line1))
    sentence2 = [x for x in wordList]
    sen1_embedding = np.zeros((1, 50), dtype=float)
    sen2_embedding = np.zeros((1, 50), dtype=float)
    for word in sentence1:
        if word in words:
            sen1_embedding +=  embedding[word_to_index[word]]
    for word in sentence2:
        if word in words:
            sen2_embedding += embedding[word_to_index[word]]
    sim = cosine_similarity(sen1_embedding,sen2_embedding)
    return sim
def get_dict(file):
    lyric= ''
    f=open(file,'r',encoding='utf8')
    for i in f:
        lyric+=f.read()
    # print(lyric)#自动加+'\n'
    # 考虑了相邻词的语义关系、基于图排序的关键词提取算法TextRank
    result=jieba.analyse.textrank(lyric,topK=50,withWeight=True)
    keywords = dict()
    for i in result:
        keywords[i[0]]=i[1]
    return keywords

def selsect_Max_similarity(file1):
    dict = get_dict(file1)
    dict_list =  list(dict.keys())[0:10]
    print('关键词：-------------------------------')
    print(dict_list)
    group_file = open(file1,encoding='utf8')
    data_lines = group_file.readlines()
    print('评论数量：',len(data_lines))
    max_sim=0
    for i in range(len(data_lines)):
        sim = count_similarity(dict_list,data_lines[i])[0][0]
        if sim>max_sim:
            max_sim=sim
            flag = i
    print('最典型评论：-----------------------------------')
    print(data_lines[flag])
    return data_lines[flag]


if __name__ == '__main__':
    file = './tmp/AP_with_emb/group-29.txt'
    sentence = selsect_Max_similarity(file)

