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


if __name__ == "__main__":
    # http://blog.csdn.net/kiki113/article/details/4062063
    # 看第三段
    import sys
    reload (sys)
    sys.setdefaultencoding('utf-8')


    pCfgID        = "DateAnalyst"
    pCmdName      = "1a.cmd"
    pMediaSrcRoot = "d:\\@My\\Mobile\\HTC.Desire.G7\\SDCard\\DCIM"
    pMediaTargetRoot = pMediaSrcRoot
    pMediaExistsRoot = pMediaSrcRoot

    mtc = MTConfig ()
    mtc.ReadConfig ("Config.xml")

    cfg = mtc.GetConfig (pCfgID)

    if cfg is None:
        exit (1)

    # mt = MediaTrimmer (cfg, [MediaDateProcessRule (["jpg", "raw", "crw", "cr2", "rw2", "nef", "nrw", "arw", "srf", "sr2", "pef", "ptx", "srw"]), \
    #                              MediaDateProcessRule (["avi", "mov"], "thm", MediaDateProcessRule.PF_FOLLOWMAIN | MediaDateProcessRule.PF_GETINFO), \
    #                              MediaDateProcessRule (["m2ts"], "modd", MediaDateProcessRule.PF_FOLLOWMAIN), \
    #                              MediaDateProcessRule (["mts"]), \
    #                              MediaDateProcessRule (["m4v", "mp4"]), \
    #                              MediaDateProcessRule (["3gp"])
    #                          ])



    mt = MediaTrimmer (cfg)
            
    #mt.Scan ("d:\\@My\\Mobile\\HTC.Desire.G7\\SDCard\\DCIM", "d:\\@My\\Mobile\\HTC.Desire.G7\\SDCard\\DCIM", "d:\\@My\\Mobile\\HTC.Desire.G7\\SDCard\\DCIM\_Repeat")

    mt.Scan (pCmdName, pMediaSrcRoot, pMediaTargetRoot, pMediaExistsRoot)
