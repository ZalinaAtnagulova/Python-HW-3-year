#G:\Python\Python\3 курс\mystem.exe <text.txt >output.txt -cnisd --eng-gr --format json
import re
class Word:
    def __init__(self, **values):
        self.wf = ''
        self.amount_of_parcings = 0
        self.frequent_lemma = ''
        #self.lemm = {}
        self.frequent_pos = ''
        #self.parts_os = {}
        vars(self).update(values)
                
    def making_array(self, *arrs):
       if self.wf not in all_words:
            all_words.append(self.wf)
            words_class_array.append(self)
       else:
           ind = all_words.index(self.wf)
           existing_word = words_class_array[ind]
           existing_word.amount_of_parcings += self.amount_of_parcings
           for one_lemm in self.lemm:
               if one_lemm not in existing_word.lemm:
                   existing_word.lemm[one_lemm] = 1
               else:
                   existing_word.lemm[one_lemm] += 1
           for one_pos in self.parts_os:
               if one_pos not in existing_word.parts_os:
                   existing_word.parts_os[one_pos] = 1
               else:
                   existing_word.parts_os[one_pos] += 1
       return(all_words, words_class_array)

    def counters(self, elem, counter_lemma, counter_pos):
        for keyl in elem.lemm:
            if elem.lemm[keyl] > counter_lemma:
                elem.frequent_lemma = keyl
                counter_lemma = elem.lemm[keyl]
        for keypos in elem.parts_os:
            if elem.parts_os[keypos] > counter_pos:
                elem.frequent_pos = keypos
                counter_pos = elem.parts_os[keypos]

def lem(a):
    lemm_dic = {}
    lemmas = re.findall('"lex":"(.*?)"', a)
    for lemma in lemmas:
        if lemma not in lemm_dic:
            lemm_dic[lemma] = 1
        else:
            lemm_dic[lemma] += 1
    return lemm_dic

def for_pos(a):
    pos_dic = {}
    pos = re.findall('"gr":"([A-Z]+)[=,]', a)
    for part in pos:
        if part not in pos_dic:
            pos_dic[part] = 1
        else:
            pos_dic[part] += 1
    return pos_dic

f = open('output.txt', 'r', encoding = 'utf-8')
file = f.read()
f.close()
file = file.split('\n')
words_class_array = []
all_words = []
for a in file:
    if 'analysis' in a:
        word_form = re.findall('"text":"(.*?)"', a)
        word = Word(lemm = lem(a), parts_os = for_pos(a))
        word.wf = word_form[0].lower()
        parcings = set(re.findall('"gr":"(.*?)"', a))
        word.amount_of_parcings = len(parcings)
        #word.lem(a)
        #word.for_pos(a)
        word.making_array(all_words, words_class_array)
for elem in words_class_array:
    print(elem.wf, elem.amount_of_parcings, elem.lemm, elem.parts_os)
    #counter_lemma = 0
    #counter_pos = 0
    counting = elem.counters(elem, counter_lemma = 0, counter_pos = 0)
    print(elem.frequent_lemma, elem.frequent_pos)
