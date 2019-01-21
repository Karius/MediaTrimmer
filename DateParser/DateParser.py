#! /usr/bin/env python
# -*- coding: utf-8 -*-


class DateParseManager (object):

    __parserList = {}

    def __init__ (self):
        pass
 
    @staticmethod
    def RegisterParser (name, parser):
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

    

if __name__ == "__main__":
    DateParseManager.RegisterParser ("EXIF2", 11)
    for k in DateParseManager.parserList():
        print ("Name:", k)
