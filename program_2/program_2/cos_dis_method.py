import numpy as np
from math import log
from scipy import spatial
import time

import idf_method

#Func----遍历两个文档的内容,找出所有词语，返回两个文档的词典(bag of words)
def get_2doc_word_dic(doc_1_dir,doc_2_dir):
    #所有词语的列表
    word_dic = []
    #读取文档1内容
    with open(doc_1_dir,'r',encoding = 'UTF-8') as file:
        text = file.read()
        file.close()
    word_dic = text.split(' ')      #把文档1中的新词加入词典
    #读取文档2内容
    with open(doc_2_dir,'r',encoding = 'UTF-8') as file:
        text = file.read()
        file.close()
    temp_list = text.split(' ')
    for word in temp_list:
        if word not in word_dic:    #把文档2中的新词加入词典
            word_dic.append(word)
    return word_dic


#Func----计算一个文档的tf权重
def get_tf(word_dic,doc_dir):
    #文本向量-tf
    tf_dic = {}
    #初始化文本向量
    for word in word_dic:
        tf_dic[word] = 0
    #读取文档中的词语
    with open(doc_dir,'r',encoding = 'UTF-8') as file:
        text = file.read()
        word_list = text.split(' ')
        file.close()
    #计算词频
    for word in word_list:
        #对出现的词语，词频+1
        count = tf_dic[word]
        tf_dic[word] = count + 1
    #计算tf
    for key,value in tf_dic.items():
        if value != 0:
            tf_dic[key] = 1 + log(value,10)   #   tf
    return tf_dic


#Func----计算一个文档的tf-idf向量
def get_tf_idf_vec(doc_tf,idf_dic):
    #tf-idf权重列表
    doc_tf_idf_list = []
    for key in doc_tf.keys():
        doc_tf_idf_list.append( doc_tf[key] * idf_dic[key] )
    #转换为一位数组
    doc_vec = np.array(doc_tf_idf_list)
    return doc_vec


#Func----计算两个向量之间的余弦距离
def cal_vec_cos_distance(vec1,vec2):
    #计算向量之间余弦值
    cos_sim = 1 - spatial.distance.cosine(vec1, vec2)
    return cos_sim


#-------------------------------封装:余弦距离------------------------------------
#Func----计算两个文档的余弦距离
def cal_doc_cos_distance(doc_1_num,doc_2_num,idf_dic):
    #文档路径
    doc_1_dir = 'C:\\Users\\ljh\\OneDrive\\大三下\\互联网搜索引擎\\课程设计2\\Ch_processed\\baike_ch_processed_' + str(doc_1_num) + '.txt'
    doc_2_dir = 'C:\\Users\\ljh\\OneDrive\\大三下\\互联网搜索引擎\\课程设计2\\Ch_processed\\baike_ch_processed_' + str(doc_2_num) + '.txt'
    #得到词典
    word_dic = get_2doc_word_dic(doc_1_dir,doc_2_dir)
    #计算两个文档各自的tf权重
    doc_1_tf = get_tf(word_dic,doc_1_dir)
    doc_2_tf = get_tf(word_dic,doc_2_dir)
    #计算两个文档各自的tf-idf向量
    doc_1_vec = get_tf_idf_vec(doc_1_tf,idf_dic)
    doc_2_vec = get_tf_idf_vec(doc_2_tf,idf_dic)
    #计算两个文档的余弦距离
    cos_dis = cal_vec_cos_distance(doc_1_vec,doc_2_vec)
    return cos_dis