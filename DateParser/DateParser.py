#! /usr/bin/env python
# -*- coding: utf-8 -*-


class DateParseManager (object):

    __parserList = {}

    def __init__ (self):
        pass
 
    @staticmethod
    def RegisterParser (name, parser):
        if not isinstance (parser, DateParser):
        #if not issubclass (parser, DateParser)
            raise TypeError ("%s not is DateParser!" % (parser))

        DateParseManager.__parserList[name] = parser
    
    @staticmethod
    def parserList():
        return DateParseManager.__parserList


class DateParser (object):
    def __init__ (self):
        pass

    # 返回一个datetime.date对象
    # 如果解析失败则返回None
    def Date (self, filename):
        return None
    
    # 返回支持的文件类型扩展名列表，必须是小写，扩展名需要以.开头
    # 例如：return (".jpg", ".mkv", ".mts")
    def FileType (self):
        return ()
    

if __name__ == "__main__":
    DateParseManager.RegisterParser ("EXIF2", DateParser())
    for k in DateParseManager.parserList():
        print ("Name:", k)
