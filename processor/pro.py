import pandas as pd
import ahocorasick_rs
from ahocorasick_rs import MATCHKIND_LEFTMOST_LONGEST
import time

gaoe_file_path = '../files/gaode_citycode_20210406.xlsx'
# 构造一个计时器
start_time = time.time()

# 读取excel文件, 只读取前name和adcode两列
data_frame = pd.read_excel(gaoe_file_path, usecols=['name', 'adcode'])
data_list = data_frame.to_dict('records')
# 讲data_list转换为字典, key为name, value为adcode, 同时如果name含有市、区、县, 则复制一份去掉市、区、县的数据
data_dict = {}
for item in data_list:
    name = item['name']
    adcode = item['adcode']
    data_dict[name] = adcode
    if len(name) <= 2:
        continue
    if '市' in name:
        data_dict[name.replace('市', '')] = adcode
    if '区' in name:
        data_dict[name.replace('区', '')] = adcode
    if '县' in name:
        data_dict[name.replace('县', '')] = adcode
    if '新区' in name:
        data_dict[name.replace('新区', '')] = adcode
print("读取excel文件耗时: %s" % (time.time() - start_time))
start_time = time.time()
# 创建ac树
ac = ahocorasick_rs.AhoCorasick(list(data_dict.keys()), matchkind=MATCHKIND_LEFTMOST_LONGEST)
# 构造ac树耗时多少毫秒
print("构造ac树耗时: %s" % (time.time() - start_time))


# 根据ac树匹配字符串, 只返回匹配到的第一个结果
def match_first(text):
    results = ac.find_matches_as_strings(text)
    return len(results) > 0 and results[0] or None


if __name__ == '__main__':
    city = match_first('郑州今天天气怎么样')
    print(data_dict.get(city))
