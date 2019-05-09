# 改变程序运行路径
import sys
import os
import json
import time
os.chdir(sys.path[0])

# 引入函数库
sys.path.append('../')
from _functions.functions import get_random_data
from _functions.functions import get_password_from_search_result
from _functions.functions import change_model_state
from _functions.functions import save_train_data


name_of_arithmetic = sys.argv[1]
name_of_model = sys.argv[2]
train_corpus = sys.argv[3]
train_data_size = sys.argv[4]
case_sensitive = sys.argv[5]

# 获取随机数据用于训练
change_model_state(name_of_arithmetic, name_of_model, state='开始获取训练数据')
random_data = get_random_data(train_corpus, train_data_size, random_seed=name_of_model)
password_list = get_password_from_search_result(random_data)
save_train_data(password_list, name_of_model)
change_model_state(name_of_arithmetic, name_of_model, state='获取训练数据完成')
#time.sleep(600)

# 主体部分开始
base_structure_with_p = {}  # {'abc':{'times':00000005,'probability':0.042}}
LDS_with_p = {}  # {'D4':{'1234':2,4321:1},'S2':{'@@':1}}
for i in password_list:
    password = i['password']
    base_structure = []
    structure_type = 'None'
    structure_len = 0
    structure_str = ''
    for index, i in enumerate(password):
        # 密码中的这个字符是字母
        if i.isalpha():
            # 如果跟上一个字符类型不一样，就先把上一个填到list中
            # 如果是第一个字符，就先填None
            if structure_type != 'L':
                structure_element = structure_type + str(structure_len)
                # 为第一张概率表做准备
                base_structure.append(structure_element)
                # 为第二张概率表做准备
                if not structure_element in LDS_with_p.keys():
                    LDS_with_p[structure_element] = {}
                if not structure_str in LDS_with_p[structure_element].keys():
                    LDS_with_p[structure_element][structure_str] = 1
                else:
                    LDS_with_p[structure_element][structure_str] += 1
                # 重新定义，为下一次变化做准备
                structure_type = 'L'
                structure_len = 0
                structure_str = ''
            structure_len += 1
            structure_str += i
        # 密码中的这个字符是数字
        elif i.isdigit():
            # 如果跟上一个字符类型不一样，就先把上一个填到list中
            # 如果是第一个字符，就先填None
            if structure_type != 'D':
                structure_element = structure_type + str(structure_len)
                # 为第一张概率表做准备
                base_structure.append(structure_element)
                # 为第二张概率表做准备

                if not structure_element in LDS_with_p.keys():
                    LDS_with_p[structure_element] = {}
                if not structure_str in LDS_with_p[structure_element].keys():
                    LDS_with_p[structure_element][structure_str] = 1
                else:
                    LDS_with_p[structure_element][structure_str] += 1
                # 重新定义，为下一次变化做准备
                structure_type = 'D'
                structure_len = 0
                structure_str = ''
            structure_len += 1
            structure_str += i
        # 密码中的这个字符是符号
        else:
            # 如果跟上一个字符类型不一样，就先把上一个填到list中
            # 如果是第一个字符，就先填None
            if structure_type != 'S':
                structure_element = structure_type + str(structure_len)
                # 为第一张概率表做准备
                base_structure.append(structure_element)
                # 为第二张概率表做准备
                if not structure_element in LDS_with_p.keys():
                    LDS_with_p[structure_element] = {}
                if not structure_str in LDS_with_p[structure_element].keys():
                    LDS_with_p[structure_element][structure_str] = 1
                else:
                    LDS_with_p[structure_element][structure_str] += 1
                structure_type = 'S'
                structure_len = 0
                structure_str = ''
            structure_len += 1
            structure_str += i
        # 密码中的最后一个字符
        if index + 1 == len(password):
            structure_element = structure_type + str(structure_len)
            # 为第一张概率表做准备
            base_structure.append(structure_element)
            # 为第二张概率表做准备
            if not structure_element in LDS_with_p.keys():
                LDS_with_p[structure_element] = {}
            if not structure_str in LDS_with_p[structure_element].keys():
                LDS_with_p[structure_element][structure_str] = 1
            else:
                LDS_with_p[structure_element][structure_str] += 1
    # 一个密码处理完后，将None删除，并转换为字符串，为了用作下面dict的key
    base_structure = ''.join(base_structure[1:])
    if base_structure in base_structure_with_p.keys():
        base_structure_with_p[base_structure]['times'] += 1
    else:
        base_structure_with_p[base_structure] = {'times': 1}


# 输出第一张表到文件
base_structure_list = []
for k,v in base_structure_with_p.items():
    output_tmp = dict()
    output_tmp['times'] = "{:09}".format(v['times'])
    output_tmp['base_structure'] = k
    output_tmp['probability'] = v['times']/int(train_data_size)
    base_structure_list.append(json.dumps(output_tmp))
    del output_tmp
# 按概率排序
base_structure_list.sort(reverse=True)
f = open('./%s/base_structure.txt'%name_of_model,'w+')
f.write(json.dumps(base_structure_list))
f.close()


# 输出第二张表到文件
del LDS_with_p['None0']
elements_table = {}
for k, v in LDS_with_p.items():
    structure_element = k
    output = []
    total_times = 0
    for structure_str, times in v.items():
        total_times += times
    for structure_str, times in v.items():
        element = {
            'times': "{:09}".format(times),
            'probability': times / total_times,
            'structure_str': structure_str
        }
        output.append(json.dumps(element))
        LDS_with_p[k][structure_str] = times / total_times
    # print("Structure Element: %s"%structure_element)
    output.sort(reverse=True)
    elements_table[structure_element] = output
f = open('./%s/structure_elements.txt'%name_of_model, 'w+')
f.write(json.dumps(elements_table))
f.close()
change_model_state(name_of_arithmetic, name_of_model, state='训练完成')