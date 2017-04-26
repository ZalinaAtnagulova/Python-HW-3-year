from flask import Flask
from flask import url_for, render_template, request, redirect
from pymystem3 import Mystem
from collections import Counter
import json
import requests

def leaders(group):
    ids = {}
    arr_posts = []
    arr_comments = []
    group_link = 'https://api.vk.com/method/wall.get?owner_id=-'+group
    comment_link = 'https://api.vk.com/method/wall.getComments?owner_id=-'+group
    resp_wall = requests.get(group_link+'&count=100')
    resp_wall_off = requests.get(group_link+'&count=100&offset=100')
    data = json.loads(resp_wall.text)
    arr_posts.append(data)
    for a in range(1, 10):
        #resp_wall1 = requests.get(group_link+'&count=100&offset=100')
        data_off = json.loads(resp_wall_off.text)
        arr_posts.append(data_off)
    for one_set in arr_posts:
        for post in range(1, len(one_set['response'])):
            post_id = data['response'][post]['id']
            count = data['response'][post]['comments']['count']
            command_post = comment_link+'&post_id='+str(post_id)+'&count=100&v=5.52'
            command_post_off = command_post+'&offset=100'
            if count <= 100:
                #command_post = comment_link+'&post_id='+str(post_id)+'&count=100&v=5.52'
                poster = json.loads(requests.get(command_post).text)
                arr_comments.append(poster)
            else:
                count = count - 100
                if count <= 100:
                    #command_post_off = comment_link+'&post_id='+str(post_id)+'&count=100&v=5.52&offset=100'
                    poster = json.loads(requests.get(command_post_off).text)
                    arr_comments.append(poster)
                else:
                    rng = int(count/100)+1
                    for roun in range(1, rng):
                        #command_post = group_link+'&post_id='+str(post_id)+'&count=100&v=5.52&offset=100'
                        poster = json.loads(requests.get(command_post_off).text)
                        arr_comments.append(poster)
    for cmmnt in arr_comments:
        for pers in range(1,len(cmmnt['response']['items'])):
            if cmmnt['response']['items'][pers]['from_id'] in ids:
                ids[cmmnt['response']['items'][pers]['from_id']] += 1
            else:
                ids[cmmnt['response']['items'][pers]['from_id']] = 1
    leaders = []
    names = []
    for one in sorted(ids, key=lambda n: ids[n], reverse=True)[:10]:
        leaders.append(one)
    for page in leaders:
        command = 'https://api.vk.com/method/users.get?user_id='+str(page)+'&fields=first_name,last_name&v=5.52'
        req = json.loads(requests.get(command).text)
        stri = req['response'][0]['first_name']+' '+req['response'][0]['last_name']
        names.append(stri)
    return names

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


m = Mystem()
app = Flask(__name__)

@app.route('/groupleaders', methods=['get', 'post'])
def commentaries():
    if request.form:
        group_id = request.form['group_id']
        comm_lead = leaders(group_id)
        return render_template('vkgroups.html', group_id=group_id, result=comm_lead)
    return render_template('vkgroups.html')


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


if __name__ == '__main__':
    app.run()
