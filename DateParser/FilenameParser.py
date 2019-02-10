#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .DateParser import DateParseManager
from .DateParser import DateParser
from datetime import date

# 提取文件名中的日期
class FilenameParser(DateParser):
    def __init__ (self):
        pass
    
    def Date (self, filename):
        
        #date(year, month, day)
        pass



if __name__ != "__main__":
    DateParseManager.RegisterParser ("FILENAME", FilenameParser)