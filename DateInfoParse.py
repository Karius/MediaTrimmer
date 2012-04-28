#! /usr/bin/env python
# -*- coding: utf-8 -*-

#from BaseType import BaseDataList, BaseDataDict
import datetime
import exif
import os


####################################################
# 根据指定的正则表达式来解析一个包含日期与时间的字符串
class DateTimeStringParser (object):
    # parseREStr: 指定用于解析包含日期时间字符串的正则表达式，如果省略，则使用一个通用的正则表达式
    def __init__ (self, parseREStr = None):
        if parseREStr is None:
            self.__parseREStr = r'(\d{4}).*?(\d{2}).*?(\d{2}).*?(\d{2}).(\d{2}).(\d{2})'
        else:
            self.__parseREStr = parseREStr

    # 解析一个包含日期时间的字符串
    # datetimeStr: 一个包含日期时间的字符串
    # pareREStr: 用于解析的正则表达式，如果省略的话则使用本类构造函数时传入的参数
    # 返回标准的 python 类：datetime.datetime
    def Parse (self, datetimeStr, parseREStr = None):
        if parseREStr is None:
            parseREStr = self.__parseREStr

        dt = None

        import re
        sList = re.compile (parseREStr, re.I).findall (datetimeStr)
        #print ("LEN", sList)
        if (len (sList) >= 1) and (len (sList[0]) >= 3):
            dtList = sList[0]
            _Y = int (dtList[0])
            _M = int (dtList[1])
            _D = int (dtList[2])
            _h = _m = _s = 0
            if len (dtList) >= 5:
                _h = int (dtList[3])
                _m = int (dtList[4])
                if len (dtList) >= 6:
                    _s = int (dtList[5])
            dt = datetime.datetime (_Y, _M, _D, _h, _m, _s)

        return dt


#####################################################
# 分析一个媒体文件从其内部获取能够用以表示其生成日期的信息，比如 EXIF
# 这是一个基类
class MediaAnalysiser (object):
    def __init__ (self):
        pass

    def AnalysisMedia (self):
        return None

########################################################
# MediaAnalysiser 派生类
# 根据媒体文件中的 Exif 信息获取媒体生成日期
class MediaBirthdayAnalysisByExif (MediaAnalysiser):
    def __init__ (self):
        MediaAnalysiser.__init__ (self)
        self.__ExifDateParser = DateTimeStringParser ()

    def AnalysisMedia (self, fullpath):
        tags = exif.parse (fullpath, 0, 0);

        if tags.has_key ("DateTimeOriginal"):
            return self.__ExifDateParser.Parse (tags["DateTimeOriginal"])
        elif tags.has_key ("DateTime"):
            return self.__ExifDateParser.Parse (tags["DateTime"])

        return None


########################################################
# MediaAnalysiser 派生类
# 根据媒体的文件名信息获取媒体生成日期
class MediaBirthdayAnalysisByFilename (MediaAnalysiser):
    def __init__ (self):
        MediaAnalysiser.__init__ (self)
        self.__FilenameDateParser = DateTimeStringParser (r'^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})')

    def AnalysisMedia (self, fullpath):
        fpinfo = os.path.split (fullpath)
        dt = self.__FilenameDateParser.Parse (fpinfo[1])
        if dt is None:
            # 如果不成功则分析文件名中是否只有日期信息
            dt = self.__FilenameDateParser.Parse (fpinfo[1],  r'^(\d{4})(\d{2})(\d{2})')

        return dt


########################################################
# MediaAnalysiser 派生类
# 根据媒体文件的修改日期获取媒体生成日期
class MediaBirthdayAnalysisByFileModifyDate (MediaAnalysiser):
    def __init__ (self):
        MediaAnalysiser.__init__ (self)
        self.__FileDateParser = DateTimeStringParser (r'^(\d{4}).(\d{2}).(\d{2}) (\d{2}).(\d{2}).(\d{2})')

    def AnalysisMedia (self, fullpath):
        return self.__FileDateParser.Parse (datetime.datetime.fromtimestamp (os.path.getmtime (fullpath)).strftime("%Y-%m-%d %H:%M:%S"))


#####################################################
# 存放需要被检查解析的媒体的类型及其处理方法的类
# 
class MediaProcessRule  (object):
    # DEFAULT  = 0
    # EXIF     = 1
    # FILENAME = 2
    # FILEDATE = 3

    def __init__ (self, extList, partner = (), methodList = (MediaBirthdayAnalysisByExif (),)):
        self.__ExtList = extList
        self.__DateParseMethod = methodList
        self.__Partner = partner

    # 返回本对象可处理的文件扩展名列表
    def ExtList (self):
        return self.__ExtList

    # 返回伴侣文件列表
    def PartnerFiles (self):
        return self.__Partner

    # 返回媒体文件生成日期分析类对象列表
    def DateParseMethod (self):
        return self.__DateParseMethod

    # 检查对象是否为 MediaAnalysiser 类或者其继承类的实例
    def IsMediaAnalysiser (self, classobj):
        #return issubclass (classobj, MediaAnalysiser)
        return isinstance (classobj, MediaAnalysiser)

    # 检查参数指定文件的扩展名是否在本类所能处理文件类型中
    def IsRuleFile (self, filename):
        pass

    # 检查参数指定文件是否在伴侣文件列表中
    def IsPartnerFile (self, filename):
        pass

    # 对参数中指定的全路径文件名进行分析处理
    def DoProcess (self, fullpath):
        pass



#####################################################
# 存放需要被检查解析的媒体的类型及其处理方法的类
# 
class MediaDateProcessRule  (MediaProcessRule):
    # DEFAULT  = 0
    # EXIF     = 1
    # FILENAME = 2
    # FILEDATE = 3

    def __init__ (self, extList, partner = (), methodList = (MediaBirthdayAnalysisByExif (),)):
        MediaProcessRule.__init__ (self, extList, partner, methodList)

    # 对参数中指定的全路径文件名进行分析处理
    def DoProcess (self, fullpath):
        pass


# unit test

if __name__ == "__main__":
    # http://zh.wikipedia.org/zh-hk/RAW
    tl = (MediaDateProcessRule (("jpg", "raw", "crw", "cr2", "rw2", "nef", "nrw", "arw", "srf", "sr2", "pef", "ptx", "srw")), \
          MediaDateProcessRule (("avi", "mov"), ("thm")), \
          MediaDateProcessRule (("m2ts",), ("modd")), \
          MediaDateProcessRule (("mts",)), \
          MediaDateProcessRule (("m4v", "mp4")) \
          )
    for v in tl:
        print (v.ExtList (), v.DateParseMethod (), v.PartnerFiles ())

    # flc = FileLocationCell ("c:\\t")
    # flc.Add ("c:\\1.jpg")
    # print (flc.Size ())

    # print (flc.Has ("C:\\1.JPG"))


    # #print (flc.samefile ("C:\tmp", "c:\tmp"))
    # print (flc.IsTargetPath ("c:\\T\\"))


    # flm = FileLocationManager ()
    # flm.AddFile ("C:\\tmp\\1", "d:\\new")

    
    
    # dtp = DateTimeStringParser ()
    # d = dtp.Parse ("20120401 13:01:05")
    # print (d)
    # print (d.strftime ("%Y-%m-%d"))

    ex = MediaBirthdayAnalysisByExif ()
    print (ex.AnalysisMedia ("c:\\tmp\\___\\exif_\\exif_\\IMAG0210.jpg"))

    ex = MediaBirthdayAnalysisByFilename ()
    print (ex.AnalysisMedia ("f:\\@My\\Memory\\_Working\\Importing\\_2012-3-24\\1\\20120324213817.m2ts"))

    ex = MediaBirthdayAnalysisByFileModifyDate ()
    print (ex.AnalysisMedia ("c:\\tmp\\___\\exif_\\exif_\\t.py"))

    mdp = MediaDateProcessRule (("m2ts",), ("modd"))



