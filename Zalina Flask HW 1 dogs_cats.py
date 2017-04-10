from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)  

@app.route('/')
def main():
    love = True
    return render_template('main.html')

@app.route('/result')
def result():
    if request.args:
        all_users = {}
        dictr = {'за собак':0, 'за кошек':0}
        f = open('stat.txt', 'r', encoding='utf-8')
        text = f.read()
        f.close()
        if len(text) != 0:
            text = text.split('\n\n')
            users = text[0]
            users = users.split('\n')
            for a in users:
                a = a.split('\t')
                all_users[a[0]] = int(a[1])
            animals = text[1]
            animals = animals.split('\n')
            for b in animals:
                b = b.split('\t')
                if b[0] == 'за собак':
                    dictr['за собак'] = int(b[1])
                if b[0] == 'за кошек':
                    dictr['за кошек'] = int(b[1])
            user = request.args['name']
            if user not in all_users:
                all_users[user] = 1
            else:
                all_users[user] += 1
            if 'dog' in request.args:
                love = True
                dictr['за собак'] += 1
            else:
                love = False
                dictr['за кошек'] += 1
            f = open('stat.txt', 'w', encoding='utf-8')
            for one_usr in all_users:
                f.write(one_usr+'\t'+str(all_users[one_usr])+'\n')
            f.write('\n')
            for anim in dictr:
                f.write(anim+'\t'+str(dictr[anim])+'\n')
            f.close()
        else:
            f = open('stat.txt', 'w', encoding='utf-8')
            user = request.args['name']
            if user not in all_users:
                all_users[user] = 1
            else:
                all_users[user] += 1
            if 'dog' in request.args:
                love = True
                dictr['за собак'] += 1
            else:
                love = False
                dictr['за кошек'] += 1
            for one_usr in all_users:
                f.write(one_usr+'\t'+str(all_users[one_usr])+'\n')
            f.write('\n')
            for anim in dictr:
                f.write(anim+'\t'+str(dictr[anim])+'\n')
            f.close()
        return render_template('result.html', name=user, animal=love,
                               all_users=all_users, dictr=dictr)
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run()
