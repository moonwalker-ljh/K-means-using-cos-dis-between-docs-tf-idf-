import cos_dis_method
import idf_method

#-----------------------------计算两个文档之间余弦相似度主程序----------------------------
#从文件中读取所有文档中所有词的idf字典
idf_dic = idf_method.load_idf_dic()
#输入需要进行计算余弦相似度的文档的编号
print('文档一编号：',end=' ')
doc_1_num = input()
print('文档二编号：',end=' ')
doc_2_num = input()
print('\n\n')
#输出两个文档的原文
print('文档一原文：')
dir = 'C:\\Users\\ljh\\OneDrive\\大三下\\互联网搜索引擎\\课程设计2\\Ch_processed\\baike_ch_processed_' + str(doc_1_num) + '.txt'
with open(dir,'r',encoding = 'UTF-8') as file:
    text = file.read()
    print(text)
    file.close()
print('\n\n')
print('文档二原文：')
dir = 'C:\\Users\\ljh\\OneDrive\\大三下\\互联网搜索引擎\\课程设计2\\Ch_processed\\baike_ch_processed_' + str(doc_2_num) + '.txt'
with open(dir,'r',encoding = 'UTF-8') as file:
    text = file.read()
    print(text)
    file.close()
print('\n\n')
#计算相似度并输出
sim = cos_dis_method.cal_doc_cos_distance(doc_1_num,doc_2_num,idf_dic)
print('相似度: ' + str(sim))