from lxml import etree
import re
import requests
from lxml import etree
from lxml import html

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

    def teachers_with_etree(root):
        for el in root:
            print(el.tag)
        #<div class="post person">
    def teachers_with_xpath():
        print()
f = open('persons.htm', 'r', encoding = 'utf-8')
all_prof = f.read()
f.close()
root = etree.HTML(all_prof)
for el in root:
    print(root.xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div/div[3]/div[2]/div[1]'))
