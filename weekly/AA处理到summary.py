import os
import re
from datetime import datetime

# 设定要搜索的目录
directory = './'

# 输出文件
output_file = 'summary.txt'

# 匹配 YAML 头部中的 date 和 title
pattern = r'---\ntitle: (.+)\ncover: .+\ncategories: .+\ntags: .+\ndate: (\d{4}/\d{2}/\d{2}) .+\n---'

# 存储提取的信息
extracted_info = []

# 遍历目录下的所有文件
for filename in os.listdir(directory):
    if filename.endswith('.md'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            match = re.search(pattern, content)
            if match:
                # 提取date和title
                title = match.group(1)
                date = match.group(2)
                # 期刊序号
                journal_number = filename.split('.')[0]
                # 将日期字符串转换为datetime对象
                date_obj = datetime.strptime(date, '%Y/%m/%d')
                # 将提取的信息添加到列表中
                extracted_info.append((date_obj, title, journal_number))
# 按日期倒序排序
extracted_info.sort(reverse=True, key=lambda x: x[0])

# 将提取的信息写入到summary.txt文件中
with open('summary.txt', 'w', encoding='utf-8') as summary_file:
    for date_obj, title, journal_number in extracted_info:
        # 格式化日期
        formatted_date = date_obj.strftime('%m/%d')
        summary_file.write(f"- {formatted_date} [{title}](https://www.wmyskxz.cn/weekly/{journal_number})\n")

print(f'Done! Extracted information is written to {output_file}.')
