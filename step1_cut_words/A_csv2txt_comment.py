import pandas as pd 
import json




#将每条评论放入list 中
def get_data(comments):
	comments = []
	for comment_data in comments_all:
		json_data = json.loads(comment_data)
		for comment in json_data:
			comments.append(comment["c_content"])
	return comments

#将评论分行写入txt 文件中
def totxt(comments):
	f = open("raw data/comments.txt","w+")
	for comment in comments:
		f.writelines(comment+"\n")
	f.close()


if __name__ == '__main__':
    
    #读取csv 中所有新闻所有评论
	excelFile = './raw data/data_new.csv'
	df = pd.DataFrame(pd.read_excel(excelFile))
	comments_all = df['comment'].values
	comment = get_data(comments_all)
	totxt(comment)
