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


class Result:
    # 构造函数
    # boolVal: bool 类型，指定结果值
    # attrList: dict 类型，可以附加多个数据结果
    # attrVal: 指定数据结果词典中的值是否可以被修改
    def __init__ (self, boolVal, attrList = None, attrVal = None):
        # 如果 boolVal 参数非 bool 类型，则抛出异常。否则将其值赋给类的私有成员
        if not isinstance (boolVal, bool):
            raise TypeError, boolVal
        self.__BoolValue = boolVal

        # 如果 attrList 参数非词典类型，则将其置为空词典
        if not isinstance (attrList, dict):
            attrList = {}

        # 如果 attrVal 参数为被设置或者其类型非 bool 类型，则将其值设为 False
        if attrVal is None or not isinstance (attrVal, bool):
            attrVal = False

        self.__EnableSetAttrValue = True # 暂时允许设置属性值

        for k, v in attrList.items ():
            self.__setattr__ (k, v)
        self.__EnableSetAttrValue = attrVal # 根据用户设置去允许或禁止修改属性值

    # 本类对象实例用于条件判断时该函数将被调用
    def __nonzero__ (self):
        return self.__BoolValue

    # 是否为内部属性
    def __isPrivateAttr (self, key):
        if key[1:].find ('_') >= 0:
            return True
        return False

    def __getAttrName (self, key):
        #if key[1:].find ('_') >= 0:
        if self.__isPrivateAttr (key):
            return key

        return key.lower ().strip ()
        # if tkey not in self.__dict__.keys ():
        #    raise AttributeError, key
        # return tkey
        #print self.__dict__.keys ()
        # for k in self.__dict__.keys ():
        #     print k.lower ().strip ()
        #     if k.lower ().strip () == tkey:
        #         return tkey
        # print tkey
        #raise AttributeError, key

    # def __setattr__ (self, key, value):
    #     #self.__getAttrName (key)
    #     #self.__Items[self.__getAttrName (key)] = value
    #     tkey = key.lower ().strip ()
    #     try:
    #         self.__Items[tkey] = value
    #     except:
    #         pass

    def __setattr__ (self, key, value):
        if not self.__isPrivateAttr (key) and not self.__EnableSetAttrValue: # 如果禁止修改属性值并且不是私有属性则返回
            return
        tkey = self.__getAttrName (key)
        d = self.__dict__
        d[tkey] = value

    def __getattr__ (self, key):
        tkey = self.__getAttrName (key)
        if tkey not in self.__dict__:
            raise KeyError, tkey
        return self.__dict__[tkey]

    def __repr__ (self):
        return self.__str__ ()

    def __contains__ (self, key):
        key = self.__getAttrName (key)
        return key in self.__dict__.keys ()

    def __eq__ (self, other):
        if isinstance (other, bool):
            self.__BoolValue = other
        elif isinstance (other, KXResult):
            self.__BoolValue = other.__BoolValue
        else:
            raise TypeError, other

    # 将本内类数据转为可打印的字符串形式
    def __str__ (self):
        strval = {'result': self.__BoolValue}
        for k in self.__dict__:
            if not self.__isPrivateAttr (k):
                strval [k] = self.__dict__[k]
        return str (strval)
