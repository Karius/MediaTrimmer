#! /usr/bin/env python
# -*- coding: utf-8 -*-


from FileLocation import FileLocationManager
from MediaRule import MediaRuleManager
from DateInfoParse import MediaDateProcessRule
from Tools import ScanDir
from Config import MTCfgData, MTConfig
import os


class MediaTrimmer (object):
    def __init__ (self, cfg):
        self.__Cfg                 = cfg

        mediaRuleList = []
        for rule in cfg.ruleList:
            if rule.typeid == "date":
                ruleObj = MediaDateProcessRule (rule.extList, rule.partner, rule.flags, rule.methodList)
            else:
                continue

            mediaRuleList.append (ruleObj)

        self.__MediaRuleManager    = MediaRuleManager (mediaRuleList)
        self.__FileLocationManager = FileLocationManager ()


    def Scan (self, outputCmdName, rootDir, targetDir = None, existsDir = None, level = None):
        if targetDir is None:
            targetDir = rootDir
        if existsDir is None:
            existsDir = os.path.join (rootDir, "_Repeat")

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
            cellTargetDir = os.path.join (targetDir, cell.TargetPath ())
            cellExistsDir = os.path.join (existsDir, cell.TargetPath ())
            for mediaName in cell.FileList ():
                #cmdBody = cmdBody + 'call :moveto "%s" "%s" "%s"\n' % (mediaName, os.path.join (targetDir, cell.TargetPath ()), os.path.join (existsDir, cell.TargetPath ()))
                line = self.__Cfg.cmd_body_single.replace ("?SRC_MEDIA_FILE?", mediaName).replace ("?TARGET_DIR?", cellTargetDir).replace ("?EXISTS_DIR?", cellExistsDir)
                cmdBody = cmdBody + line

        cmdAll = (self.__Cfg.cmd_head + cmdBody + self.__Cfg.cmd_tail).replace ("\\n", "\n")
        f = file(outputCmdName, "w")
        f.write (cmdAll.decode('utf-8', 'ignore').encode('GBK'))
        #f.write (cmdAll)
        f.close ()

####################################################################
def Main (argv):
    # 设置系统默认编码为 utf-8。如果不设置在 decode ('utf-8').encode ('GBK') 时将会出现 UnicodeValueError 之类的异常
    # http://blog.csdn.net/kiki113/article/details/4062063
    # 看第三段
    import sys
    reload (sys)
    sys.setdefaultencoding('utf-8')


    # pCfgID        = "DateAnalyst"
    # pCmdName      = "1a.cmd"
    # pMediaSrcRoot = "d:\\@My\\Mobile\\HTC.Desire.G7\\SDCard\\DCIM"

    pCfgID        = None
    pCmdName      = "output.cmd"
    pMediaSrcRoot = None
    pMediaTargetRoot = None
    pMediaExistsRoot = None

    import getopt
    try:
        opts, args = getopt.getopt (argv, "c:i:m:t:e", ["cmdname=", "id=", "mediaroot=", "targetroot=", "existsroot="])

        for opt, arg in opts:
            if opt in ("-c", "--cmdname"):
                pCmdName = arg
            elif opt in ("-i", "--id"):
                pCfgID = arg
            elif opt in ("-m", "--mediaroot"):
                pMediaSrcRoot = arg
            elif opt in ("-t", "--targetroot"):
                pMediaTargetRoot = arg
            elif opt in ("-e", "--existsroot"):
                pMediaExistsRoot = arg
    except:
        pass

    if pCfgID is None:
        print ("Config ID is null!")
        sys.exit (1)

    if pMediaSrcRoot is None:
        print ("Media root dir is null!")
        sys.exit (1)
    elif not os.path.exists (pMediaSrcRoot):
        print ("Media root dir is not exists!")
        sys.exit (1)


    mtc = MTConfig ()
    if not mtc.ReadConfig ("Config.xml"):
        print ("Config.xml not exists.")
        sys.exit (2)

    cfg = mtc.GetConfig (pCfgID)

    if cfg is None:
        print ("cfg id (%s) not exists" % (pCfgID))
        sys.exit (3)

    mt = MediaTrimmer (cfg)

    mt.Scan (pCmdName, pMediaSrcRoot, pMediaTargetRoot, pMediaExistsRoot)


if __name__ == "__main__":
    import sys
    Main (sys.argv[1:])
