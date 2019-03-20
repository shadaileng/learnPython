# Python3

[toc]

# Python基础

## 数据类型

- 整数: `Python`可以处理任意大小的整数, 当然包括负整数.
    - 一般使用十进制表示, 十六进制需要添加前缀`0x`
- 浮点数: 即小数,因为科学记数法时,小数点的位置是可以变化的,所以成为浮点数
    - 一般用数学写法: `1.2`
    - 科学记数法使用`e`替代`10`,如: `1.23x10^9 = 1.23e9`
- 字符串: 使用`'`或者`"`括起来的文本,`'`和`"`是表达方式,不是字符串的一部分
    - `'`和`"`也是,嵌套使用,可以在字符串中显示该字符,如: 
    ```
    "I'm OK"
    ```
    - 如果字符串中包含`'`和`"`,则需要转义字符`\`标识,如: 
    ```
    "I'm \"OK\""
    ```
    - 如果字符串中有很多需要转义的字符, 可以在字符串前添加`r`,使字符串内部不转义
    ```
    r'\n\t\r'
    ```
    - 如果需要输入多行字符,使用`'''...'''`将字符括起来
        - 也可以用来作注释,`python`文件中的第一个块字符串就是文档`__doc__`
        ```
        '''
        abc
        def
        '''
        ```
- 布尔值: 布尔值只要两个值表示: `True`和`False`
    - 布尔运算的结果也是布尔值: `3 > 2`, `3 < 2`
    - 布尔值可以使用`and`,`or`和`not`进行布尔运算

- 空值: `Python`中使用`None`表示空值


> `Python`中的除法有两种: `/`和`//`
> 
> `/`的计算结果是浮点数
> 
> `//`的计算结果是整数,取计算结果的整数部分
> 
> `%`取余数


## 变量和常量

- 变量: `Python`是动态语言,变量不需要定义,可以直接赋值: `a = 7`
    - 变量赋值时,实质是将变量指向,内存中的数据
- 常量: `Python`中一般以大写字母表示常量,实质还是变量: `PI = 3.14159`

## 字符编码和字符串格式化

### 字符编码

- `python3`中,字符串是以`Unicode`编码的,所以`Python`的字符串支持多语言
- `ord()`函数可以取得单个字符的整数表示: 
```
>>> ord('A')
65
```
- `chr()`函数可以将字符编码转换成对应字符: 
```
>>> chr(65)
'A'
```
- 将字符串转换成`bytes`: 
    - 在字符串前添加`b`: 
    ```
    >>> b'ABC'
    b'ABC'
    ```
    - 使用`encode`方法,以指定的编码转换,如果字符编码超出指定编码范围,则会抛出异常: 
    ```
    >>> 'ABC'.encode('ascii')
    b'ABC'
    >>> '中文'.encode('utf-8')
    b'\xe4\xb8\xad\xe6\x96\x87'
    # 中文字符编码超出ascii编码范围,抛出异常
    >>> '中文'.encode('ascii') 
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)
    ```
- 将`bytes`转换成字符串: 使用`decode`方法以指定编码解码字节
```
>>> b'ABC'.decode('ascii')
'ABC'
>>> b'\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8')
'中文'
# 如果bytes中包含小部分无效字节,使用errors='ignore'忽略
>>> b'\xe4\xb8\xad\xff'.decode('utf-8', errors='ignore')
'中文'
```
- `len`方法可以计算`str`的字符长度和`bytes`的字节长度
```
>>> len('ABC')
3
>>> len('中文')
2
>>> len(b'ABC')
3
>>> len(b'\xe4\xb8\xad\xe6\x96\x87')
6
>>> len('中文'.encode('utf-8'))
6
```
- `Python`源代码中可以指定编码格式

```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
```

### 字符串格式化
- `%`分隔符
    - 字符串中使用`%`前缀的占位符,字符串与赋值变量直接以`%`分隔,赋值变量如果有多个需要用括号括起来
    ```
    >>> 'Hello, I\'m %s, I\'m %d years old' % ('shadaileng', 26)
    'Hello, I\'m Shadaileng, I\'m 26 years old'
    ```
    - 常见占位符

占位符 | 替换内容
---|---
%d | 整数
%f | 浮点数
%s | 字符串
%x | 十六进制整数

- `format()`
    - 传入的参数依次替换字符串内的占位符`{0}`、`{1}`
    ```
    >>> 'Hello, {0}, 成绩提升了 {1:.1f}%'.format('小明', 17.125)
    'Hello, 小明, 成绩提升了 17.1%'
    ```
## list和tuple

### list

- `list`是一种有序的集合，可以随时添加和删除其中的元素,元素类型可以不同
```
>>> l = ['A', 'B', 'C']
```

- `len()`函数可以获得`list`元素个数
```
>>> len(l)
3
```

- 使用索引访问`list`中的元素,索引从`0`开始,越界会抛出异常
```
>>> l[0]
'A'
>>> l[3]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: list index out of range
```

- 索引是负数,从尾部开始访问`list`,最后一个元素索引是`-1`
```
>>> l[-1]
'C'
```

- `append`方法在`list`末尾追加元素,`insert`方法在指定位置插入元素
```
>>> l.append('D')
>>> l
['A', 'B', 'C', 'D']
>>> l.insert(1, 'A-')
>>> l
['A', 'A-', 'B', 'C', 'D']
```

- `pop`方法删除并返回`list`中指定的元素,不指定参数,默认删除最后一个元素
```
>>> l.pop()
'D'
>>> l
['A', 'A-', 'B', 'C']
>>> l.pop(1)
'A-'
>>> l
['A', 'B', 'C']
```
- 替换元素只要将新的值赋值给指定位置, 实质是将该位置元素指向一个新的内存空间
```
>>> l[2] = 'D'
>>> l
['A', 'B', 'D']
```
- `list`中可以添加不同类型元素,甚至`list`也可以作为元素,类似二维数组
```
>>> L = ['A', True, 123, [1, 2, 3]]
```

### tuple

- `tuple`称为元祖,和`list`一样是有序集合,不同的是`tuple`内的元素不可更改
```
>>> t = (1,)
>>> t
(1,)
>>> t = (1, 2)
>>> t
(1, 2)
```

## 条件判断和循环

### 条件判断

- 基本格式
```
if 条件:
    pass
```

### 循环

- 基本格式有两种: 
    - `for ... in`
    ```
    for x in [1, 2, 3]:
        print(x)
    ```
    - `while`
    ```
    n = 10
    while n > 0:
        print(n)
        n = n - 1
    ```
 - `break`: 跳出循环
 - `continue`: 跳过当前循环

## dict和set

### dict

- `dict`全称`dictionary`,其他语言中称为`map`,使用键值对存储,提高查找效率
- `dict`的`key`必须是不可变对象,通过`key`计算位置的算法称为哈希算法(`Hash`),为了保证`hash`的正确性，作为`key`的对象就不能变
```
>>> d = {'A': 1, 'B', 'C': 3}
```

- 键值对存储方式, 在添加元素时`key`算出`value`的存放位置, 获取元素时`key`直接拿到`value`
- `key`是唯一的,多次以相同的`key`存入数据,会覆盖`key`原来对应的数据
```
>>> d['D'] = 4
>>> d['D']
4
>>> d['D'] = 5
>>> d['D']
5
```

- 如果`key`不存在,会抛出异常
- 可以使用`in`判断`key`是否存在
- 使用`get`方法获取数据,`key`不存在会返回`None`或者指定默认值
```
>>> d['E']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'E'
>>> 'E' in d
false
>>> d.get('E')
None
>>> d.get('E', -1)
-1
```

- `dict`内部存放的顺序和`key`放入的顺序是没有关系的,`dict`是无序的
- 和`list`比较,`dict`查找和插入数据的速度较快,不会因为数据增多而变慢,但占用内存较大;`list`查找和插入数据会因为数据增加而变慢,但占用内存较小

### set

- `set`是一组`key`的集合,但不存储`value`,
- `set`中没有重复元素,定义是重复元素会被自动过滤
- `set`也是无序的
```
>>> s = set([1, 2, 3, 2])
>>> s
{1, 2, 3}
```

- `add`方法添加元素,添加已有的数据不会有效果
```
>>> s.add(4)
>>> s
{1, 2, 3, 4}
>>> s.add(4)
>>> s
{1, 2, 3, 4}
```

- `remove`方法删除元素
```
>>> s.remove(4)
>>> s
{1, 2, 3}
```

- `set`可以取交易和并集
```
>>> s1 = set([1, 2, 3])
>>> s2 = set([2, 3, 4])
>>> s1 & s2
{2, 3}
>>> s1 | s2
{1, 2, 3, 4}
```

## 函数

### 函数定义

- 基本格式:
```
def 函数名(参数列表):
    pass
```

- 如果函数中没有`return`,默认`return None`
- 函数可以返回多个值,返回值实质是一个`tuple`

### 函数的参数

- 位置参数: 最基本的参数,调用函数是必输,多个参数按顺序赋值
```
def pow(x):
    return x * x
>>> pow(5)
25
```

- 默认参数: 必须在位置参数之后,参数有默认值,调用时可以不填;默认参数必须指向不变对象！
    - 如果默认参数值时可变对象,如: `list`, 则该参数指向的内存空间在定义函数时已经创建,使用默认参数调用函数,操作的都是相同内存空间
    ```
    def pow(x, n = 2):
        p = 1
        while n > 0:
            n = n - 1
            p = p * x
        return p
    >>> pow(5)
    25
    >>> pow(5, 3)
    125
    >>> pow(5, n = 4)
    625

    def appEl(list=[]):
        list.append('E')
        return list
    >>> appEl()
    ['E']
    >>> appEl()
    ['E', 'E']
    ```
- 可变参数: 定义函数时,在参数前加一个`*`,则该参数被定义为可变参数,调用函数时,函数内接收的是一个`tuple`
```
def sum(*num):
    s = 0
    for x in num:
        sum = sum + x
    return sum
>>> sum(1, 2, 3)
6
>>> num = [1, 2, 3]
>>> sum(*num)
6
>>> num = (1, 2, 3)
>>> sum(*num)
6
```

- 关键字参数: 定义函数时, 在参数前加一个`**`,则该参数被定义为关键字参数,调用函数时,函数内接收的一个`dict`
```
def person(name, age, **kw):
    print('name:', name, 'age:', age, 'kw:', kw)
>>> person('Shadaileng', 26)
'name: Shadaileng age: 26 kw: {}'
>>> person('Shadaileng', 26, gender='M', city='GZ')
name: Shadaileng age: 26 kw: {'city': 'GZ', 'gender': 'M'}
>>> extra = {'city': 'GZ', 'gender': 'M'}
>>> person('Shadaileng', 26, **extra)
name: Shadaileng age: 26 kw: {'city': 'GZ', 'gender': 'M'}
```

- 命名关键字参数: 定义函数时, `*`后面的参数就是命名关键字参数,调用函数时,必须根据参数名进行赋值
    - 命名关键字参数必须传入参数名，这和位置参数不同。如果没有传入参数名，调用将报错
    - 命名关键字参数可以有缺省值，从而简化调用
    - 如果参数列表中有可变参数,定义命名关键字参数时,不需要使用`*`分隔
```
def person(name, age, *, gender, city):
    print('name:', name, 'age:', age, 'gender:', gender, 'city: ', city)
>>> person('Shadaileng', 26, city='GZ', gender='M')
name: Shadaileng age: 26 gender: 'M' city: 'GZ'
############################################################
def person(name, age, *, gender, city='GZ'):
    print('name:', name, 'age:', age, 'gender:', gender, 'city: ', city)
>>> person('Shadaileng', 26, gender='M')
name: Shadaileng age: 26 gender: 'M' city: 'GZ'
############################################################
def person(name, age, *arg, gender, city='GZ'):
    print('name:', name, 'age:', age, 'gender:', gender, 'city: ', city, 'arg:', arg)
>>> person('Shadaileng', 26, gender='M')
name: Shadaileng age: 26 gender: 'M' city: 'GZ', arg: ()
```

- 参数组合: 参数定义的顺序必须是：必选参数、默认参数、可变参数、命名关键字参数和关键字参数

# 高级特性

## 切片

- 格式: `L[begin:end:step]`: 截取`begin`开始到`end`,不包含`end`,每`step`个元素取第一个
- 用于截取`list`,`tuple`,`str`等可迭代对象
```
>>> L = [1, 2, 3, 4, 5]
>>> L[1, 3]
[2, 3]
>>> L[::2]
[1, 3, 5]
```

## 迭代

- 判断对象是否可迭代
```
>>> from collections import Iterable
>>> isinstance('abc', Iterable) # str是否可迭代
True
>>> isinstance([1,2,3], Iterable) # list是否可迭代
True
>>> isinstance(123, Iterable) # 整数是否可迭代
False
```

- `dict`的`key`,`value`和键值对(`items`)都是可迭代的
```
>>> isinstance(d, Iterable) # 遍历key
True
>>> isinstance(d.values(), Iterable) # 遍历value
True
>>> isinstance(d.items(), Iterable) # 遍历key, value
True
```

## 列表生成式

- 列表生成式即`List Comprehensions`, 是`Python`内置的非常简单却强大的可以用来创建`list`的生成式
```
>>> list(range(1, 11))
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

- 列表生成式可以用一行代码遍历计算并生成`list`
```
>>> [x * x for x in range(1, 11)]
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

- 遍历后面还可以判断
```
>>> [x * x for x in range(1, 11) if x % 2 == 0]
[4, 16, 36, 64, 100]
```

- 还可以嵌套遍历
```
>>> [m + n for m in 'ABC' for n in 'XYZ']
['AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ']
```

# IO编程

IO在计算机中指的是`Input/Output`。在程序和运行时数据在内存中驻留，程序由`CPU`执行和处理数据。内存与外设通过`IO接口`进行数据交换，从外设到内存为输入，内存到外设为输出。输入输出是以数据流(`Stream`)的形式进行数据交换。由于`CPU`和内存速度远高于外设的速度，所以文件输入输出有两种处理方法：

- 同步模式: `CPU`等待`IO`处理完再执行后续的程序;
- 异步模式: `CPU`不等待，继续执行后续程序，`IO`处理完成通知`CPU`;

## 文件读写

读写文件的功能都是系统提供的，`Python`读写文件都是调用系统读写文件的`API`。

### 打开文件

读写文件之前要先打开文件：

```
file = open(filename, mod)
```
`filename`是文件的路径，`mod`是读写文件的模式：`'r'`,`'w'`,`'rb'`,`'wb'`.如果文件不存在，会跑出`IOError`错误。
例：

```
file = open(__file__, 'r') //以读的模式打开当前文件
```

### 读取文件

打开的文件调用`read()`方法，返回文件里的内容。
```
content = file.read()
```
如果文件太大，一次性读取文件会是内存溢出，使用`read(size)`方法会返回`size`个字节的内容: