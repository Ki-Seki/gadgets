"""
Module name: Craworder;
Author: Ki Seki;
Description: get, parse and save words into vocabulary
"""

import requests
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r.text


def parse_detail(word, trans='', root='http://www.youdao.com/w/'):
    url = root + word
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')

    # parse soundmark
    sdmk = ''
    tmp = soup.find_all(name='span', attrs={'class': 'phonetic'})
    if tmp and len(tmp) > 0:
        sdmk = tmp[-1].string.replace(',', '，')  # ensure no ',' in the final csv file

    # parse translation
    tmp = soup.find_all(attrs={'class': 'trans-container'})
    if tmp and len(tmp) > 0:
        tmp = tmp[0].find_all(name='li')
        if tmp and len(tmp) > 0:
            for li in tmp:
                if li.string and trans in li.string:
                    trans = li.string.replace(',', '，')  # ensure no ',' in the final csv file
                    break

    return word, sdmk, trans


def progressbar(curr, total, word, code):
    """

    :param curr: current index of the total words
    :param total: length of all the words
    :param word: current word
    :param code: 0 for ongoing, 1 for succeed, 2 for failed
    :return: nothing but a progress bar
    """
    status = {0: '-', 1: '√', 2: '×'}
    bar_size = 35
    showed = int(curr / total * bar_size)
    not_showed = bar_size - showed
    percentage = int(curr / total * 100)
    print('\r' + ' ' * 119, end='')  # clear a line
    print('\r' + '▇' * showed + '  ' * not_showed + ' {:>3}% | {}({})'.format(percentage, word, status[code]), end='')


class Craworder:
    """
    import words from file or input
    """
    def __init__(self, filename=''):
        """
        :param filename: if assigned, then import from the file
        """
        self.words = []  # var. words contains tuples like ('word', 'soundmark', 'default translation')
        if filename == '':
            self.import_words_from_input()
        else:
            self.import_words_from_file(filename)

    def import_words_from_input(self):
        """
        input format is "words(：default translation)"
        """
        while True:
            word = input()
            if word:
                tmp = word.split('：')
                if len(tmp) == 1:
                    self.words.append((tmp[0], '', ''))
                elif len(tmp) == 2:
                    self.words.append((tmp[0], '', tmp[1]))
            else:  # end by inputting double newline
                break

    def import_words_from_file(self, filename):
        """
        :param filename: txt file exported by Eudic
        """
        with open(filename, encoding='utf-8') as f:
            for line in f.readlines():
                if len(line.split('@')) > 1:
                    self.words.append((line.split('@')[1], '', ''))

    def crawl_words(self):
        """
        crawl all the words; meanwhile, output the progress bar
        """
        length = len(self.words)
        for i in range(length):
            word = self.words[i][0]
            trans = self.words[i][2]

            progressbar(i+1, length, word, 0)
            self.words[i] = parse_detail(word, trans)
            status_code = 1 if (self.words[i][1] != '' and self.words[i] != '') else 2
            progressbar(i+1, length, word, status_code)
        print()  # to start a new line due to progressbar

    def save_words_to_csv(self, filename='vocabulary.csv'):
        with open(filename, 'w', encoding='utf-8') as f:
            for word, sdmk, trans in self.words:
                print(word, sdmk, trans, sep=',', file=f)

    def save_words_to_xlsx(self, filename='vocabulary.xlsx'):
        pass

    def __repr__(self):
        string = ''
        for item in self.words:
            string += f'{item[0]}, {item[1]}, {item[2]}\n'
        return string
