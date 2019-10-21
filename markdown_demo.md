# 示例

# 标题

**粗体**

- 缩进
  - 缩进

行内高亮： `markdown`

按键：CTRL

> 多层引用
> > 多层引用

———— 

> 单层引用
> 单层引用

| 表格 | 表格 |
| -    |  -   |
| 表格 | 表格 |


图片： ![图片](https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1563882144794&di=52eb774da4ec1facb58beba757917fb0&imgtype=0&src=http%3A%2F%2Fb-ssl.duitang.com%2Fuploads%2Fitem%2F201610%2F17%2F20161017085709_n4BPs.gif)



代码高亮：
```python
def dict_recursion(dict_all):
    if isinstance(dict_all, dict):
        for x in dict_all:
            dict_key = x
            dict_value = dict_all[dict_key]
            print("{}:{}".format(dict_key, dict_value))
            dict_recursion(dict_value)
    else:
        return
```

