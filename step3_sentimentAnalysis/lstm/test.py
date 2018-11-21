import numpy as np
import jieba

string='酒店的环境非常好，价格也便宜，值得推荐'
words=jieba.lcut(string)
words=np.array(words).reshape(1,-1)
print(words)