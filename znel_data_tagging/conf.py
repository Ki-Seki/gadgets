# 百度自然语言处理接口
APP_ID = '27992202'
API_KEY = 'FdzxCAhYdMhb6dfvT4PeEw63'
SECRET_KEY = 'iFgZo6a6rLPoLCfx8O3uhA5c10092iOb'

# 接口调用失败时，最大总尝试次数
max_trials = 10

# 候选行业数量
candi = 15

# 标注范围，总计有 10194 个待标注的短句子
# 建议 count ≤ 30，不建议值特别大，因为一旦出错，百度云计算的算力可能就直接浪费了
start = 638  # 从 start 号开始标注
count = 59  # 总共标注 count 个