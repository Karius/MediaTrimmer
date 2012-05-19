#! /usr/bin/env python
# -*- coding: utf-8 -*-

from XMLUtility import XMLParser
from MediaRule import MediaProcessRule
from MediaDateRule import MediaDateProcessRule
import os

class MTCfgData (object):
    
    #######################################################
    class Analyst (object):
        class Rule (object):
            def __init__ (self):
                self.typeid     = ""
                self.extList    = []
                self.partner    = ""
                self.flags      = 0
                self.methodList = []


        def __init__ (self):
            self.id       = ""
            self.ruleList = []

        def AddRule (self, rule):
            self.ruleList.append (rule)

    #######################################################
    class Output (object):
        def __init__ (self):
            self.id              = ""
            self.cmd_head        = ""
            self.cmd_body_single = ""
            self.cmd_tail        = ""

    #######################################################
    def __init__ (self):
        self.analystList = {}
        self.outputList  = {}

    def AddAnalyst (self, analyst):
        self.analystList[analyst.id] = analyst

    def AddOutput (self, output):
        self.outputList[output.id] = output


class MTConfig (object):

    # 所有 MediaProcessRule 的子类都需将其类名称放在此列表中
    MEDIA_RULE_CLASS_LIST = [MediaDateProcessRule]

    def __init__ (self):
        self.__CfgData = MTCfgData ()

    def TranslateFlagValue (self, typeid, flagStr):
        for c in self.MEDIA_RULE_CLASS_LIST:
            if c.RULE_ID == typeid:
                return c.TranslateFlagValue (flagStr)

        return 0

        # if typeid.lower () == "date":
        #     if flagStr == "PF_FOLLOWMAIN":
        #         return MediaProcessRule.PF_FOLLOWMAIN
        #     elif flagStr == "PF_GETINFO":
        #         return MediaProcessRule.PF_GETINFO
        # return 0

    def TranslateMethodValue (self, typeid, methodStr):
        for c in self.MEDIA_RULE_CLASS_LIST:
            if c.RULE_ID == typeid:
                return c.TranslateMethodValue (methodStr)

        return None

        # if typeid.lower () == "date":
        #     if methodStr == "EXIF":
        #         return MediaDateProcessRule.EXIF
        #     elif methodStr == "FILENAME":
        #         return MediaDateProcessRule.FILENAME
        #     elif methodStr == "FILEDATE":
        #         return MediaDateProcessRule.FILEDATE
        # return None

    def ReadConfig (self, cfgFile):
        if not os.path.exists (cfgFile):
            return False

        xParser = XMLParser ()

        xmldom = xParser.ParseFile (cfgFile)
        cfgroot = xParser.getFirstNode (xmldom, "config")

        if cfgroot is None:
            return False

        # 解析 <analyst></analyst> 的设置
        analystNodeList = xParser.getSpeicNodeList (cfgroot, "analyst")
        for analystNode in analystNodeList:

            analystID = xParser.getNodeAttribValue (analystNode, "id")
            if analystID is None:
                continue

            analyst    = MTCfgData.Analyst ()
            analyst.id = analystID

            # 获取 rule 列表
            ruleNodeList = xParser.getSpeicNodeList (analystNode, "rule")
            for ruleNode in ruleNodeList:
                typeid = xParser.getNodeAttribValue (ruleNode, "method")
                if typeid is None or len (typeid) <= 0:
                    continue

                rule = MTCfgData.Analyst.Rule ()
                rule.typeid  = typeid
                
                rule.extList = xParser.GetXmlNodeValueList (ruleNode, "ext", None)
                if rule.extList is None:
                    continue

                rule.partner = xParser.GetXmlNodeValue (ruleNode, "partner", None)

                # 读取标志
                flagList = xParser.GetXmlNodeValueList (ruleNode, "flags", [])
                for f in flagList:
                    rule.flags = rule.flags | self.TranslateFlagValue (typeid, f)

                # 读取解析方法列表
                methodList = xParser.GetXmlNodeValueList (ruleNode, "method", [])
                for m in methodList:
                    rule.methodList.append (self.TranslateMethodValue (typeid, m))

                #print typeid, rule.flags, rule.methodList #DEBUG
                analyst.AddRule (rule)

            self.__CfgData.AddAnalyst (analyst)


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

    def GetAnalystConfig (self, cfgID):
        if cfgID in self.__CfgData.analystList.keys ():
            return self.__CfgData.analystList[cfgID]
        return None

    def GetOutputConfig (self, cfgID):
        if cfgID in self.__CfgData.outputList.keys ():
            return self.__CfgData.outputList[cfgID]
        return None
