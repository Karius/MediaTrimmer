#! /usr/bin/env python
# -*- coding: utf-8 -*-


from FileLocation import FileLocationManager
from MediaRule import MediaRuleManager
from DateInfoParse import MediaDateProcessRule
from Tools import ScanDir
import os


class MediaTrimmer (object):
    def __init__ (self, mediaRuleList):
        self.__MediaRuleManager    = MediaRuleManager (mediaRuleList)
        self.__FileLocationManager = FileLocationManager ()



    def Scan (self, rootDir, targetDir, existDir, level = None):
        fileList = ScanDir (rootDir, level)

        # 扫描收集所有符合条件的媒体文件到 self.__FileLocationManager 对象中
        for mediaName in fileList:
            r = self.__MediaRuleManager.DoAction (mediaName)
            if r:
                self.__FileLocationManager.AddFile (mediaName, r.data)

        # 处理收集完成的所有媒体文件
        # 遍历每个目标目录相同的 Cell 列表
        cmdBody = ""
        for cell in self.__FileLocationManager.GetCellList ():
            for mediaName in cell.FileList ():
                cmdBody = cmdBody + 'call :moveto "%s" "%s" "%s"\n' % (mediaName, os.path.join (targetDir, cell.TargetPath ()), os.path.join (existDir, cell.TargetPath ()))

        cmdHead = "@echo off"
        cmdTail = """
goto :EOF

rem ##########################################################
rem %1 待移动的文件全路径
rem %2 正常移动到的目标路径
rem %3 当目标文件已存在时将移动到的路径
:moveto
if exist "%~2\%~n1%~x1" (
   call :movefileto %1 %3
) else (
   call :movefileto %1 %2
)
goto :EOF


rem %1 待移动的文件全路径
rem %2 移动到的目标路径
:movefileto
if not exist %2 md %2
move %1 %2
goto :EOF


rem ###########################################################
rem 该过程为上面两个过程的合体
rem %1 待移动的文件全路径
rem %2 正常移动到的目标路径
rem %3 当目标文件已存在时将移动到的路径
:movetofull
if exist "%~2\%~n1%~x1" (
   if not exist %3 md %3
   move %1 %3
) else (
   if not exist %2 md %2
   move %1 %2
)
goto :EOF
"""
        cmdAll = cmdHead + cmdBody + cmdTail
        f = file("1.cmd", "w")
        f.write (cmdAll)
        f.close ()


if __name__ == "__main__":
    #tl = MediaRuleManager ([
          #   MediaDateProcessRule (["jpg", "raw", "crw", "cr2", "rw2", "nef", "nrw", "arw", "srf", "sr2", "pef", "ptx", "srw"]), \
          #   MediaDateProcessRule (["avi", "mov"], "thm", MediaDateProcessRule.PF_FOLLOWMAIN or MediaDateProcessRule.PF_GETINFO), \
          #   MediaDateProcessRule (["m2ts"], "modd", MediaDateProcessRule.PF_FOLLOWMAIN), \
          #   MediaDateProcessRule (["mts"]), \
          #   MediaDateProcessRule (["m4v", "mp4"]), \
          #   MediaDateProcessRule (["3gp"]), \
          # ])

    #print (tl.DoAction ("20120402183751.m2ts"))

                
            mt = MediaTrimmer ([MediaDateProcessRule (["jpg", "raw", "crw", "cr2", "rw2", "nef", "nrw", "arw", "srf", "sr2", "pef", "ptx", "srw"]), \
                               MediaDateProcessRule (["avi", "mov"], "thm", MediaDateProcessRule.PF_FOLLOWMAIN or MediaDateProcessRule.PF_GETINFO), \
                               MediaDateProcessRule (["m2ts"], "modd", MediaDateProcessRule.PF_FOLLOWMAIN), \
                               MediaDateProcessRule (["mts"]), \
                               MediaDateProcessRule (["m4v", "mp4"]), \
                               MediaDateProcessRule (["3gp"])
                                ])

            
            mt.Scan ("d:\\@My\\Mobile\\HTC.Desire.G7\\SDCard\\DCIM", "d:\\@My\\Mobile\\HTC.Desire.G7\\SDCard\\DCIM", "d:\\@My\\Mobile\\HTC.Desire.G7\\SDCard\\DCIM\_Repeat")
