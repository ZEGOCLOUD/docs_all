#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append('.scripts/migrate')
from convert import remove_heading_numbers

# 测试用例
test_content = """# 1 主标题
## 2 功能列表
### 4.3 满足多种互动小班场景
#### 1.2.3 详细说明
##### （1）括号序号
###### a) 字母序号

# 一、中文序号
## ① 圆圈数字
### [1] 方括号数字

# 正常标题（无序号）
## 另一个正常标题
"""

print("原内容：")
print(test_content)
print("\n" + "="*50 + "\n")

result = remove_heading_numbers(test_content)
print("处理后：")
print(result)

print("\n" + "="*50 + "\n")
print("测试您提到的具体例子：")
specific_test = """## 2 功能列表
### 4.3 满足多种互动小班场景
"""
print("原内容：")
print(specific_test)
print("处理后：")
print(remove_heading_numbers(specific_test)) 