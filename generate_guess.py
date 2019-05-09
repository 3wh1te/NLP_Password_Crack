# coding=utf-8
import queue
import json
import re


class Guess(object):
    def __init__(self,base_structure, base_structure_prob, terminals, terminals_prob,pivot=0):
        self.base_structure = base_structure
        self.base_structure_prob = base_structure_prob
        self.terminals = terminals
        self.terminals_prob = terminals_prob
        self.pivot = pivot
        self.p = base_structure_prob
        for prob in terminals_prob:
            self.p = self.p*prob

    def __cmp__(self, other):
        return self.p <= other.p

    def __lt__(self, other):
        return self.p > other.p


# 终结符和概率
def find_next_terminal(semantic_tag, prob, term,terminals_prob_dict):
    terminal = ""
    p = 0
    # terminal 的列表
    terminal_list = []
    # 概率的列表
    prob_list = []
    # 找到 semantic_tag 且 概率小于prob的所有终结符
    for item in terminals_prob_dict:
        p = terminals_prob_dict.get(item)
        stag = item.split("->")[0]
        terminal = item.split("->")[1]
        if stag == semantic_tag and p <= prob and terminal != term:
            terminal_list.append(terminal)
            prob_list.append(p)

    # 找到小于prob的最大概率和终结符
    if len(prob_list) != 0:
        p = max(prob_list)
        index = prob_list.index(p)
        terminal = terminal_list[index]
    else:
        p = 0
        terminal = ""


    return (terminal,p)

def get_base_structure():
    with open("data/base_prob.json",'r') as fp:
        dict = json.load(fp)
    return dict

def get_terminals_prob():

    with open("data/seman_prob.json", 'r') as fp:
        dict = json.load(fp)
    return dict


def generate_guess():
    # 初始化队列
    que = queue.PriorityQueue()
    # 读取第一张表
    all_base_structures = get_base_structure()
    # 读取第二张表
    terminals_prob_dict = get_terminals_prob()

    for base_structure in all_base_structures:
        # print(base_structure)
        # 转化成数组形式
        bs_list = base_structure[1:len(base_structure)-1].split("][")
        # 得到该基本结构的概率
        base_structure_prob = all_base_structures.get(base_structure)
        # print(base_structure_prob)
        # 找到概率最大所有终结符和其概率
        terminals_list = []
        terminals_prob_list = []
        for pivot in range(len(bs_list)):
            terminal,prob = find_next_terminal(bs_list[pivot], 1, "", terminals_prob_dict)
            terminals_list.append(terminal)
            terminals_prob_list.append(prob)

        guess = Guess(base_structure, base_structure_prob, terminals_list, terminals_prob_list, 0)
        que.put(guess)
        # print(guess.terminals)

    # 概率最大的出队
    c = que.get()
    print(c.terminals)
    # 所有password的list
    passwd_list = []
    while c is not None:
        passwd_list.append(c)
        # print(c.base_structure)
        print(c.terminals)
        pivot = c.pivot
        for i in range(pivot, len(c.terminals)):
            bs_list = c.base_structure[1:len(c.base_structure)-1].split("][")
            # 找到概率最大所有终结符和其概率
            terminals_list = c.terminals
            terminals_prob_list = c.terminals_prob

            terminal, prob = find_next_terminal(bs_list[i], c.terminals_prob[i], c.terminals[i], terminals_prob_dict)
            terminals_list[i] = terminal
            terminals_prob_list[i] = prob

            guess = Guess(c.base_structure, c.base_structure_prob, terminals_list, terminals_prob_list, i)
            if terminal.__len__() != 0:
                que.put(guess)
        c = que.get()

    return passwd_list











if __name__ == '__main__':
    generate_guess()

