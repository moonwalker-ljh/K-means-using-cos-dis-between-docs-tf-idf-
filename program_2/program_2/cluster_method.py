import cos_dis_method
import idf_method
import numpy as np

#Func----获取500个文档的词典(bag of words)
def get_500doc_word_dic():
    #词典
    word_dic = []
    #遍历500个文档
    for doc_num in range(0,500):
        dir = 'C:\\Users\\ljh\\OneDrive\\大三下\\互联网搜索引擎\\课程设计2\\Ch_processed\\baike_ch_processed_' + str(doc_num) + '.txt'
        with open(dir,'r',encoding = 'UTF-8') as file:
            #当前文档中所有词语
            word_list = (file.read()).split(' ')
            for word in word_list:
                if word not in word_dic:  #文档中新词语加入词典
                    word_dic.append(word)
            file.close()
    return word_dic


#Func----获取500个文档的tf-idf权重列表的字典
def get_500doc_tf_idf_dic():
    #得到所有文档的词典
    word_dic = get_500doc_word_dic()

    #所有文档的tf-idf权重列表的字典         {
    #                                          文档编号：[tf-idf, tf-idf, ......]
    #                                           ....
    #                                        }
    doc_tf_idf_dic ={}

    #从文件中读取所有文档中所有词的idf字典
    idf_dic = idf_method.load_idf_dic()
    #计算每一个文档的tf-idf列表，并插入到字典中
    for doc_num in range(0,500):
        doc_dir = 'C:\\Users\\ljh\\OneDrive\\大三下\\互联网搜索引擎\\课程设计2\\Ch_processed\\baike_ch_processed_' + str(doc_num) + '.txt'
        #该文档的tf字典
        doc_tf = cos_dis_method.get_tf(word_dic,doc_dir)
        #该文档的tf-idf权重列表
        doc_tf_idf_list = []
        for key in doc_tf.keys():
            doc_tf_idf_list.append( doc_tf[key] * idf_dic[key] )
        #将该文档的编号和tf-idf列表插入到字典中
        doc_tf_idf_dic[doc_num]=doc_tf_idf_list

    return doc_tf_idf_dic


#Func----根据20个类中 文档编号列表的字典计算20个类各自的重心
def cluster_doc_id_dic_2_cluster_centroid_dic(cluster_doc_id_dic,_500doc_tf_idf_dic):
    cluster_centroid_dic = {}
    #遍历每个类
    for cluster_id in cluster_doc_id_dic.keys():
        if len(cluster_doc_id_dic[cluster_id]) == 0:    
            sum_tf_idf = 0          #该类中没有文档，保持之前的重心不变，0为记号
        else:
            #该类的中文档的tdf-idf向量的和
            sum_tf_idf = []
            doc_id = cluster_doc_id_dic[cluster_id][0]
            sum_tf_idf = _500doc_tf_idf_dic[doc_id][:]
            #该类中现有的文档编号
            for doc_id in cluster_doc_id_dic[cluster_id][1:]:
                #将向量进行相加
                for index in range(0,len(sum_tf_idf)):
                    sum_tf_idf[index] += _500doc_tf_idf_dic[doc_id][index]
            #除以该类中的文档数量得到重心
            for index in range(0,len(sum_tf_idf)):
                sum_tf_idf[index] = sum_tf_idf[index] / len(cluster_doc_id_dic[cluster_id])
        #把该类的重心插入到临时字典
        cluster_centroid_dic[cluster_id] = sum_tf_idf
    return cluster_centroid_dic



#Func----一个文档和一个向量之间的距离
def cal_doc_vec_cos_distance(doc_num,vec,_500doc_tf_idf_dic):
     #计算两个文档各自的tf-idf向量
    doc_vec = np.array(_500doc_tf_idf_dic[doc_num])
     #计算两个文档的余弦距离
    cos_dis = cos_dis_method.cal_vec_cos_distance(doc_vec,vec)
    return cos_dis