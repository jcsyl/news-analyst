import pandas as pd
import json 
import os


def get_data(comments):
	comments = []
	for comment_data in comments_all:
		json_data = json.loads(comment_data)
		for comment in json_data:
			comments.append(comment["c_content"])
	return comments

df = pd.DataFrame(pd.read_excel('./data/data.csv'))
comments_all = df['comment'].values
comments_list = get_data(comments_all)

data_out_file = open('data.json','w',encoding='utf8')
item = dict()
count=0
for comment in comments_list:
	item['comments'] = str(comment)
	new_line = json.dumps(item,ensure_ascii=False)+'\n'
	data_out_file.write(new_line)
	count+=1
print("comments count:",count)
