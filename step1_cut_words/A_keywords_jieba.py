from jieba import analyse


def extract_key(file1,file2):
    tfidf = analyse.extract_tags
    for line in open(file1,encoding="utf8"):
        if line.strip()=='':
            continue
        text = line
        #tfidf 仅仅从词的统计信息出发，而没有充分考虑词之间的语义信息
        keywords = tfidf(text,allowPOS=('ns','nr','nt','nz','nl','n', 'vn','vd','vg','v','vf','a','an','i'))
        result=[]

        for keyword in keywords:     
            result.append(keyword)
        #print(result[0])
        fo = open(file2, "a+")
        for j in result:
            fo.write(j)
            fo.write(' ')
        fo.write('\n')
    fo.close()

    print("Keywords Extraction Done!")

if __name__ == '__main__':
    
    file1 = "temp data/contents_full.dat"
    file2 = "temp data/contents_keywords.dat"
    print("关键词提取开始...")     
    extract_key(file1,file2)
        
    print("Done!")

