import time
import idf_method

#-----------------------------执行一次保存所有文档的idf字典-------------------------
print('start time:' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
print('processing...')
idf_method.save_idf_dic()
print('finish time:' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

a = input()