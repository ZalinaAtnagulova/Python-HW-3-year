import unittest
import doctest
import re

def text_cr(file):
    """Reads text file
       Tiny finction you'd need if you're going to read text from file in several parts of code
    Args:
        file: filename with extention (.txt, .doc, etc)
    Returns:
        the content of the file as a string
    """
    f = open(file, 'r', encoding = 'utf-8-sig')
    text = f.read()
    f.close()
    return text

def kwiq(word, text, num = 3):
    """Find a word and it's context
       The function looks for a word in a text and if the word is present it returns it
       and 3 words before and after it if the other was'nt set
    Args:
        word: a word you look for in text
        text: a text you look for the word in
        num: optionally, a length of a context on each side of the word, 3 by default
    Returns:
        a list of text pieces, containing word and context     
    """
    arr = []
    dic = {}
    key = 0
    textspl = text.split()
    for part in textspl:
        dic[key] = part
        key += 1
    for q in list(dic.keys()):
        new_elem = dic[q].strip(',.?!:;')
        if new_elem == word or new_elem.lower() == word:
            string = ''
            for b in range(q-num, q+num+1):
                if b in dic:
                    if b == q-1 or b == q:
                        string += dic[b] + ' '
                    else:
                        string += dic[b] + ' '
            arr.append(string)
    return(arr)

class kwiqTestCase(unittest.TestCase):
    def test_dic(self):
        self.assertEqual((['word1 word2 word3 word word5 word6 word7 ']),
                         kwiq('word', 'word1 word2 word3 word word5 word6 word7'))

if __name__ == "__main__":
    unittest.main()
def print_table(table):
    col_width = [max(len(x) for x in col) for col in zip(*table)]
    for line in table:
        print ("| " + " | ".join("{:{}}".format(x, col_width[i])
                                for i, x in enumerate(line)) + " |")

text = text_cr('text.txt')
arr = kwiq('Eragon', text)
arr1 = []
kwiq('Eragon', text, num = 4)
print(kwiq.__doc__)
doctest.testmod()
