# coding=utf-8

import nltk

# 1.     CC      Coordinating conjunction 连接词
# 2.     CD     Cardinal number  基数词
# 3.     DT     Determiner  限定词（如this,that,these,those,such，不定限定词：no,some,any,each,every,enough,either,neither,all,both,half,several,many,much,(a) few,(a) little,other,another.
# 4.     EX     Existential there 存在句
# 5.     FW     Foreign word 外来词
# 6.     IN     Preposition or subordinating conjunction 介词或从属连词
# 7.     JJ     Adjective 形容词或序数词
# 8.     JJR     Adjective, comparative 形容词比较级
# 9.     JJS     Adjective, superlative 形容词最高级
# 10.     LS     List item marker 列表标示
# 11.     MD     Modal 情态助动词
# 12.     NN      Noun, singular or mass 常用名词 单数形式
# 13.     NNS     Noun, plural  常用名词 复数形式
# 14.     NNP     Proper noun, singular  专有名词，单数形式
# 15.     NNPS     Proper noun, plural  专有名词，复数形式
# 16.     PDT     Predeterminer 前位限定词
# 17.     POS     Possessive ending 所有格结束词
# 18.     PRP     Personal pronoun 人称代词
# 19.     PRP$     Possessive pronoun 所有格代名词
# 20.     RB     Adverb 副词
# 21.     RBR     Adverb, comparative 副词比较级
# 22.     RBS     Adverb, superlative 副词最高级
# 23.     RP     Particle 小品词
# 24.     SYM     Symbol 符号
# 25.     TO     to 作为介词或不定式格式
# 26.     UH     Interjection 感叹词
# 27.     VB     Verb, base form 动词基本形式
# 28.     VBD     Verb, past tense 动词过去式
# 29.     VBG     Verb, gerund or present participle 动名词和现在分词
# 30.     VBN     Verb, past participle 过去分词
# 31.     VBP     Verb, non-3rd person singular present 动词非第三人称单数
# 32.     VBZ     Verb, 3rd person singular present 动词第三人称单数
# 33.     WDT     Wh-determiner 限定词（如关系限定词：whose,which.疑问限定词：what,which,whose.）
# 34.     WP      Wh-pronoun 代词（who whose which）
# 35.     WP$     Possessive wh-pronoun 所有格代词
# 36.     WRB     Wh-adverb   疑问代词（how where when）





def pos_tag(tokens):
    tagged = nltk.pos_tag(tokens)
    return tagged


if __name__ == '__main__':

    sentence = "At eight o'clock on Thursday morning Arthur didn't feel very good.language processing. " \
               "Written by the creators of NLTK," \
               " it guides the reader through the fundamentals of writing Python programs"
    tokens = nltk.word_tokenize(sentence)
    tagged_data = pos_tag(tokens)
    print(tagged_data)
