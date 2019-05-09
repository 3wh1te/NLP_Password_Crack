#coding = utf-8

from nltk.corpus import words
from nltk.corpus import webtext
from nltk.corpus import wordnet
import re
import nltk
# worddict = ['a', 'an', 'any', 'anyone','on','one','bar', 'barks', 'ark', 'bark']
import json
# 生成所有子串
def substrings(string):
    string_list = []
    length = len(string)

    # 分别找长度为 1 2 3 4...n 的子串
    for i in range(length):

        # 子串长度
        n = i + 1
        # 子串数量
        num = length - i
        for j in range(num):
            seg = Segment(string[j:j + n], j, j + n)
            string_list.append(seg)
    return string_list


class Segment:

    def __init__(self, content, start, end):
        self.content = content
        self.start = start
        self.end = end


class Candidate:

    def __init__(self):
        self.seg_list = []
        self.num = 0
        self.end = 0
        self.coverage = 0

    def add_candidate(self, segment):
        # 比较起始位置和结束位置
        end = self.end
        start = segment.start
        if end <= start:
            self.seg_list.append(segment)
            self.num = self.num + 1
            self.end = segment.end
            self.coverage = self.coverage + len(segment.content)


# 定义密码对象
class Password:
    def __init__(self, content):
        self.content = content
        self.len = 0
        # 最优切割
        self.candidates_word = []
        self.gap = []


# def is_word(seg):
#     corpus = webtext.words()
#     try:
#         return corpus.index(seg)
#     except ValueError:
#         return -1

worddict = words.words()
def is_word(word):
    if word in worddict:
        return True
    else:
        return False


def classify_semantic(segment):
    semantic_seg = []

    for seg, pos in segment:
        c = ""
        if pos is "gap":
            c = 'number'
        elif pos == 'noun':
            c = 'dog.n.03'
        elif pos == 'noun' or 'verb':
            print("hdkjask")
        semantic_seg.append([seg,pos,c])
    return semantic_seg


# 判断gap类型：数字、字母、特殊符号、混合
def get_gap_type():
    digital = '^[0-9]*$'
    letter = '^[A-Za-z]+$'
    special = "^[%&;()=?><.,':\"_+@#$\x22]+"

    re.match()



if __name__ == '__main__':
    # nltk.download('wordnet')s
    # print(wordnet.synsets("dog"))
    special = "^[%&;-()=?><.,':\"_+@#$\x22]+"
    re.match(special,"sd&><.,")
