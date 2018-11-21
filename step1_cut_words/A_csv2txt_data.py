import pandas as pd 
import json




#将每条评论放入list 中
def get_data(contents_all):
	contents = []
	for content_data in contents_all:
		c = content_data.split('。')
		contents.append(c)
	return contents

#将评论分行写入txt 文件中
def totxt(contents):
	f = open("raw data/contents.txt","w+")
	for content in contents:
		for c in content:
			f.writelines(c+"\n")
	f.close()


if __name__ == '__main__':
    
    #读取csv 中所有新闻所有评论
	excelFile = 'raw data/data_new.csv'
	df = pd.DataFrame(pd.read_excel(excelFile))
	contents_all = df['content'].values
	contents = get_data(contents_all)
	# print(content[1])
	totxt(contents)
