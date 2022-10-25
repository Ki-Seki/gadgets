# 介绍

中南财经政法大学经济学课题组的一个数据标注任务的自动化工具

核心任务就是将 `src.txt` 中每一行匹配到 `dst.txt` 中153个行业中去。

`.\参考`文件夹下有更详细的原始文档

# 使用方法

1. clone this repo
2. cd to this repo
3. run `pip install -r requirements.txt`
4. install Baidu AIP
   1. decompress the `.\参考\aip-python-sdk-4.16.7.zip`
   2. run setup.py to install `AipNlp`
5. edit `conf.py`
6. run `main.py`