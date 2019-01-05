#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

# gather
# rootDir: 指定开始扫描的顶层目录
# level: 扫描的层数。0: 无限制，扫描所有层数
def ScanDir (rootDir, filesort = False, level = None):

    # 扫描一个目录列表内的所有文件与目录信息
    def ScanSingle (rootDirList):
        fList = []
        dList  = []
        # 扫描 rootDirList 目录列表中的所有目录
        for root in rootDirList:
            # 开始扫描每一个指定目录
            for name in os.listdir (root):
                newname = os.path.join (root, name)
                if os.path.isdir(newname):
                    dList.append (newname)
                else:
                    fList.append (newname)

        return dList, fList

    # 所有的文件列表
    fileList  = []
    currLevel = 0
    # 开始扫描的顶层目录
    scanDirList = [rootDir]

    # 默认 level 为 0
    if level is None:
        level = 0

    while True:
        scanDirList, nfList = ScanSingle (scanDirList)
        fileList = fileList + nfList
        currLevel = currLevel + 1

        # 如果再没有任何子目录则退出循环
        if len (scanDirList) <= 0:
            break
        # 如果层数无限制则继续扫描
        elif level <= 0:
            continue
        # 如果达到指定扫描层数则退出循环
        elif currLevel >= level:
            break

    if filesort:
        # 根据传入rootDir是否为unicode类型来具体处理
        if isinstance(rootDir,unicode):
            return sorted (fileList, key=unicode.lower)
        else:
            return sorted (fileList, key=str.lower)

    return fileList


def path2Unicode (name):
    # 获取当前文件系统命名的编码规则
    # 如果不这么做在处理含有中文的路径时则会有 UnicodeError 的异常抛出

    # 首先获取当前的文件系统编码
    filesystem_encoding = sys.getfilesystemencoding()

    # 然后使用该编码进行重新编码，将其编码为 unicode
    return unicode (name, filesystem_encoding)

    # 经过上面两行的处理，则可以正常使用含有中文的路径了
    # 别忘了在 python 的源文件开头加上 # -*- coding: utf-8 -*-
    # 该种处理方法来源 http://www.zeuux.org/group/python/bbs/content/18305/

