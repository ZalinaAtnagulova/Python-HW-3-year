from flask import Flask
from flask import render_template, request
from pymystem3 import Mystem
import json
import requests
import re
import os
import nltk
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.collocations import *
#РАБОЧИЙ НА 100% ФАЙЛ

def vk_api(method, **kwargs):
    api_request = 'https://api.vk.com/method/'+method + '?'
    api_request += '&'.join(['{}={}'.format(key, kwargs[key]) for key in kwargs])
    print(api_request)
    return json.loads(requests.get(api_request).text)

def leaders(group_name):
    ids = {}
    leaders = []
    names = []
    id_name_dic={}
    leaders_num={}
    leaders_dict={}
    arr_posts = []
    arr_comments = []
    id_name_link = 'https://api.vk.com/method/groups.getById?group_id='+group_name+'&fileds=name,gid,is_closed'
    ##n = vk_api("groups.getById", group_id=group_name, fileids="name,gid,is_closed")
    
    if json.loads(requests.get(id_name_link).text)['response'][0]['is_closed'] is 0:
        group = str(json.loads(requests.get(id_name_link).text)['response'][0]['gid'])
        group_N = json.loads(requests.get(id_name_link).text)['response'][0]['name']
        group_link = 'https://api.vk.com/method/wall.get?owner_id=-'+group
        comment_link = 'https://api.vk.com/method/wall.getComments?owner_id=-'+group
        resp_wall = requests.get(group_link+'&count=100')
        resp_wall_off = requests.get(group_link+'&count=100&offset=100')
        data = json.loads(resp_wall.text)
        arr_posts.append(data)
        for a in range(1, 10):
            data_off = json.loads(resp_wall_off.text)
            arr_posts.append(data_off)
        for one_set in arr_posts:
            for post in range(1, len(one_set['response'])):
                post_id = data['response'][post]['id']
                count = data['response'][post]['comments']['count']
                command_post = comment_link+'&post_id='+str(post_id)+'&count=100&v=5.52'
                command_post_off = command_post+'&offset=100'
                if count <= 100:
                    poster = json.loads(requests.get(command_post).text)
                    arr_comments.append(poster)
                else:
                    count = count - 100
                    if count <= 100:
                        poster = json.loads(requests.get(command_post_off).text)
                        arr_comments.append(poster)
                    else:
                        rng = int(count/100)+1
                        for roun in range(1, rng):
                            poster = json.loads(requests.get(command_post_off).text)
                            arr_comments.append(poster)
        for cmmnt in arr_comments:
            for pers in range(1,len(cmmnt['response']['items'])):
                if cmmnt['response']['items'][pers]['from_id'] in ids:
                    ids[cmmnt['response']['items'][pers]['from_id']] += 1
                else:
                    ids[cmmnt['response']['items'][pers]['from_id']] = 1
        for one in sorted(ids, key=lambda n: ids[n], reverse=True)[:10]:
            leaders.append(one)
            leaders_num[one]=ids[one]
        for page in leaders:
            if page > 0:
                command = 'https://api.vk.com/method/users.get?user_id='+str(page)+'&fields=first_name,last_name&v=5.52'
                req = json.loads(requests.get(command).text)
                print(command, req)
                stri = req['response'][0]['first_name']+' '+req['response'][0]['last_name']
                names.append(stri)
                id_name_dic[page]=stri
            if page < 0:
                page1 = page*(-1)
                command = 'https://api.vk.com/method/groups.getById?group_id='+str(page1)+'&fileds=name'
                req = json.loads(requests.get(command).text)
                print(req)
                stri = req['response'][0]['name']
                names.append(stri)
                id_name_dic[page]=stri
        for a in leaders_num:
            leaders_dict[id_name_dic[a]]=leaders_num[a]
    else:
        group_N = 'Простите, вы ввели ID закрытой группы, у меня нет к ней доступа'
    return names, leaders_dict, group_N

def fun(text):
    m = Mystem()
    ana = m.analyze(text)
    verb_counter = 0
    word_counter = 0
    nesov = 0
    sov = 0
    trans = 0
    intrans = 0
    intr = []
    tr = []
    verbs = {}
    all_verbs = []
    for b in range(len(ana)):
        a = ana[b]
        if 'text' in a and 'analysis' in a:
            word_counter += 1
            if len(a['analysis'])>0 and a['analysis'][0]['gr'][0] == 'V':
                if a['analysis'][0]['lex'] in verbs:
                    verbs[a['analysis'][0]['lex']] += 1
                    verb_counter += 1
                else:
                    verbs[a['analysis'][0]['lex']] = 1
                    verb_counter += 1
                if a['analysis'][0]['gr'][-5:] == 'несов':
                    nesov += 1
                if a['analysis'][0]['gr'][-5:] != 'несов':
                    sov += 1
                if 'нп' in a['analysis'][0]['gr']:
                    if a['analysis'][0]['lex'] not in intr:
                        intr.append(a['analysis'][0]['lex'])
                        intrans += 1
                else:
                    if a['analysis'][0]['lex'] not in tr:
                        trans += 1
                        tr.append(a['analysis'][0]['lex'])
    for vb in sorted(verbs, key=lambda n: verbs[n], reverse=True):
        all_verbs.append(vb)
    return verb_counter, word_counter, nesov, sov, intrans, trans, all_verbs, intr, tr, text

def split_words(file):
    f = open('subtitles/'+file, 'r', encoding='utf-8')
    text = f.read()
    f.close()
    norm = []
    all_words = word_tokenize(text)
    for word in all_words:
        rus = re.search('([а-яёА-ЯЁ])', word)
        if rus is not None:
            word = re.sub(r'\\N', '', word)
            norm.append(word)
    return norm

def split_stem(norm):
    stemmer = SnowballStemmer("russian")
    stems = []
    for word in norm:
        base = stemmer.stem(word)
        stems.append(base)
    return stems

def search_precise(word):
    names = []
    for root, dirs, files in os.walk('subtitles'):
            for fname in files:
                cont = split_words(fname)
                if word in cont:
                    names.append(fname)
    col = colloc()
    return names, col

def search_stem(word):
    names = []
    for root, dirs, files in os.walk('subtitles'):
            for fname in files:
                words = split_words(fname)
                stems = split_stem(words)
                if word in stems:
                    names.append(fname)
    col = colloc()
    return names, col

def colloc():
    my_corpus = nltk.corpus.PlaintextCorpusReader('./subtitles', '.*\.ass')
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(my_corpus.words(), window_size=4)
    finder.apply_freq_filter(3)
    finder.apply_word_filter(lambda w: re.search('[а-яё]+', w.lower()) is None)
    return finder.nbest(bigram_measures.pmi, 10)


m = Mystem()
app = Flask(__name__)

@app.route('/groupleaders', methods=['get', 'post'])
def commentaries():
    if request.form:
        group_id = request.form['group_id']
        comm_lead, leaders_dict, group_name = leaders(group_id)
        return render_template('vkgroups.html', group_id=group_name, result=comm_lead, data=leaders_dict)
    return render_template('vkgroups.html', data={})


@app.route('/', methods=['get'])
def index():
    return render_template('Zmain.html')

@app.route('/zmystem', methods=['get', 'post'])
def zmystem():
    if request.form:
        text = request.form['text']
        verb_counter, word_counter, nesov, sov, intrans, trans, all_verbs, intr, tr, result = fun(text)
        result = result.replace('\n', '<br>')
        return render_template('verbs_res.html', text=text,
                               verb_counter=verb_counter,
                               word_counter=word_counter, nesov=nesov,
                               sov=sov, intrans=intrans, trans=trans,
                               intr=intr, tr=tr, verbs=all_verbs, result=result)
    return render_template('Zmystem.html')

@app.route('/sub', methods=['get', 'post'])
def sbttls():
    if request.form:
       full_word = request.form['full_word']
       stem = request.form['stem']
       if full_word:
           names, col = search_precise(full_word)
       if stem:
           names, col = search_stem(stem)
       return render_template('subtitles.html', names=names, col=col)
    return render_template('subtitles.html')

if __name__ == '__main__':
    app.run()
