#! /usr/bin/env python
# -*- coding: utf-8 -*-

from XMLUtility import XMLParser
from MediaRule import MediaProcessRule
from DateInfoParse import MediaDateProcessRule
import os

class MTCfgData (object):
    
    class Rule (object):
        def __init__ (self):
            self.typeid     = ""
            self.extList    = []
            self.partner    = ""
            self.flags      = 0
            self.methodList = []
        
    def __init__ (self):
        self.id              = ""
        self.cmd_head        = ""
        self.cmd_body_single = ""
        self.cmd_tail        = ""

        self.ruleList        = []

    def AddRule (self, rule):
        self.ruleList.append (rule)


class MTConfig (object):
    def __init__ (self):
        self.__CfgList = {}

    def TranslateFlagValue (self, typeid, flagStr):
        if typeid.lower () == "date":
            if flagStr == "PF_FOLLOWMAIN":
                return MediaProcessRule.PF_FOLLOWMAIN
            elif flagStr == "PF_GETINFO":
                return MediaProcessRule.PF_GETINFO


        return 0

    def TranslateMethodValue (self, typeid, methodStr):
        if typeid.lower () == "date":
            if methodStr == "EXIF":
                return MediaDateProcessRule.EXIF
            elif methodStr == "FILENAME":
                return MediaDateProcessRule.FILENAME
            elif methodStr == "FILEDATE":
                return MediaDateProcessRule.FILEDATE

        return None

    def ReadConfig (self, cfgFile):
        if not os.path.exists (cfgFile):
            return False

        xParser = XMLParser ()

        xmldom = xParser.ParseFile (cfgFile)
        cfgroot = xParser.getFirstNode (xmldom, "config")

        if cfgroot is None:
            return False

        cfgNodeList = xParser.getSpeicNodeList (cfgroot, "name")

        for cfgNode in cfgNodeList:
            cfgID = xParser.getNodeAttribValue (cfgNode, "id")
            if cfgID is None:
                continue

            cfg = MTCfgData ()
            cfg.id = cfgID
            cfg.cmd_head = xParser.GetXmlNodeValue (cfgNode, "output/head", "")
            cfg.cmd_body_single = xParser.GetXmlNodeValue (cfgNode, "output/bodysingle", "")
            cfg.cmd_tail = xParser.GetXmlNodeValue (cfgNode, "output/tail", "")

            # 获取 rule 列表
            ruleNodeList = xParser.getSpeicNodeList (cfgNode, "rule")
            for ruleNode in ruleNodeList:
                typeid = xParser.getNodeAttribValue (ruleNode, "method")
                if typeid is None or len (typeid) <= 0:
                    continue

                rule = MTCfgData.Rule ()
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

                cfg.AddRule (rule)

            self.__CfgList[cfgID] = cfg
        
        return self.__CfgList

    def GetConfig (self, cfgID):
        if cfgID in self.__CfgList.keys ():
            return self.__CfgList[cfgID]
        return None
