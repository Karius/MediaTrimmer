#! /usr/bin/env python
# -*- coding: utf-8 -*-

#from BaseType import BaseDataList, BaseDataDict
from BaseType import Result
from MediaRule import MediaProcessRule
import datetime
import exiftool
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
            try:
                dt = datetime.datetime (_Y, _M, _D, _h, _m, _s)
            except ValueError:
                dt = None

        return dt



#####################################################
# 存放需要被检查解析的媒体的类型及其处理方法的类
# 
class MediaDateProcessRule (MediaProcessRule):

    RULE_ID  = "DATE"  # 本规则类的 ID

    # Flag
    PF_FOLLOWMAIN = 1      # 跟随主文件进行移动
    PF_GETINFO    = 2      # 从伴侣文件中获取日期

    # Method
    EXIF     = 1
    FILENAME = 2
    FILEDATE = 3


    STR_FLAG_DICT = { \
        "PF_GETINFO" : PF_GETINFO, \
        "PF_FOLLOWMAIN" : PF_FOLLOWMAIN \
        }

    STR_METHOD_DICT = { \
        "EXIF" : EXIF, \
        "FILENAME" : FILENAME, \
        "FILEDATE" : FILEDATE \
        }


    def __init__ (self, extList, partnerExt = None, partnerFlag = PF_FOLLOWMAIN, methodList = [EXIF, FILENAME, FILEDATE]):
        MediaProcessRule.__init__ (self, extList, partnerExt, partnerFlag, methodList)
        self.exiftool = exiftool.ExifTool ()
        self.exiftool.start ()

    def __del__ (self):
        self.exiftool.terminate ()



    # 对参数中指定的全路径文件名进行分析处理
    def DoProcess (self, fullpath):

        dt = None

        # 检查是否为可处理的文件类型
        if self.IsRuleFile (fullpath):

            # 如果有伴侣文件，按指定方法从伴侣文件中获取日期信息
            if self.HasPartner () and (self.GetFlags () & self.PF_GETINFO):
                # 获取伴侣文件名
                pfile = self.GetPartnerFilename (fullpath)
                dt = self.GetMediaDate (pfile)

            # dt 如果为 None 有两种情况
            # 一种是其有伴侣文件并通过伴侣文件获取日期信息失败
            # 二是其无伴侣文件， dt 初始化值为 None
            if dt is None:
                dt = self.GetMediaDate (fullpath)


        # 如果当前处理的是伴侣文件
        elif self.IsPartnerFile (fullpath):

            # 如果指定从伴侣文件中获取日期信息则按指定方法从伴侣文件中获取日期信息
            if self.GetFlags () & self.PF_GETINFO:
                dt = self.GetMediaDate (fullpath)

            # 否则从主文件中获取日期信息
            else:
                # 获取符合该伴侣文件的主文件名
                mainFilenameList = self.GetMainFilenameList (fullpath)
                mainFilename = None
                for v in mainFilenameList:
                    if os.path.exists (v):
                        mainFilename = v
                        dt = self.GetMediaDate (mainFilename)

                #print fullpath, dt

        else:
            return Result (False, {'error':1})


        # 获取日期信息失败
        if dt is None:
            return Result (False, {'error':3})

        # 返回格式化后的日期字符串
        return Result (True, {'data':dt.strftime ("%Y-%m-%d")})



    # 内部使用函数，循环使用所用可用的方法解析媒体日期信息
    def GetMediaDate (self, fullpath):
        dt = None
        # 遍历媒体解析方法列表
        for m in self.ParseMethod ():
            dt = self.AnalysisMedia (fullpath, m)
            # 如果解析成功则退出遍历
            if dt is not None:
                break

        return dt
        

    # 内部使用函数，根据指定分析方法去分析指定媒体文件日期信息
    def AnalysisMedia (self, fullpath, method = EXIF):
        if method == self.EXIF:
            ExifDateParser = DateTimeStringParser ()

            #with self.exiftool:
            tags = self.exiftool.get_tags (["DateTimeOriginal", "DateTimeDigitized", "DateTime"], fullpath)
            
            # exif_tool 返回的exif标签带有分组名，例如"EXIF:DateTimeOriginal"
            # 所以下面这个循环做的就是去掉分组名：
            exif_tags = {}
            for tag in tags:
                exif_tags[tag.split(":")[-1]] = tags[tag]

            # print ("tags>>>>:", {x.split(":")[-1] for x in tags})
            for k in ["DateTimeOriginal", "DateTimeDigitized", "DateTime"]:
                #print ("SPLIT::::::::::::", k.split(":")[-1])
                if k in exif_tags:
                    return ExifDateParser.Parse (str(exif_tags[k]))
            return None

        elif method == self.FILENAME:
            fpinfo = os.path.split (fullpath)
            FilenameDateParser = DateTimeStringParser (r'^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})')
            dt = FilenameDateParser.Parse (fpinfo[1])
            if dt is None:
                # 如果不成功则分析文件名中是否只有日期信息
                dt = FilenameDateParser.Parse (fpinfo[1],  r'^(\d{4})(\d{2})(\d{2})')
            return dt

        elif method == self.FILEDATE:
            try:
                FileDateParser = DateTimeStringParser (r'^(\d{4}).(\d{2}).(\d{2}) (\d{2}).(\d{2}).(\d{2})')
                return FileDateParser.Parse (datetime.datetime.fromtimestamp (os.path.getmtime (fullpath)).strftime("%Y-%m-%d %H:%M:%S"))
            except IOError:
                pass
            except WindowsError: # 当 fullpath 中的文件不存在时，os.path.getmtime 会抛出 WindowsError 错误。比如 5D3 的 *.MOV 文件就不像 7D 一样有 *.THM 伴侣文件
                pass
                
            return None

        else:
            return None



# unit test

if __name__ == "__main__":
    # http://zh.wikipedia.org/zh-hk/RAW
    tl = (MediaDateProcessRule (["jpg", "raw", "crw", "cr2", "rw2", "nef", "nrw", "arw", "srf", "sr2", "pef", "ptx", "srw"]), \
          MediaDateProcessRule (["avi", "mov"], "thm", MediaDateProcessRule.PF_FOLLOWMAIN or MediaDateProcessRule.PF_GETINFO), \
          MediaDateProcessRule (["m2ts"], "modd", MediaDateProcessRule.PF_FOLLOWMAIN), \
          MediaDateProcessRule (["mts"]), \
          MediaDateProcessRule (["m4v", "mp4"]) \
          )
    # for v in tl:
    #     print (v.ExtList (), v.DateParseMethod (), v.PartnerFiles ())
    #     print (v.IsRuleFile ("test.cr2"))
    #     print (v.IsPartnerFile ("test.thm"))

    # print (tl[0].DoProcess ("1.jpg"))
    # print (tl[0].DoProcess ("2.jpg"))

    # print (tl[2].DoProcess ("20120402183751.m2ts"), tl[2].DoProcess ("20120402183751.modd"))

    #print (tl[1].DoProcess ("c:\\w\\3.avi"))


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

    # ex = MediaBirthdayAnalysisByExif ()
    # print (ex.AnalysisMedia ("c:\\tmp\\___\\exif_\\exif_\\IMAG0210.jpg"))

    # ex = MediaBirthdayAnalysisByFilename ()
    # print (ex.AnalysisMedia ("f:\\@My\\Memory\\_Working\\Importing\\_2012-3-24\\1\\20120324213817.m2ts"))

    # ex = MediaBirthdayAnalysisByFileModifyDate ()
    # print (ex.AnalysisMedia ("c:\\tmp\\___\\exif_\\exif_\\t.py"))

    # mdp = MediaDateProcessRule (("m2ts",), ("modd"))



    al = [MediaDateProcessRule,]
    print (MediaDateProcessRule, al[0])
    print (al[0].RULE_ID)
    print (al[0].TranslateFlagValue ("PF_GETINFO"))
