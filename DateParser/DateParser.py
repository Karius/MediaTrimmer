# -*- coding: utf-8 -*-

import fnmatch

class DateParseManager (object):

    __parserList = {}

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


class DateParser (object):
    def __init__ (self):
        self.setTypeList (())
    
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
    设置列表
    """
    def setTypeList (self, typeList):
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
