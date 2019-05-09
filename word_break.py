# coding = utf-8

def wordBreak(s):
    res = []
    for i in range(len(s)):
        for j in range(i+1,len(s)-1):
            word = s[i:j]
            if is_word(word):
                res.append(word)
                if j < len(s):
                    res.append(wordBreak(s[j:len(s)]))
                else:
                    return res
            else:
                continue
    return res






def is_word(word):
    worddict = ['a', 'an', 'any', 'anyone','on','one','bar', 'barks', 'ark', 'bark']
    if word in worddict:
        return True
    else:
        return False


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
           candidate = item.pop()
           item.append(candidate)
           flag = True
    return candidate_list





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



if __name__ == '__main__':
    res = wordBreak("anyonebarks89")

    candidate_set = generate_candidate(res)
    candidate_set = get_all_candidate(candidate_set[0])

    print(candidate_set.__len__())
    for item in candidate_set:
        for i in item:
            print(i.content)
        print("-----------")
    # for item in candidate_set:
    #     print(item.content)
    #     print(len(item.next))
    # item_set = []
    # item = []
    # candidate_set = get_all_candidate(candidate_set[0],item_set,item)

    # print(candidate_set)
    # for item in candidate_set:
    #     print(item)





