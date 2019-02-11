#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .DateParser import DateParseManager
from .DateParser import DateParser
from datetime import date, datetime
import os

# 提取文件修改日期
class FiledateParser(DateParser):
    def __init__ (self):
        self.SetTypeList (("*.*"))

    def Date (self, filename):
        t = os.path.getmtime (filename)
        return datetime.fromtimestamp(t)



if __name__ != "__main__":
    DateParseManager.RegisterParser ("FILEDATE", FiledateParser ())