"""
单词表生成器
版本：5
作者: Ki Seki
修改日志：
2020/03/23 - 修改getDetails()函数中因为html解析出现的错误
2020/04/02 - 向Excel表格中加入表头；优化命令行界面输出效果；增加汉化版，即版本4
2020/12/05 - 利用面向对象的方法重新构造
2021/08/26 - 重构 xlsx 文件生成函数
"""


from Craworder import Craworder


crd = None
input_code = input("Input words (1 for manually, 2 for automatically): ")
if input_code == '1':
    print("Please input words: ")
    crd = Craworder()
elif input_code == '2':
    filename = input("Input the filename (nothing for e.txt): ")
    crd = Craworder('e.txt') if filename == '' else Craworder(filename)
print("Crawling...")
crd.crawl_words()

print("These are results: ")
print(crd)

filename = input("Input CSV or EXCEL filename to save results (Nothing for Vocabulary(yyyy-mm-dd).xlsx): ")
while not (filename.endswith(".csv") or filename.endswith(".xlsx") or filename == ""):
    print("FILENAME should end with either .csv or .xlsx")
    filename = input("Please input correct filename: ")

if filename:
    if filename.endswith(".csv"):
        crd.save_words_to_csv(filename)
    else:
        crd.save_words_to_xlsx(filename)
else:
    import datetime
    date = datetime.date.isoformat(datetime.date.today())
    filename = f"Vocabulary({date}).xlsx"
    crd.save_words_to_xlsx(filename)
print("File saved.")

input("Press Enter to exit")
