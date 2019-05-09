# coding=utf-8
import re
import json
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import *
import random








# 第二张表
def semantic_prob(semantic_segs_list):

    semantic_tag_list = []
    # 段列表
    segandstag_list = []
    for segs in semantic_segs_list:
        # 三元组
        seg = segs[0]
        seman = segs[2]
        semantic_tag_list.append(seman)
        segandstag_list.append((seg,seman))
    # 语义模式词典
    semantic_dict = {}
    # 统计概率
    segandstag_set = set(segandstag_list)
    for segandstag in list(segandstag_set):
        seg,stag = segandstag
        term = stag + "->" + seg
        key = segandstag_list.count(segandstag) / semantic_tag_list.count(stag) + random.random()/1000000
        dict = {term:key}
        semantic_dict.update(dict)
        with open("../data/seman_prob.json", "w") as seman_porb:
            json.dump(semantic_dict, seman_porb)
    return semantic_dict




# 第一张表
def base_struct_prob(base_list):

    base_porb_dict = {}
    # 去重
    base_set = set(base_list)

    for bs in list(base_set):
        dict = {bs:base_list.count(bs)/len(base_list)}
        base_porb_dict.update(dict)
    with open("../data/base_prob.json","w") as base_porb:
        json.dump(base_porb_dict,base_porb)
    return base_porb_dict




def generate_base_struct(segs):
    base = ""
    for seg,tag,semantic in segs:
        base = base + "[" + semantic + "]"
    return base

def semantic_classify(segs):
    stemmer = SnowballStemmer("english")
    verb = 'V.*'
    noun = 'N.*'
    semantic_segs = []
    c = ""
    for seg,tag in segs:
        if tag == 'gap':
            c = get_gap_type(seg)
        elif re.match(verb, tag) or re.match(noun, tag):
            synsets = wn.synsets(stemmer.stem(seg))
            if len(synsets) > 0:
                c = synsets[0].name()
            else:
                # print("无法分类")
                c = stemmer.stem(seg + ".nn.01")
        else:
            c = tag
        semantic_segs.append((seg,tag,c))
    return semantic_segs





def pos_tag(segs,words,gaps):
    tagged_segs = []
    for seg in segs:
        if seg in words:
            token = nltk.word_tokenize(seg)
            tagged_seg = nltk.pos_tag(token)
        if seg in gaps:
            tagged_seg = [(seg,'gap')]
        tagged_segs = tagged_segs + tagged_seg
    return tagged_segs





def get_gap_type(gap):

    number = "^[0-9]*$"
    char = "^[A-Za-z]+$"
    num_char = "^[A-Za-z0-9]+$"
    special = "^[%&',;=+_@!()?>$\x22]+"

    if re.match(number,gap):
        return 'number'
    elif re.match(char, gap):
        return 'char'
    elif re.match(num_char, gap):
        return 'num_char'
    elif re.match(special, gap):
        return 'speical'
    else:
        return 'all_mixed'

if __name__ == '__main__':
    # nltk.download('punkt')
    # nltk.download('wordnet')


    # list = semantic_classify(pos_tag(segs,words,gaps))
    #
    # print(generate_base_struct(list))
    with open("../data/data0.json",'r') as data:
        lines = data.readlines()
        base_list = []
        segs_list = []
        for line in lines:
            dict = json.loads(line)
            sorted_segs = dict.get("sorted_segs")
            words = dict.get("words")
            gaps = dict.get("gaps")

            tagged_segs = pos_tag(sorted_segs, words, gaps)
            semantic_tagged_segs = semantic_classify(tagged_segs)

            base = generate_base_struct(semantic_tagged_segs)
            base_list.append(base)
            for seg in semantic_tagged_segs:
                segs_list.append(seg)
        # base_struct_prob(base_list)
        # semantic_prob(segs_list)


