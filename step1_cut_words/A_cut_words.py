import jieba

jieba.load_userdict("SogouLabDic.txt")
jieba.load_userdict("dict_baidu_utf8.txt")
jieba.load_userdict("dict_pangu.txt")
jieba.load_userdict("dict_sougou_utf8.txt")
jieba.load_userdict("dict_tencent_utf8.txt")
#jieba.load_userdict("my_dict.txt")

def get_data(file,file2):
    stopwords = {}.fromkeys([ line.rstrip() for line in open('Stopword.txt','r',encoding='utf8') ])
    result =[]
    f = open(file,"r")
    data = f.readlines()
    f.close()
    print(len(data))
    for line in data:
        if not len(line):
            continue
        seg = jieba.cut(line)
        for i in seg:
            if i not in stopwords:  
                result.append(i)

        fo = open(file2, "a+",encoding='utf8')
        for j in result:       
           fo.write(j)
           fo.write(' ')
        fo.write('\n')
        result=[]
    fo.close()
    print("转换完成!")

if __name__ == '__main__':
    
    #可以修改为评论或则新闻本身
    # file = "raw data/comments.txt"
    # file2 = "temp data/comments_full.dat"
    file = "raw data/contents.txt"
    file2 ="raw data/contents_full.dat"
    print("转换开始...")     
    get_data(file,file2)
        
    print("Done!")






