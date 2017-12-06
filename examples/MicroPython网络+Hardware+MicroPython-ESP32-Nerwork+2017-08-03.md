---
title: microPython高级应用
layout: page
category: wiki
---
## 内部文件系统
microPython支持标准的Python的文件模块，可以使用`open()`这类原生函数。

> 需要注意的是esp32上实时资源少，需要及时关闭掉一些file、socket。

### 创建一个文件

```python
>>> f = open('data.txt', 'w')
>>> f.write('some data')
9
>>> f.close()
```

其中这个9是指write()函数写进去的字节数

### 查看一个文件

```python
>>> f = open('data.txt')
>>> f.read()
'some data'
>>> f.close()
```

### 文件目录操作

```python
>>> import os   # 引用os模块
>>> os.listdir()    # 查看当前目录下的所有文件
['boot.py', 'port_config.py', 'data.txt']
>>> os.mkdir('dir') # 创建目录
>>> os.remove('data.txt')   # 删除文件
```

## esp启动顺序

首先运行_boot.py这个脚本，把文件系统挂载上，这个部分一般是固定的，不推荐用户来修改，可能会出很多奇怪的问题。

当文件系统挂载成功后，运行boot.py，在这个脚本里面，用户可以设置一些在REPL里面需要使用的变量或者函数，每次重启esp32，这个脚本也会运行一次，但是如果这个地方写错了代码， 比如进入了死循环之类的，你就需要重新刷固件了。

最后系统会从文件系统运行main.py（如果不存在，就不会运行），这个文件就是用来每次启动的时候运行用户程序而不是进入REPL的，对于一些小的脚本，你可以直接写成一个main.py名字的文件，不过也会推荐你把一个大应用分散来写，写成多个小程序，在main.py里面这么写就好了：

```python
import my_app
my_app.main()
```

### 设置开机自启动的脚本

对boot.py和main.py这两个文件进行修改都可以，比如对main.py进行修改：

```python
>>> file = open("main.py", 'w')
>>> file.write("""import time
... for i in range(0,10):
...     time.sleep(1)
...     print(i)""")
64
>>> file.close()
```

通过快捷键`ctrl+D`，软启动esp32，就能看到上面的效果了

```python
>>>
PYB: soft reboot
0
1
2
3
4
5
6
7
8
9
MicroPython v1.9.1-394-g79feb956 on 2017-08-03; ESP32 module with ESP32
Type "help()" for more information.
>>>
```

## 网络socket应用
简单的连接WiFi和设置热点可以看上一篇教程，成功之后就可以考虑TCP socket连接了。

在这里我们可以用socket模块，但其实有更加方便的模块，urequests（u表示这个模块和标准python的模块相比有许多没有方法没有实现）：

```python
import urequests

r = urequests.get('http://www.baidu.com')   # 发起HTTP的GET请求
r.text  # 查看服务器返回的内容
```

urequests实现了主要的几个方法，比如get、post、put、delete这几种请求，在网络方面使用起来非常方便。
