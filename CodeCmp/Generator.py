import random

data = ['''2
5 6
abcde
a b 3
a c 2
b d 5
c d 7
c e 4
d e 6
4 5
abcd
a b 2
a c 3
a d 4
b d 1
c d 3
''',
        '''1
5 6
abcde
a b 3
a c 2
b d 5
c d 6
c e 4
d e 6
''']


def test_case_generator():
    for i in data:
        yield i
