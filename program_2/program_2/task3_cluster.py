import cluster_method
import time


#返回一个20个类中文档编号列表的字典  类编号:[文档编号，文档编号...]
def get_temp_cluster_doc_id_dic():
    cluster_doc_id_dic = {}
    for id in range(0,20):
        cluster_doc_id_dic[id] = []
    return cluster_doc_id_dic
     
    
#返回一个20个类各自的重心      类编号:[，...]
def get_temp_cluster_centroid_dic():
    cluster_centroid_dic = {}
    for id in range(0,20):
        cluster_centroid_dic[id] = []
    return cluster_centroid_dic



#------------------------------------准备工作
#获取500个文档的tf-idf权重列表的字典
print('start time:' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
print('获取500个文档各自的tf-idf权重向量...')
_500doc_tf_idf_dic = cluster_method.get_500doc_tf_idf_dic()
print('finish time:' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
print('')


#----------------------------------算法开始
#得到20个类中 文档编号列表的字典      { 类编号：[doc_id, doc_id ....]  
#                                       类编号：[]
#                                       ...
#                                      }
cluster_doc_id_dic = get_temp_cluster_doc_id_dic()
#得到20个类各自的重心的字典           { 类编号：[ ]
#                                       类编号： []  
#                                       ...  
#                                      }
cluster_centroid_dic = get_temp_cluster_centroid_dic()
#初始化，给20个类选择各自的种子
for cluster_id in range(0,20):
    doc_id  = (cluster_id + 1) * 25 -1        #24、49、74。。
    cluster_centroid_dic[cluster_id] = _500doc_tf_idf_dic[doc_id][:]



print('start time:' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
print('开始K-Means算法...')
#开始K‐Means算法
##停止条件：固定次数的递归,100次
for iteration_time in range(0,5):
    #得到临时的20个类中 文档编号列表的字典
    temp_cluster_doc_id_dic = get_temp_cluster_doc_id_dic()
    #遍历每个文档
    for doc_id in range(0,500):
        #遍历每个类，找出和其重心距离最近的类
        min_cos_dis = cluster_method.cal_doc_vec_cos_distance(doc_id,cluster_centroid_dic[0],_500doc_tf_idf_dic)
        min_cos_dis_cluster_id = 0
        for cluster_id in range(1,20):
            cos_dis = cluster_method.cal_doc_vec_cos_distance(doc_id,cluster_centroid_dic[cluster_id],_500doc_tf_idf_dic)
            if cos_dis > min_cos_dis:   #比当前余弦距离更近的话更新最近距离和对应类编号，这里进行比较的是余弦相似度，所以值越大余弦距离越小
                min_cos_dis = cos_dis
                min_cos_dis_cluster_id = cluster_id
        #把该文档加入到该类
        temp_cluster_doc_id_dic[min_cos_dis_cluster_id].append(doc_id)
    #根据20个类中 文档编号列表的字典计算20个类各自的新的重心的字典
    temp_cluster_centroid_dic = cluster_method.cluster_doc_id_dic_2_cluster_centroid_dic(temp_cluster_doc_id_dic,_500doc_tf_idf_dic)  
    #更新所有类的重心
    for cluster_id in cluster_centroid_dic.keys():
        if temp_cluster_centroid_dic[cluster_id] != 0:  
            #如果新计算得到的该类的向量为0，说明该类中目前没有文档，保持之前的重心不变，否则更新为最新的重心
            cluster_centroid_dic[cluster_id] = temp_cluster_centroid_dic[cluster_id][:]
    print('time ' + str(iteration_time) + ' finished at  ' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    #结束算法时保存20个类中 文档编号列表的字典
    if iteration_time == 4:
        cluster_doc_id_dic = temp_cluster_doc_id_dic.copy()

print('finish time:' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
print('')



#-------------------------------得到最大的三个类的编号
sort_cluster_size = []    #[(类的大小,类编号),()...]
for cluster_id in cluster_doc_id_dic.keys():
    sort_cluster_size.append(  (len(cluster_doc_id_dic[cluster_id]) ,  cluster_id)   )
#从大到小排序
sort_cluster_size.sort(reverse = True)
#最大的五个类的编号列表  [#1_cluster_id , #2_cluster_id ,#3_cluster_id]
top3_cluster_id_list = [sort_cluster_size[0][1] , sort_cluster_size[1][1] , sort_cluster_size[2][1]]


#------------------------------计算这三个类中所有文档 离所在类重心的距离的字典
doc_2_cluster_centroid_cos_dis_dic = {}     # { 
                                            #   类编号:[ (doc_2_cluster_centroid_cos_dis , doc_id) , () ,() ]
                                            #   
                                            #  }

for i in range(0,3):
    cluster_id = top3_cluster_id_list[i]
    doc_2_cluster_centroid_cos_dis_dic[cluster_id] = []
    for doc_id in cluster_doc_id_dic[cluster_id]:
        cos_dis = cluster_method.cal_doc_vec_cos_distance(doc_id, cluster_centroid_dic[cluster_id], _500doc_tf_idf_dic)
        doc_2_cluster_centroid_cos_dis_dic[cluster_id].append( (cos_dis, doc_id) )

for cluster_id in doc_2_cluster_centroid_cos_dis_dic.keys():
    #按和重心的距离从小到大排序
    doc_2_cluster_centroid_cos_dis_dic[cluster_id].sort()



#------------------------------输出结果
print('输出结果：')
num = 1
for cluster_id in doc_2_cluster_centroid_cos_dis_dic.keys():
    print('第' + str(num) + '大的类编号：', end='')
    print(cluster_id)
    print('其中的五个代表性文档：',end='')
    for i in range(0,5):
        print(doc_2_cluster_centroid_cos_dis_dic[cluster_id][i][1], end='\t')
    print('')
    num += 1

#防止意外退出
a = input()