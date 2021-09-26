# 太极图形课S1-ODOP示例程序-Galaxy
## 背景简介
本文实现了一个简单的星系系统（Galaxy），其中包含基类星体（CelestialObject），和两个子类恒星（Star）和行星（Planets）。为了简化计算，行星对恒星的引力被忽略不计。

## 成功效果展示
![fractal demo](./data/galaxy.gif)
## 整体结构（Optional）
```
├── data
│   └── galaxy.gif
├── requirements.txt
├── LICENSE
├── README.md
├── celestial_objects.py
└── galaxy.py
```

## 运行方式
运行环境：

```
[Taichi] version 0.8.0, llvm 10.0.0, commit 181c9039, win, python 3.8.10
```

确保`celestial_objects.py` 和`galaxy.py` 在相同的路径下

直接运行:  `python3 galaxy.py`

按键

- `Space` : 暂停/继续
- `r` : 重置
