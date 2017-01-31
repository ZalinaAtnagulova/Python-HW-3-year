from lxml import etree
from lxml import html
import requests

class Prof(object):
    def __init__(self):
        self.name = ''
        self.surname = ''
        self.fname = ''
        self.mobile = []
        self.email = []
        self.position = []
        self.dep = []
        self.unit = []
        self.interests = []

    def teachers_with_etree(self, a):
        self.etree_mobiles(a)
        self.etree_mails(a)
        self.etree_names(a)
        self.etree_positions(a)
        self.etree_departments(a)
        self.etree_unit(a)
        self.etree_intetests(a)
            
    def etree_mobiles(self, a):
        for one_numtag in a[0][0]:
            if one_numtag.tag == 'span':
                self.mobile.append(one_numtag.text)
                
    def etree_mails(self, a):
        for emailtag in a[0][0]:
            if emailtag.tag == 'a':
                mail_letters = emailtag.attrib['data-at']
                mails = mail_letters.replace('"','').replace('[','').replace(']','').replace(',','').replace('-at-','@').replace(' ','')
                self.email.append(mails)

    def etree_names(self, a):
        if len(a[0]) > 1:
            full_name = a[0][1][0][0][0].tail.split()
            if len(full_name) == 3:
                self.name = full_name[1]
                self.surname = full_name[0]
                self.fname = full_name[2]
            if len(full_name) == 2:
                self.name = full_name[1]
                self.sname = full_name[0]
        else:
            full_name = a[0][0][0][0][0].tail.split()
            if len(full_name) == 3:
                self.name = full_name[0]
                self.surname = full_name[1]
                self.fname = full_name[2]
            if len(full_name) == 2:
                self.name = full_name[0]
                self.sname = full_name[1]

    def etree_positions(self, a):
        if len(a[0]) > 1:
            for postag in a[0][1][0][1]:
                if postag.tag == 'span':
                    self.position.append(postag.text.strip().strip(':'))
        else:
            for postag in a[0][0][0][1]:
                if postag.tag == 'span':
                    self.position.append(postag.text.strip().strip(':'))

    def etree_departments(self, a):
        if len(a[0]) > 1:
            for postag in a[0][1][0][1]:
                if postag.tag == 'span' and len(postag) > 0:
                    self.dep.append(postag[0].text.strip())
        else:
            for postag in a[0][0][0][1]:
                if postag.tag == 'span' and len(postag) > 0:
                    self.dep.append(postag[0].text.strip())

    def etree_unit(self, a):
        if len(a[0]) > 1:
            for unittag in a[0][1][0][1]:
                if unittag.tag == 'span' and len(unittag) > 1:
                    self.unit.append(unittag[1].text.strip())
        else:
            for unittag in a[0][0][0][1]:
                if unittag.tag == 'span' and len(unittag) > 1:
                    self.unit.append(unittag[1].text.strip())

    def etree_intetests(self, a):
        if len(a[0]) > 1:
            if len(a[0][1][0]) > 2:
                for interesttag in a[0][1][0][2]:
                    self.interests.append(interesttag.text.strip())
        else:
            if len(a[0][0][0]) > 2:
                for interesttag in a[0][0][0][2]:
                    self.interests.append(interesttag.text.strip())
                    
    def teachers_with_xpath(self, one):
        self.xpath_fio(one)
        self.xpath_mobiles(one)
        self.xpath_emails(one)
        self.xpath_positions_depts_units(one)
        self.xpath_interests(one)

    def xpath_fio(self, one):
        names = one.xpath('./div/div/div/a/text()')
        if len(names) > 0:
            self.name = names[1].split()[1]
            self.surname = names[1].split()[0]
            if len(names[1].split()) == 3:
                self.fname = names[1].split()[2]
                
    def xpath_mobiles(self, one):
        self.mobile = one.xpath('./div/div[1]/span/text()')
        
    def xpath_emails(self, one):
        mail_letters = one.xpath('./div/div[1]/a/@data-at')
        emails_arr = []
        for letters in mail_letters:
            email = ''
            letters = letters.strip('["')
            letters = letters.strip(']"')
            letters = letters.split('","')
            for letter in letters:
                if letter == '-at-':
                    email += '@'
                else:
                    email += letter
            emails_arr.append(email)
        self.email = emails_arr
        
    def xpath_positions_depts_units(self, one):
        self.dep = one.xpath('./div/div/div/p/span/a/text()')
        posit = one.xpath('./div/div/div/p/span/text()')
        lettters_arr = ['й', 'ц', 'у','к','е','н','г','ш','щ','з','х','ъ','ф','ы','в','а','п','р','о','л','д','ж','э','я','ч','с','м','и','т','ь','б','ю']
        if len(posit) > 0:
            for pos in posit:
                if any(letter in pos for letter in lettters_arr):
                    if '/' not in pos:
                        pos = pos.strip().strip(':')
                        self.position.append(pos)
                    else:
                        pos = pos.strip()
                        pos = pos.replace('\t', '').replace('/', '').replace('\n', '')
                        self.dep.append(pos)
                        
    def xpath_interests(self, one):
        self.interests = one.xpath('./div/div[2]/div/div/a/text()')


prof_arr_etree = []
page = requests.get('https://www.hse.ru/org/persons?ltr=%D0%96;udept=22726')
#for etree
root = etree.HTML(page.content)
for a in root[1][1][3][2][1][0][2][1]:
    prof = Prof()
    prof.teachers_with_etree(a)
    prof_arr_etree.append(prof)
#for xpath
prof_arr_xpath = []
tree = html.fromstring(page.content)
persons = tree.xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div/div[3]/div[2]/div')
for one in persons:
    prof = Prof()
    prof.teachers_with_xpath(one)
    prof_arr_xpath.append(prof)
for one_pr in prof_arr_xpath:
    print(one_pr.name)
    print(one_pr.surname)
    print(one_pr.fname)
    print(one_pr.mobile)
    print(one_pr.email)
    print(one_pr.position)
    print(one_pr.dep)
    print(one_pr.unit)
    print(one_pr.interests)
print('\nА теперь то же самое с etree\n')
for one_prof in prof_arr_etree:
    print(one_prof.name)
    print(one_prof.surname)
    print(one_prof.fname)
    print(one_prof.mobile)
    print(one_prof.email)
    print(one_prof.position)
    print(one_prof.dep)
    print(one_prof.unit)
    print(one_prof.interests)
