# coding=utf-8


from nltk import sent_tokenize, word_tokenize
from nltk.corpus import cess_esp as cess
from nltk import UnigramTagger as ut
from nltk import BigramTagger as bt


class TextProccess(object):
    def __init__(self):
        cess_sents = cess.tagged_sents()
        self.uni_tag = ut(cess_sents)
        train = int(len(cess_sents)*90/100)  # 90%
        self.bi_tag = bt(cess_sents[:train])
        self.bi_tag.evaluate(cess_sents[train+1:])

    def text_proccess(self, text):
        result = []
        sents = sent_tokenize(text)
        for sent in sents:
            tokens = word_tokenize(sent)
            tagged_tokens = self.uni_tag.tag(tokens)
            result.append(tagged_tokens)
        return result
