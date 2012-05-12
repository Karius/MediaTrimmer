#! /usr/bin/env python
# -*- coding: utf-8 -*-

from BaseType import Result
import os

#####################################################
# 存放需要被检查解析的媒体的类型及其处理方法的类
# 
class MediaProcessRule  (object):

    # partner flags
    F_NONE        = 0      # 无任何规则
    PF_FOLLOWMAIN = 1      # 跟随主文件进行移动
    PF_GETINFO    = 2      # 从伴侣文件中获取日期


    def __init__ (self, extList, partnerExt = None, partnerFlag = 0, methodList = []):
        self.__ExtList     = []
        self.__PartnerExt  = partnerExt
        self.__ParseMethod = methodList
        self.__Flags       = partnerFlag

        for v in extList:
            if v[0] <> '.':
                v = "." + v
            self.__ExtList.append (os.path.normcase (v))
        if isinstance (partnerExt, str) and partnerExt[0] <> '.':
            partnerExt = "." + partnerExt
            self.__PartnerExt = os.path.normcase (partnerExt)
        else:
            self.__partnerExt = None

    # 返回本对象可处理的文件扩展名列表
    def ExtList (self):
        return self.__ExtList

    # 返回伴侣文件扩展名
    def PartnerFileExt (self):
        return self.__PartnerExt

    # 伴侣文件列表是否有伴侣文件
    def HasPartner (self):
        return self.__PartnerExt <> None

    # 返回 Flag
    def GetFlags (self):
        return self.__Flags

    # 返回媒体文件分析方法列表
    def ParseMethod (self):
        return self.__ParseMethod

    # 检查参数指定文件的扩展名是否在本类所能处理文件类型中
    def IsRuleFile (self, filename):
        ext = os.path.splitext (os.path.normcase(filename))[1]
        return ext in self.__ExtList

    # 检查参数指定文件是否为伴侣文件
    def IsPartnerFile (self, filename):
        ext = os.path.splitext (os.path.normcase(filename))[1]
        return ext == self.__PartnerExt

    # 根据伴侣文件名返回主文件名列表
    def GetMainFilenameList (self, partnerName):
        r = []
        for v in self.__ExtList:
            r.append (os.path.splitext (partnerName)[0] + v)
        return r

    # 根据主文件名称返回伴侣文件全路径
    def GetPartnerFilename (self, mainfilename):
        return os.path.splitext (mainfilename)[0] + self.PartnerFileExt ()

    # 对参数中指定的全路径文件名进行分析处理
    def DoProcess (self, fullpath):
        pass



#####################################################
# 存放需要被检查解析的媒体的类型及其处理方法的类
# 
class MediaRuleManager (object):
    def __init__ (self, ruleObjList = []):
        self.__RuleList = ruleObjList

    def IsMediaRelevantFile (self, fullpath):
        for rule in self.__RuleList:
            if rule.IsRuleFile (fullpath) or rule.IsPartnerFile (fullpath):
                return Result (True, {'reason':1, 'rule':rule})
        return Result (False)

    def DoAction (self, fullpath):
        rule = self.IsMediaRelevantFile (fullpath)
        if rule:
            return rule.rule.DoProcess(fullpath)
        return Result (False, {'reason':1})
