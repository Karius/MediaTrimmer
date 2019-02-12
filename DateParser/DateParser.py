# -*- coding: utf-8 -*-

import fnmatch

# 解析器管理器
class DateParseManager (object):

    __parserList = {}
    __parserPriorityList = {}

    def __init__ (self):
        pass
 
    """注册一个日期提取器
    name: 提取器的名称
    parser: 提取器的实例
    """
    @staticmethod
    def RegisterParser (name, parser):
        if not isinstance (parser, DateParser):
        #if not issubclass (parser, DateParser)
            raise TypeError ("%s not is DateParser!" % (parser))

        DateParseManager.__parserList[name] = parser
    
    """返回已注册提取器列表
    """
    @staticmethod
    def parserList():
        return DateParseManager.__parserList
    
    # 根据提取器的名字查找并返回提取器
    @staticmethod
    def parserByName (name):
        for k, v in DateParseManager.__parserList.items ():
            if k == name:
                return v
        return None
    
    # 检测文件名是否为支持的类型
    @staticmethod
    def TypeParser (filename):
        for name, parser in DateParseManager.parserList().items ():
            #if parser.IsType (filename):
            if filename in parser:
                return name, parser
            #print (parser.FileType ())
            #for ftype in parser.FileType ():
            #    if fnmatch.fnmatch (filename, ftype):
            #        return name, parser
        return None, None
    
    # 设置提取器的使用优先级列表
    @staticmethod
    def SetParserPriorityList (priList):
        DateParseManager.__parserPriorityList = priList

    # 返回提取器的使用优先级列表
    @staticmethod
    def GetParserPriorityList ():
        return DateParseManager.__parserPriorityList

# 解析器基类
class DateParser (object):
    def __init__ (self):
        self.SetTypeList (())
    
    # 返回一个datetime.date对象
    # 如果解析失败则返回None
    def Date (self, filename):
        return None
    
    # 检测文件名是否为支持的类型
    def IsType (self, filename):
        for ftype in self.TypeList ():
            if fnmatch.fnmatch (filename, ftype):
                return True
        return False

    # 返回支持的文件类型通配符列表
    # 例如：return ("*.jpg", "*.mkv", "*.mts")
    def TypeList (self):
        return self._FileType

    """
    设置支持的文件类型列表
    可以由用户自定义。因为例如exiftool支持的文件类型种类繁多，全部写死在程序中不现实，所以可以由用户在配置文件中灵活定义。
    """
    def SetTypeList (self, typeList):
        self._FileType = typeList

    """
    实现 if filename in DateParser:
    表现方法
    """
    def __contains__ (self, item):
        return self.IsType (item)
    

if __name__ == "__main__":
    DateParseManager.RegisterParser ("EXIF2", DateParser())
    for k in DateParseManager.parserList():
        print ("Name:", k)

    #print (DateParseManager ().IsType ("fda.mts"))
