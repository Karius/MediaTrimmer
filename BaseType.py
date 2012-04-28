#! /usr/bin/env python
# -*- coding: utf-8 -*-


##################################################
# 数据列表类型基本类
class BaseDataList(object):
    def __init__ (self):
        self.__DataList = []

    # 返回内部 List
    def List (self):
        return self.__DataList

    # 返回内部 List 的一个副本
    def ListCopy (self):
        return self.__DataList[:]

    # 删除所有元素
    def Clear (self):
        del self.List ()[:]

    # 列表长度
    def Size (self):
        return len (self.List ())

    # 根据索引访问指定元素
    def Element (self, index):
        return self.List ()[index]

    # 运算符重载：根据索引访问指定元素
    def __getitem__ (self, index):
        return self.List ()[index]

    # 运算符重载：根据索引设置指定元素
    def __setitem__ (self, index, item):
        self.List ()[index] = item

    def __delitem__ (self, index):
        del self.List ()[index]

    # 运算符重载：返回 List 容量
    def __len__ (self):
        return len (self.List ())

    def __contains__ (self, val):
        return val in self.List ()

    def __iter__ (self):
        return self.List ().__iter__ ()

    def __next__ (self):
        return self.List ().__next__ ()

    # 在数据列表末尾增加一个元素
    def Append (self, item):
        self.List ().append (item)

    # 在指定位置插入一个元素
    def Insert (self, pos, item):
        self.List ().insert (pos, item)

    # 从数据列表删除一个指定位置的元素
    def Del (self, pos):
        del self.List ()[pos]

    # 排序数据列表
    def Sort (self):
        self.List ().sort ()

    # 反转列表内容
    def Reverse (self):
        self.List ().reverse ()

    # 打乱列表顺序
    def Shuffle (self):
        import random
        random.shuffle (self.List ())



##################################################
# 数据词典类型基本类
class BaseDataDict(object):
    def __init__ (self):
        self.__DataDict = {}

    # 返回内部 Dict
    def Dict (self):
        return self.__DataDict

    # 返回内部 Dict 的一个副本
    def DictCopy (self):
        return self.__DataDict.items ()

    # 删除所有元素
    def Clear (self):
        self.Dict ().clear ()

    # 词典长度
    def Size (self):
        return len (self.Dict ())

    # 根据 Key 访问指定元素
    def Value (self, key):
        return self.Dict ()[key]

    # 运算符重载：根据索引访问指定元素
    def __getitem__ (self, key):
        return self.Dict ()[key]

    # 运算符重载：根据索引设置指定元素
    def __setitem__ (self, key, val):
        self.Dict ()[key] = val

    def __delitem__ (self, key):
        del self.Dict ()[key]

    # 运算符重载：返回 Dict 容量
    def __len__ (self):
        return self.Size ()

    def __contains__ (self, key):
        return key in self.Dict ()

    def __iter__ (self):
        return self.Dict ().__iter__ ()

    def __next__ (self):
        return self.Dict ().__next__ ()

    # 在数据词典增加一个元素
    def Add (self, key, val):
        self.Dict ()[key] = val


    # 从数据词典删除一个的元素
    def Del (self, key):
        del self.Dict ()[key]

    # 排序数据词典
    def Sort (self):
        self.Dict ().sort ()

    # 反转词典内容
    def Reverse (self):
        self.Dict ().reverse ()

    # 打乱词典顺序
    def Shuffle (self):
        import random
        random.shuffle (self.Dict ())

