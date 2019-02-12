#! /usr/bin/env python
# -*- coding: utf-8 -*-

from XMLUtility import XMLParser
#from MediaRule import MediaProcessRule
#from MediaDateRule import MediaDateProcessRule
import os

class MTCfgData (object):
    
    #######################################################
    # 定制Parser的行为
    class BehaviorCustomize (object):
        class Behavior (object):
            def __init__ (self):
                self.id          = ""
                self.fileTypeList    = ""


        def __init__ (self):
            self.id       = ""
            self.parserPriority = []
            self.parserList = []

        def AddParserBehavior (self, parser):
            self.parserList.append (parser)

    #######################################################
    class Output (object):
        def __init__ (self):
            self.id              = ""
            self.cmd_head        = ""
            self.cmd_body_single = ""
            self.cmd_tail        = ""

    #######################################################
    def __init__ (self):
        self.customizeList = {}
        self.outputList  = {}

    def AddCustomize (self, customize):
        self.customizeList[customize.id] = customize

    def AddOutput (self, output):
        self.outputList[output.id] = output


class MTConfig (object):

    MEDIA_RULE_CLASS_LIST = []

    def __init__ (self):
        self.__CfgData = MTCfgData ()

    def TranslateFlagValue (self, parserID, flagStr):
        for c in self.MEDIA_RULE_CLASS_LIST:
            if c.RULE_ID == parserID:
                return c.TranslateFlagValue (flagStr)

        return 0

    def TranslateMethodValue (self, parserID, methodStr):
        for c in self.MEDIA_RULE_CLASS_LIST:
            if c.RULE_ID == parserID:
                return c.TranslateMethodValue (methodStr)

        return None


    def ReadConfig (self, cfgFile):
        if not os.path.exists (cfgFile):
            return False

        xParser = XMLParser ()

        xmldom = xParser.ParseFile (cfgFile)
        cfgroot = xParser.getFirstNode (xmldom, "config")

        if cfgroot is None:
            return False

        # 解析 <customize></customize> 的设置
        customizeNodeList = xParser.getSpeicNodeList (cfgroot, "customize")
        for customizeNode in customizeNodeList:

            customizeID = xParser.getNodeAttribValue (customizeNode, "id")
            if customizeID is None:
                continue

            customize    = MTCfgData.BehaviorCustomize ()
            customize.id = customizeID


            parserPriorityStr = xParser.getNodeAttribValue(customizeNode, "parserPriority")
            if parserPriorityStr is not None:
                customize.parserPriority = parserPriorityStr.split (";")

            # 获取 parser 列表
            parserNodeList = xParser.getSpeicNodeList (customizeNode, "parser")
            for parserNode in parserNodeList:
                parserID = xParser.getNodeAttribValue (parserNode, "id")
                if parserID is None or len (parserID) <= 0:
                    continue

                behavior = MTCfgData.BehaviorCustomize.Behavior ()
                behavior.id  = parserID
                
                behavior.fileTypeList = xParser.GetXmlNodeValueList (parserNode, "filetype", None)
                if behavior.fileTypeList is None:
                    continue

                #print parserID, rule.flags, rule.methodList #DEBUG
                customize.AddParserBehavior (behavior)

            self.__CfgData.AddCustomize (customize)


        # 解析 <output></output> 的设置
        outputNodeList = xParser.getSpeicNodeList (cfgroot, "output")
        for outputNode in outputNodeList:
            outputID = xParser.getNodeAttribValue (outputNode, "id")
            if outputID is None:
                continue

            output    = MTCfgData.Output ()
            output.id = outputID
            output.cmd_head        = xParser.GetXmlNodeValue (outputNode, "head", "")
            output.cmd_body_single = xParser.GetXmlNodeValue (outputNode, "bodysingle", "")
            output.cmd_tail        = xParser.GetXmlNodeValue (outputNode, "tail", "")

            self.__CfgData.AddOutput (output)
        
        return self.__CfgData

    def GetCustomizeConfig (self, cfgID):
        if cfgID in self.__CfgData.customizeList.keys ():
            return self.__CfgData.customizeList[cfgID]
        return None

    def GetOutputConfig (self, cfgID):
        if cfgID in self.__CfgData.outputList.keys ():
            return self.__CfgData.outputList[cfgID]
        return None
