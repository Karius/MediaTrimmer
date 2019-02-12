#! /usr/bin/env python
# -*- coding: utf-8 -*-


from FileLocation import FileLocationManager
from Tools import ScanDir
from Config import MTCfgData, MTConfig
import os
from DateParser.DateParser import DateParseManager
from DateParser.ExifParser import ExifParser
from DateParser.FiledateParser import FiledateParser

class MediaTrimmer (object):
    def __init__ (self, outputCfg):
        self.__outputCfg  = outputCfg

        self.__FileLocationManager = FileLocationManager ()
        self.__FileLocationList = {}

    # outputCmdName: 输出的批处理文件名
    # rootDir: 待处理的根目录
    # targetDir: 移动到的根目录
    # existsDir: 目标文件已存在时将重名文件存方的目录
    # level: 目录扫描层数
    def Scan (self, outputCmdName, rootDir, targetDir = None, existsDir = None, level = None):

        # 扫描root目录，查找 name 开头的目录，如果有则返回该目录，否则返回defName参数指定的字符串
        def getSimilarDir (root, name, defName):
            if os.path.exists (root):
                for n in os.listdir (root):
                    if os.path.isdir(os.path.join (root, n)):
                        if n.lower().find (name.lower()) == 0:
                            return n
            return defName

        # 确保rootDir是绝对路径
        rootDir = os.path.abspath (rootDir)

        # 如果未设置目标目录则将目标目录设为源目录
        if targetDir is None:
            targetDir = rootDir
        else:
            targetDir = os.path.abspath (targetDir)
        # 当existsDir目录未设置时给个默认目录
        if existsDir is None:
            existsDir = os.path.join (targetDir, "_Repeat")
        else:
            existsDir = os.path.join (os.path.abspath (existsDir), "_Repeat")

        # 开始扫描指定根目录，所有文件存在fileList中
        fileList = ScanDir (rootDir, True, level)

        # 扫描收集所有符合条件的媒体文件到 self.__FileLocationManager 对象中
        for mediaName in fileList:
            # 按照用户设置的提取器使用优先级进行遍历提取器并使用
            for parserID in DateParseManager.GetParserPriorityList ():
                parser = DateParseManager.parserByName (parserID)
                if parser is None:
                    continue
                # 如果该提取器无法解析此种类型文件的日期则遍历下一个提取器
                if not parser.IsType (mediaName):
                    continue
                #parserName, parser = DateParseManager.TypeParser (mediaName)
                parserName = parserID
                if parser is not None:
                    print (mediaName, parserName)
                    """
                    通过提取器解析日期信息，通常是ExifParser，但有些虽然是图片或是视频，但其中并没有包含Exif信息
                    所以这里需要判断一下
                    """
                    dateobj = parser.Date(mediaName)
                    if dateobj is not None:
                        dateStr = dateobj.strftime("%Y-%m-%d")
                        if not (parserName in self.__FileLocationList.keys ()):
                            self.__FileLocationList[parserName] = FileLocationManager ()
                        self.__FileLocationList[parserName].AddFile (mediaName, dateStr)
                        print (dateStr)
                        break  # 正确获取到日期，则退出循环
                    else: # 无法提取日期，这种情况通常发生在媒体文件中不含有EXIF的情况下
                        pass
                else:
                    print ("<No Support File", mediaName)
                
                #r = self.__MediaRuleManager.DoAction (mediaName)
                
                #if r:
                #    self.__FileLocationManager.AddFile (mediaName, r.data)


        # 处理收集完成的所有媒体文件
        cmdBody = ""
        # 遍历所有的存储文件定位信息，每种不同的提取器类提取的文件日期放在各自的FileLocationManager对象中
        for parserName, fileLocatMager in self.__FileLocationList.items ():
            # 提取器的类名，默认为未知
            parserClassName = "UNKNOWN"
            # 根据提取器的ID获取其类实例
            parserObj = DateParseManager.parserByName (parserName)
            # 如果取到类实例则获取其类名
            if parserObj is not None:
                parserClassName = type (parserObj).__name__
            # 将提取器的ID和其类名作为注释添加到批处理中，方便查看是由哪类生成的。
            cmdBody += "REM ParserID:[%s], ClassName:[%s]\n" % (parserName, parserClassName)
            
            # 遍历每个目标目录相同的 Cell 列表
            for cell in fileLocatMager.GetCellList (): # 每个Cell中保存的都是相同目标目录的文件
                # 这是一个参数，指定可以使用已存在的目标目录，比如自动生成的目标目录为:1989-06-04 但如果有个已存在的目录1989-06-04_XXX，则使用这个目录作为目标目录，如果有多个相似的则使用第一个
                isUseExistsTargetPath = True 
                if isUseExistsTargetPath:
                    defCellTargetPath = getSimilarDir (targetDir, cell.TargetPath (), cell.TargetPath ())
                else:
                    defCellTargetPath = cell.TargetPath ()

                cellTargetDir = os.path.join (targetDir, defCellTargetPath)
                cellExistsDir = os.path.join (existsDir, defCellTargetPath)

                for mediaName in cell.FileList ():
                    line = self.__outputCfg.cmd_body_single.replace ("?SRC_MEDIA_ROOT_DIR?", mediaName).replace ("?TARGET_ROOT_DIR?", cellTargetDir).replace ("?EXISTS_ROOT_DIR?", cellExistsDir)
                    cmdBody = cmdBody + line

        cmdAll = (self.__outputCfg.cmd_head + cmdBody + self.__outputCfg.cmd_tail).replace ("\\n", "\n")

        f = open(outputCmdName, "w")
        f.write (cmdAll)
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

    #pAnalystCfgID = None
    pOutputCfgID  = None
    pCmdName      = "Go.cmd"
    pConfigFile   = "Config.xml"
    pMediaSrcRoot = None
    pMediaTargetRoot = None
    pMediaExistsRoot = None

    import getopt
    try:
        opts, args = getopt.getopt (argv, "c:a:m:t:e:s", ["cmdname=", "customizeid=", "outputid=", "mediaroot=", "targetroot=", "existsroot=", "config="])

        for opt, arg in opts:
            # 输出的批处理文件名，默认Go.cmd
            if opt in ("-c", "--cmdname"):
                pCmdName = arg
            # Config.xml文件中的提取器行为ID，如All：<config><customizeid id="All"></customizeid></config>
            elif opt in ("-a", "--customizeid"):
                pCustomizeCfgID = arg
            # Config.xml文件中的输出格式ID，如moveto：<config><output id="moveto"></output></config>
            elif opt in ("-o", "--outputid"):
                pOutputCfgID = arg
            # 待扫描的文件夹
            elif opt in ("-m", "--mediaroot"):
                pMediaSrcRoot = arg
            # 移动到的目录文件夹
            elif opt in ("-t", "--targetroot"):
                pMediaTargetRoot = arg
            # 当移动后的目的文件存在时将同名文件转存到的文件夹
            elif opt in ("-e", "--existsroot"):
                pMediaExistsRoot = arg
            # 指定配置文件名，默认Config.xml
            elif opt in ("-s", "--config"):
                pConfigFile = arg
    except:
        pass

    if pCustomizeCfgID is None:
        print ("Config ID(Customize) is null!")
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

    customizeCfg = mtc.GetCustomizeConfig (pCustomizeCfgID)
    # 遍历提取器的自定义行为
    for parserBehivor in customizeCfg.parserList:
        parser = DateParseManager.parserByName (parserBehivor.id)
        if parser is not None:
            # 设置提取器的针对文件类型列表
            parser.SetTypeList (parserBehivor.fileTypeList)
            # print (parserBehivor.id, parserBehivor.fileTypeList)

    # 设置提取器使用优先级列表
    DateParseManager.SetParserPriorityList (customizeCfg.parserPriority)

    outputCfg  = mtc.GetOutputConfig (pOutputCfgID)    
    

    # if analystCfg is None:
    #     print ("analystCfg id (%s) not exists" % (pAnalystCfgID))
    #     sys.exit (3)
    if outputCfg is None:
        print ("outputCfg id (%s) not exists" % (pOutputCfgID))
        sys.exit (3)

    mt = MediaTrimmer (outputCfg)

    mt.Scan (pCmdName, pMediaSrcRoot, pMediaTargetRoot, pMediaExistsRoot)


if __name__ == "__main__":
    import sys
    Main (sys.argv[1:])
