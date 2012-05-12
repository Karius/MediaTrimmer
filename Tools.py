#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os

# gather
# rootDir: 指定开始扫描的顶层目录
# level: 扫描的层数。0: 无限制，扫描所有层数
def ScanDir (rootDir, level = None):

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

    return fileList
