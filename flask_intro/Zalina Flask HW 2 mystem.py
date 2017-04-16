from flask import Flask
from flask import url_for, render_template, request, redirect
from pymystem3 import Mystem

app = Flask(__name__)

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
            if a['analysis'][0]['gr'][0] == 'V':
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

@app.route('/', methods=['get', 'post'])
def index():
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
