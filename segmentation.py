# coding = utf-8

import utils
import json
import threading
from nltk.corpus import wordnet as wn


# 获取密码
def get_passwd(path):
    passwd_list = []
    with open(path, 'r') as info:
        info_dicts = info.readlines()
        for dict in info_dicts:
            passwd = json.loads(dict)['passwordplaintext']
            passwd_list.append(passwd)
    return passwd_list


class Candidate():
    def __init__(self,content, next):
        self.content = content
        self.next = next
        # 0 表示未被遍历
        self.flag = 0

    def has_next(self):
        if len(self.next) == 0:
            return False
        else:
            return True


# 切分密码
def segment_passwd(passwd):
    res = []
    for i in range(len(passwd)):
        for j in range(i + 1, len(passwd) - 1):
            word = passwd[i:j]
            if utils.is_word(word):
                res.append(word)
                if j < len(passwd):
                    res.append(segment_passwd(passwd[j:len(passwd)]))
                else:
                    return res
            else:
                continue
    return res


def generate_candidate(result):
    candidate_set = []
    for i in range(0,result.__len__(),2):
        content = result[i]
        next_set = generate_candidate(result[i+1])
        candidate = Candidate(content,next_set)
        candidate_set.append(candidate)

    return candidate_set


def get_all_candidate(candidate):
    candidate_list = []
    item = []
    item.append(candidate)
    flag = True
    while flag:
       flag = False
       if candidate.has_next():
            next = candidate.next
            for i in next:
                if i.flag == 0:
                    candidate = i
                    item.append(candidate)
                    # print(candidate.content)
                    candidate.flag = 1
                    flag = True
                    break
            if not flag:
                item.pop()
                if item.__len__() != 0:
                    candidate = item.pop()
                    item.append(candidate)
                    flag = True
       else:
           res = []
           for i in item:
               res.append(i)
           candidate_list.append(res)
           item.pop()
           if item.__len__() != 0:
               candidate = item[item.__len__()-1]
               flag = True
    return candidate_list
# As previously stated, it contains high order N-gram frequencies
# that can help us rank the segmentations by likelihood. Let KN
# be an N-gram corpus and f(KN ) the total frequency of N-grams in corpus K
# 这个词出现的频率/所有这个长度的词出现的频率


def best_ngram_score(segs):
    score = 0
    length = len(segs)

    if length == 1:
        score = uni_gram_probability(segs)
    elif length == 2:
        score = bi_gram_probability(segs)
    elif length == 3:
        score = tri_gram_probability(segs)

    if score == 0:
        for i in range(1,3):
            a = best_ngram_score(segs[:i])
            b = best_ngram_score(segs[i:])
            tem_score = a*b
            if tem_score > score:
                score = tem_score
    return score


def uni_gram_probability(segments):
    print("d")
    return 1


def bi_gram_probability(segments):
    print("d")
    return 2


def tri_gram_probability(segments):
    print("d")
    return 3


def parse_passwd(passwd):

    # 最大覆盖长度
    max_coverage_len = 0
    # 最大覆盖率
    max_coverage = 0
    # 覆盖率最大的切割方式
    max_coverage_candidates = []


    res = segment_passwd(passwd)

    candidate_set = generate_candidate(res)
    # candidate_set = get_all_candidate(candidate_set[0])

    for candidate in candidate_set:
        candidate_list = get_all_candidate(candidate)
        for item in candidate_list:
            # 覆盖长度
            coverage_len = 0
            for i in item:
                coverage_len = coverage_len + len(i.content)
            if coverage_len >= max_coverage_len:
                max_coverage_len = coverage_len
    max_coverage = max_coverage_len/len(passwd)
    # print(max_coverage_len)
    # print(max_coverage)

    candidate_set = generate_candidate(res)
    for candidate in candidate_set:
        candidate_list = get_all_candidate(candidate)
        for item in candidate_list:
            # 覆盖长度
            coverage_len = 0
            for i in item:
                coverage_len = coverage_len + len(i.content)
            if coverage_len == max_coverage_len:
                list = []
                for i in item:
                    list.append(i.content)
                max_coverage_candidates.append(list)


    words = []
    if max_coverage_len > 0:
        words = max_coverage_candidates[0]
        min_num = max_coverage_candidates[0].__len__()
        for c in max_coverage_candidates:
            num = c.__len__()
            if num < min_num:
                min_num = num
                words = c
    # print(words)


    gaps = []
    rest_passwd = [passwd]
    for word in words:
        tem = []
        for p in rest_passwd:
            tem += p.split(word)
        rest_passwd = tem
    for gap in rest_passwd:
        if gap != '':
            gaps.append(gap)
    # print(gaps)

    # 按位置进行排序
    segs = words + gaps
    segs_pos = []
    # print(segs)

    for seg in segs:
        pos = passwd.find(seg)
        segs_pos.append(pos)
    sorted_segs = []
    for seg in segs:
        min_pos = min(segs_pos)
        min_index = segs_pos.index(min_pos)
        segs_pos[min_index] = len(passwd)
        sorted_segs.append(segs[min_index])
    # print(sorted_segs)


    return (sorted_segs,words,gaps)


def run(passwd_list,file_name):
    count = 0
    with open("data/"+ file_name +".json",'w') as ps:
        for passwd in passwd_list:
            if count%100 == 0:
                print(count)
            count += 1
            # print(passwd)
            sorted_segs, words, gaps = parse_passwd(passwd)
            dict = {'sorted_segs': sorted_segs, 'words':words, 'gaps': gaps}
            # dict_list.append(dict)
        # for dict in dict_list:
            json.dump(dict, ps)
            ps.write("\n")

if __name__ == "__main__":
    dict_list = []
    passwd_list = []
    passwd_list = get_passwd("data/collection_32.json")
    total = passwd_list.__len__()
    # passwd = "any1one23barks98"
    # passwd_list.append(passwd)
    last = 48000
    start = 0
    while last >= 6000:
        threading.Thread(target=run, args=[passwd_list[start:start+6000],"data"+str(start)]).start()
        start += 6000
        last -= 6000
    if last > 0:
        threading.Thread(target=run, args=[passwd_list[start:start + last], "data" + str(start)]).start()








