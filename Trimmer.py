#! /usr/bin/env python
# -*- coding: utf-8 -*-


from FileLocation import FileLocationManager
from MediaRule import MediaRuleManager
from MediaDateRule import MediaDateProcessRule
from Tools import ScanDir, path2Unicode
from Config import MTCfgData, MTConfig
import os


class MediaTrimmer (object):
    def __init__ (self, analystCfg, outputCfg):
        self.__analystCfg = analystCfg
        self.__outputCfg  = outputCfg

        mediaRuleList = []
        for rule in self.__analystCfg.ruleList:
            # 遍历当前所有的媒体处理规则派生类（在 MTConfig.MEDIA_RULE_CLASS_LIST 中定义)
            for v in MTConfig.MEDIA_RULE_CLASS_LIST:
                if v.RULE_ID == rule.typeid:  # 如果其 ID 符合设置中的 ID 则创建一个其类对象
                    ruleObj = v (rule.extList, rule.partner, rule.flags, rule.methodList)
                
            mediaRuleList.append (ruleObj)

        self.__MediaRuleManager    = MediaRuleManager (mediaRuleList)
        self.__FileLocationManager = FileLocationManager ()


    def Scan (self, outputCmdName, rootDir, targetDir = None, existsDir = None, level = None):

        # 扫描root目录，查找 name 开头的目录，如果有则返回该目录，否则返回defName参数指定的字符串
        def getSimilarDir (root, name, defName):
            for n in os.listdir (root):
                if os.path.isdir(os.path.join (root, n)):
                    if n.lower().find (name.lower()) == 0:
                        return n
            return defName

        if targetDir is None:
            targetDir = rootDir
        if existsDir is None:
            existsDir = os.path.join (targetDir, "_Repeat")

        fileList = ScanDir (rootDir, True, level)

        # 扫描收集所有符合条件的媒体文件到 self.__FileLocationManager 对象中
        for mediaName in fileList:
            r = self.__MediaRuleManager.DoAction (mediaName)
            if r:
                self.__FileLocationManager.AddFile (mediaName, r.data)


        # 处理收集完成的所有媒体文件
        # 遍历每个目标目录相同的 Cell 列表
        cmdBody = ""
        for cell in self.__FileLocationManager.GetCellList ():
            # 这是一个参数，指定可以使用已存在的目标目录，比如自动生成的目标目录为:1989-06-04 但如果有个已存在的目录1989-06-04_XXX，则使用这个目录作为目标目录，如果有多个相似的则使用第一个
            isUseExistsTargetPath = True 
            if isUseExistsTargetPath:
                defCellTargetPath = getSimilarDir (targetDir, cell.TargetPath (), cell.TargetPath ())
            else:
                defCellTargetPath = cell.TargetPath ()

            cellTargetDir = os.path.join (targetDir, defCellTargetPath)
            cellExistsDir = os.path.join (existsDir, defCellTargetPath)

            for mediaName in cell.FileList ():
                line = self.__outputCfg.cmd_body_single.replace (u"?SRC_MEDIA_ROOT_DIR?", mediaName).replace (u"?TARGET_ROOT_DIR?", cellTargetDir).replace (u"?EXISTS_ROOT_DIR?", cellExistsDir)
                cmdBody = cmdBody + line

        cmdAll = (self.__outputCfg.cmd_head + cmdBody + self.__outputCfg.cmd_tail).replace ("\\n", "\n")

        f = file(outputCmdName, "w")
        f.write (cmdAll.decode('utf-8', 'ignore').encode('GBK'))
        #f.write (cmdAll)
        f.close ()

####################################################################
def Main (argv):
    # 设置系统默认编码为 utf-8。如果不设置在 decode ('utf-8').encode ('GBK') 时将会出现 UnicodeValueError 之类的异常
    # http://blog.csdn.net/kiki113/article/details/4062063
    # 看第三段
    #import sys
    #from imp import reload
    #reload (sys)
    #sys.setdefaultencoding('utf-8')

    # 除了上面的设置之外，如果需要处理中文路径，也需要对含有中文的文件名或目录名做如下处理
    # 首先获取当前的文件系统编码
    # filesystem_encoding = sys.getfilesystemencoding()
    # 然后使用该编码进行重新编码，将其编码为 unicode
    # newfilename = unicode (filename, filesystem_encoding)
    # 经过上面两行的处理，则可以正常使用含有中文的路径了
    # 别忘了在 python 的源文件开头加上 # -*- coding: utf-8 -*-
    # 该种处理方法来源 http://www.zeuux.org/group/python/bbs/content/18305/


    # pCfgID        = "DateAnalyst"
    # pCmdName      = "1a.cmd"
    # pMediaSrcRoot = "d:\\@My\\Mobile\\HTC.Desire.G7\\SDCard\\DCIM"

    pAnalystCfgID = None
    pOutputCfgID  = None
    pCmdName      = "Go.cmd"
    pConfigFile   = "Config.xml"
    pMediaSrcRoot = None
    pMediaTargetRoot = None
    pMediaExistsRoot = None

    import getopt
    try:
        opts, args = getopt.getopt (argv, "c:a:m:t:e:s", ["cmdname=", "analystid=", "outputid=", "mediaroot=", "targetroot=", "existsroot=", "config="])

        for opt, arg in opts:
            if opt in ("-c", "--cmdname"):
                pCmdName = arg
            elif opt in ("-a", "--analystid"):
                pAnalystCfgID = arg
            elif opt in ("-o", "--outputid"):
                pOutputCfgID = arg
            elif opt in ("-m", "--mediaroot"):
                pMediaSrcRoot = arg
            elif opt in ("-t", "--targetroot"):
                pMediaTargetRoot = arg
            elif opt in ("-e", "--existsroot"):
                pMediaExistsRoot = arg
            elif opt in ("-s", "--config"):
                pConfigFile = arg
    except:
        pass

    if pAnalystCfgID is None:
        print ("Config ID(Analyst) is null!")
        sys.exit (1)

    if pOutputCfgID is None:
        print ("Config ID(Output) is null!")
        sys.exit (1)

    if pMediaSrcRoot is None:
        print ("Media root dir is null!")
        sys.exit (1)
    elif not os.path.exists (pMediaSrcRoot):
        print ("Media root dir is not exists!")
        sys.exit (1)


    mtc = MTConfig ()
    if not mtc.ReadConfig (pConfigFile):
        print ("Config.xml not exists.")
        sys.exit (2)

    analystCfg = mtc.GetAnalystConfig (pAnalystCfgID)
    outputCfg  = mtc.GetOutputConfig (pOutputCfgID)

    if analystCfg is None:
        print ("analystCfg id (%s) not exists" % (pAnalystCfgID))
        sys.exit (3)
    if outputCfg is None:
        print ("outputCfg id (%s) not exists" % (pOutputCfgID))
        sys.exit (3)

    mt = MediaTrimmer (analystCfg, outputCfg)

    mt.Scan (pCmdName, pMediaSrcRoot, pMediaTargetRoot, pMediaExistsRoot)


if __name__ == "__main__":
    import sys
    Main (sys.argv[1:])
