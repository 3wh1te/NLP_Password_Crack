# 改变程序运行路径
import sys
import os
import json
import re
import datetime
os.chdir(sys.path[0])

# 引入函数库
sys.path.append('../')
from _functions.functions import change_dict_state




name_of_arithmetic = sys.argv[1]
name_of_model = sys.argv[2]
name_of_dict = sys.argv[3]
gen_size = sys.argv[4]




# 读取模型数据
f = open('./%s/base_structure.txt'%name_of_model,'r')
base_structure_list = json.loads(f.readline())
f.close()
f = open('./%s/structure_elements.txt'%name_of_model, 'r')
elements_table = json.loads(f.readline())
f.close()


# 计算pre-terminal概率
# NEXT办法
def split_elements(string_elements):
    patt = re.compile("L\d+|D\d+|S\d+")
    res = re.findall(patt, string_elements)
    result = json.dumps(res)
    return result


def find_replaceable(elements_list_string):
    elements_list = json.loads(elements_list_string)
    result = {'index': {}}
    for index, i in enumerate(elements_list):
        # print(i)
        # if i[0] != 'L':
        result['index'][str(index)] = -1
    return result


queue = {}
for i in base_structure_list:
    queue_key = split_elements(json.loads(i)['base_structure'])
    # print(queue_key)
    queue[queue_key] = find_replaceable(queue_key)
    queue[queue_key]['probability'] = json.loads(i)['probability']
# print(queue)
print()
init_queue = {}
for k, v in queue.items():
    if v['index'] != {}:
        k_list = json.loads(k)
        # print(k_list)
        p = v['probability']
        for i in v['index'].keys():
            element_position = int(i)
            element_index = v['index'][i] + 1
            # print(element_position,element_index)
            # print(k_list[element_position])
            element_table = elements_table[k_list[element_position]]
            # print(element_table)
            replace_element = json.loads(element_table[element_index])['structure_str']
            replace_probability = json.loads(element_table[element_index])['probability']
            # print(replace_probability)
            k_list[element_position] = replace_element
            p = p * replace_probability
            v['index'][i] += 1
        k_str = json.dumps(k_list)
        init_queue[k_str] = {}
        init_queue[k_str]['index'] = json.dumps(v['index'])
        init_queue[k_str]['probability'] = p
        init_queue[k_str]['base_structure'] = k
# print(init_queue)
# for k,v in init_queue.items():
#   print(k,v)

queuep_order = []
for k, v in init_queue.items():
    if v['probability'] not in queuep_order:
        queuep_order.append(v['probability'])
queuep_order.sort(reverse=True)


# print(queuep_order)

def find_highest(queue, queuep_order):
    while 1:
        highest_probability = queuep_order[0]
        highest_key = ''
        for k, v in queue.items():

            if v['probability'] == highest_probability:
                # print(v['probability'],123123123,k)
                # highest_probability = v['probability']
                highest_key = k
                break
        if highest_key == '':
            queuep_order.pop(0)
        else:
            break
    # print(highest_key)
    return highest_key, queuep_order


def next(queue, queuep_order, sort_queue):
    # 添加进新队列
    # print(len(queuep_order),22122223)
    highest_key, queuep_order = find_highest(queue, queuep_order)
    # print(type(highest_key))
    poped = {}
    poped[highest_key] = queue[highest_key]
    poped = json.dumps(poped)
    # 替换旧队列
    old_element = queue[highest_key]
    # print("............",old_element)
    old_element_structure = json.loads(old_element['base_structure'])
    for p, i in json.loads(old_element['index']).items():
        # print(old_element)

        elements_list = elements_table[old_element_structure[int(p)]]
        next_index = i + 1
        if next_index < len(elements_list):

            nep = json.loads(elements_list[next_index])['probability']
            oep = json.loads(elements_list[i])['probability']
            probability = old_element['probability'] / oep * nep
            new_key = json.loads(highest_key)
            new_key[int(p)] = json.loads(elements_list[next_index])['structure_str']
            # print(old_element_structure)
            new_element_index = json.loads(old_element['index'])
            new_element_index[p] = next_index
            queue[json.dumps(new_key)] = {'index': json.dumps(new_element_index), 'probability': probability,
                                          'base_structure': old_element['base_structure']}
            if probability not in queuep_order:
                queuep_order.append(probability)
            if sort_queue:
                queuep_order.sort(reverse=True)
                # print(len(queuep_order),22123)
        # print(elements_table[old_element_structure[int(p)]])
        # old_element_structure[p] =
    # 删除旧元素
    del queue[highest_key]
    return queue, poped, queuep_order


gen_size = int(gen_size)
sorted_queue = []
count = 0

last_time = datetime.datetime.now()
for i in range(gen_size):
    queue = init_queue
    if count % 100 == 0:
        sort_queue = True
    else:
        sort_queue = False

    queue, poped, queuep_order = next(queue, queuep_order, sort_queue)
    sorted_queue.append(poped)
    count += 1
    if count % 10000 == 0:
        now_time = datetime.datetime.now()
        took_time = now_time - last_time
        last_time = now_time
        # print("[+] Took: %s. GenPass: %s" % (took_time, count))
        change_dict_state(name_of_arithmetic, name_of_model, name_of_dict, state="已生成: %s. 耗时: %s."%(count, took_time))

result_file_name = './%s/%s.txt'%(name_of_model,name_of_dict)
g = open(result_file_name, 'w+')
for i in sorted_queue:
    pw = json.loads(i)
    for j in pw.keys():
        passwd = ''.join(json.loads(j))
        g.write(passwd + "\n")
g.close()
change_dict_state(name_of_arithmetic, name_of_model, name_of_dict, state="生成完成. 共计: %s."%(count))


