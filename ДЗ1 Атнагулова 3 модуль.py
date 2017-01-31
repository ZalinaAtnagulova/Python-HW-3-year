import re
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

    def fio(self, data):
        one_pers = data
        whole_name = re.search('<div class="g-pic person-avatar-small2" title="(.*?)"',
                               one_pers, flags = re.DOTALL)
        if whole_name.group(1) != None:
            name_elements = re.split('[^\\w]+', whole_name.group(1))
            prof.name = name_elements[1]
            prof.surname = name_elements[0]
            if len(name_elements) == 3:
                self.fname = name_elements[2]

    def mobiles(self, data):
        one_pers = data
        all_mobiles = re.findall('<div class="l-extra small">(.*?)<br/>',
                            one_pers, flags = re.DOTALL)
        for one in all_mobiles:
            mobile = re.findall('<span>(.*?)</span>', one)
            self.mobile = mobile

    def emails(self, data):
        one_pers = data
        all_emails = re.findall('<a class="link" data-at=\'\[(.*?)\]\'></a>',
                                one_pers, flags = re.DOTALL)
        for one in all_emails:
            email = ''
            email_elem = re.findall('"(.*?)"', one)
            for elem in email_elem:
                email += elem
            email = re.sub('-at-', '@', email)
            self.email.append(email)
    def positions_departments_units(self, data):
        one_pers = data
        all_pos = re.search('<p class="with-indent7">(.*?)</p>',
                            one_pers, flags = re.DOTALL)
        if all_pos.group(1) != None:
            pose = re.findall('<span>.*?([а-яёА-ЯЁ, -]+):.*?</span>',
                              all_pos.group(1), flags = re.DOTALL)
            prof.position = pose
        depts = re.findall('<a class="link" href=.*?">([а-яёА-ЯЁ, -]+)</a>',
                           all_pos.group(1), flags = re.DOTALL)
        if len(depts) > 1:
            self.dep = depts[0]
            self.unit = depts[0:]
        else:
            self.dep = depts

    def interest(self, data):
        one_pers = data
        all_interests = re.search('<div class="with-indent small">(.*?)</div>?',
                                  one_pers, flags = re.DOTALL)
        if all_interests != None:
            interests = re.findall('">([0-9а-яёА-ЯЁ. ()-]+)',
                                   all_interests.group(1), flags = re.DOTALL)
            self.interests = interests

f = open('persons.htm', 'r', encoding = 'utf-8')
all_prof = f.read()
f.close()
prof_arr = []
a1 = re.findall('<div class="post person">(.*?)\n</div>',
                all_prof, flags = re.DOTALL)
if a1 != None:
    for one_pers in a1:
        prof = Prof()
        prof.fio(one_pers)
        prof.mobiles(one_pers)
        prof.emails(one_pers)
        prof.positions_departments_units(one_pers)
        prof.interest(one_pers)
        prof_arr.append(prof)
for c in prof_arr:
    print(c.surname)
    print(c.name)
    print(c.fname)
    print(c.mobile)
    print(c.email)
    print(c.position)
    print(c.dep)
    print(c.unit)
    print(c.interests)
