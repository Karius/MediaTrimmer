#! /usr/bin/env python
# -*- coding: utf-8 -*-

from BaseType import BaseDataList, BaseDataDict
import os


##################################################
# 存放并管理相同目标文件夹的文件列表类
class FileLocationCell (object):
    # target : 目标文件夹
    def __init__ (self, target = ""):
        self.__SrcFileDict = BaseDataDict ()
        self.__TargetPath  = target

    # 设置目标路径
    def SetTargetPath (self, target):
        self.__TargetPath = target

    # 返回当前目标路径
    def TargetPath (self):
        return self.__TargetPath

    # 检查两个路径是否为同一路径
    def samefile (self, path1, path2):
        return os.path.normcase(os.path.normpath(path1)) == \
            os.path.normcase(os.path.normpath(path2))

    # 检查参数中的路径是否为当前设置的目标路径
    def IsTargetPath (self, path):
        return self.samefile (self.TargetPath (), path)

    # 增加一个文件到列表中（需要全路径文件）
    def Add (self, fullpath):
        if not os.path.isabs (fullpath):
            return False
        #self.__SrcFileDict[os.path.normcase (fullpath)] = os.path.split (fullpath)
        self.__SrcFileDict[os.path.normcase (fullpath)] = fullpath
        return True

    # 检查参数中的文件是否已存在列表中（需要全路径文件）
    def Has (self, fullpath):
        return os.path.normcase (fullpath) in self.__SrcFileDict

    # 返回文件列表
    def FileList (self):
        return self.__SrcFileDict

    # 返回列表中的文件数量
    def Size (self):
        return len (self.__SrcFileDict)

#####################################################
# 用于管理 FileLocationCell 类的类
class FileLocationManager (object):
    def __init__ (self):
        self.__FLCellList = BaseDataList ()
        pass

    # 根据参数中的目标路径来找出同样目标路径的 FileLocationCell 类对象实例
    def GetCellByTargetPath (self, TargetPath):
        for v in self.__FLCellList:
            if v.IsTargetPath (TargetPath):
                return v
        return None


    # 增加一个文件到指定的目标列表类中
    # srcFullpath: 需要增加的文件（全路径）
    # TargetPath: 目标路径
    def AddFile (self, srcFullpath, TargetPath):
        cell = self.GetCellByTargetPath (TargetPath)
        #print ("SrcFullPath:%s, [Target]:%s" % (srcFullpath,TargetPath), cell)

        if cell is None:
            cell = FileLocationCell (TargetPath)
            self.__FLCellList.Append (cell)

        cell.Add (srcFullpath)
        #print (cell.FileList ().Dict ())

    # 返回 FileLocationCell 类实例的列表
    def GetCellList (self):
        return self.__FLCellList
