from math import log


#Func----计算所有文档中所有词的idf权重
def get_idf_dic():
    #idf字典
    idf_dic = {}
    #初始化idf字典
    for doc_num in range(0,500):
        dir = 'C:\\Users\\ljh\\OneDrive\\大三下\\互联网搜索引擎\\课程设计2\\Ch_processed\\baike_ch_processed_' + str(doc_num) + '.txt'
        with open(dir,'r',encoding = 'UTF-8') as file:
            #当前文档中所有词语
            word_list = (file.read()).split(' ')
            for word in word_list:
                if word not in idf_dic.keys():  #文档中新词语加入idf字典
                    idf_dic[word] = 0
            file.close()
    #遍历所有文档统计df
    for doc_num in range(0,500):
        dir = 'C:\\Users\\ljh\\OneDrive\\大三下\\互联网搜索引擎\\课程设计2\\Ch_processed\\baike_ch_processed_' + str(doc_num) + '.txt'
        with open(dir,'r',encoding = 'UTF-8') as file:
            #当前文档中所有词语
            word_list = (file.read()).split(' ')
            #遍历字典中所有词语，查找该文档中是否出现该词语，出现的话df += 1
            for key in idf_dic.keys():
                if key in word_list:    # df += 1
                    idf_dic[key] += 1
            file.close()
    #计算idf
    for key,value in idf_dic.items():
        if value != 0:
            idf_dic[key] = log(500.0/value,10)   #   idf
    return idf_dic


#保存idf字典
def save_idf_dic():
    idf_dic = get_idf_dic()
    with open('C:\\Users\\ljh\\OneDrive\\大三下\\互联网搜索引擎\\课程设计2\\idf_dic.txt','w',encoding='UTF-8') as file:
        for key,value in idf_dic.items():
            file.write(key + ' ' + str(value) + ' \n')
        file.close()


#读取idf字典
def load_idf_dic():
    idf_dic = {}
    with open('C:\\Users\\ljh\\OneDrive\\大三下\\互联网搜索引擎\\课程设计2\\idf_dic.txt','r',encoding='UTF-8') as file:
        for line in file.readlines():
            parts = line.split(' ')
            idf_dic[parts[0]] = float(parts[1])
    return idf_dic