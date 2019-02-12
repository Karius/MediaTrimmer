# -*- coding: utf-8 -*-

from .DateParser import DateParseManager
from .DateParser import DateParser
from .exiftool import ExifTool
from datetime import date
import sys

# 提取媒体文件中的Exif内的日期信息
class ExifParser(DateParser):

    #exiftool = ExifTool ()

    def __init__ (self):
        self.SetTypeList (("*.jpg", "*.mkv", "*.mts"))
    
    def Date (self, filename):
        #date(year, month, day)
        exifdata = None
        with ExifTool() as et:
            exifdata = et.get_tag ("DateTimeOriginal", filename)
        if exifdata is not None:
            edate = exifdata.split(" ")[0]
            return date(int(edate.split(":")[0]), int(edate.split(":")[1]), int(edate.split(":")[2]))

        return None



if __name__ != "__main__":
    # 注册日期提取器
    DateParseManager.RegisterParser ("EXIF", ExifParser ())

elif __name__ == "__main__":
    DateParseManager.RegisterParser ("EXIF", ExifParser ())
    parserName, parser = DateParseManager.TypeParser ("fda.mts")
    print (parserName, parser.TypeList())
    print (parser.Date ("b.jpg"), parser.Date ("d:\\Apps\\ExifToolGui\\M2TS.mts"))
