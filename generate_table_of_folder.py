# Helped by ChatGPT, with the prompt being
# "  请帮我写一个Python函数，这个程序能够自动生成特定文件夹中所有文件或文件夹的目录，这个目录的每一行就是一个文件或者文件夹，第一列是文件（夹）的名称，第二列是说明。并且注意这个目录是Markdown表格格式的；不递归遍历深层文件或文件夹，仅第一层的；名称列要求是可点击的链接；函数第一个参数是特定文件夹的路径；函数接受一个列数量参数，可以自行指定列的数量，但不能小于2；接收一个ignore字符串，其每一行都是一个要忽略的文件或文件夹，忽略其中指明的文件；为所有参数加上默认值"

def generate_table(path='.', num_columns=2, ignore_str='.git\n.gitignore\nLICENSE\nREADME.md'):
    if num_columns < 2:
        raise ValueError('Number of columns must be greater than or equal to 2.')
    import os
    # 获取指定文件夹中的所有文件和文件夹
    files = os.listdir(path)
    # 读取ignore字符串，获取要忽略的文件
    ignore_files = [line.strip() for line in ignore_str.split('\n')]
    # 初始化Markdown表格
    table = '|Name'
    for i in range(2, num_columns + 1):
        table += '|Column {}'.format(i)
    table += '|\n|---'
    for i in range(2, num_columns + 1):
        table += '|---'
    table += '|\n'
    # 遍历文件和文件夹，添加到表格中
    for file in files:
        # 如果文件在ignore字符串中，则跳过
        if file in ignore_files:
            continue
        table += '|[{}]({})'.format(file, os.path.join(path, file))
        for i in range(2, num_columns + 1):
            table += '| |'
        table += '\n'
    # 输出表格
    print(table)

if __name__ == '__main__':
    generate_table()