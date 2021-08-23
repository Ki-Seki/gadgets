"""
单词表生成器
版本：5
作者: Ki Seki
修改日志：
2020/03/23 - 修改getDetails()函数中因为html解析出现的错误
2020/04/02 - 向Excel表格中加入表头；优化命令行界面输出效果；增加汉化版，即版本4
2020/12/05 - 利用面向对象的方法重新构造
"""

from Craworder import Craworder


crd = None
input_code = input("Input words (1 for manually, 2 for automatically): ")
if input_code == '1':
    print("Please input words: ")
    crd = Craworder()
elif input_code == '2':
    filename = input("Input the filename (nothing for e.txt): ")
    if filename == '':
        crd = Craworder('e.txt')
    else:
        crd = Craworder(filename)

print("Crawling...")
crd.crawl_words()

print("These are results: ")
print(crd)

filename = input("Input csv file name to save results (Nothing for vocabulary.csv): ")
if filename:
    crd.save_words_to_csv(filename)
else:
    crd.save_words_to_csv()
print("File saved.")

input("Press Enter to exit")
