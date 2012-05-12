#! /usr/bin/env python
# -*- coding: utf-8 -*-

from XMLUtility import XMLParser
import os

class MTCfgData (object):
    def __init__ (self):
        self.id              = ""
        self.cmd_head        = ""
        self.cmd_body_single = ""
        self.cmd_tail        = ""


class MTConfig (object):
    def __init__ (self):
        self.__CfgList = {}

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
            id = xParser.getNodeAttribValue (cfgNode, "id")
            if id is None:
                continue

            cfg = MTCfgData ()
            cfg.id = id
            cfg.cmd_head = xParser.getSpeicNodeText (cfgNode, "output/head")
            cfg.cmd_body_single = xParser.getSpeicNodeText (cfgNode, "output/bodysingle")
            cfg.cmd_tail = xParser.getSpeicNodeText (cfgNode, "output/tail")

            self.__CfgList[id.lower ()] = cfg
        
        return self.__CfgList

    def GetConfig (self, cfgID):
        cfgID = cfgID.lower ()
        if cfgID in self.__CfgList.keys ():
            return self.__CfgList[cfgID]
        return None
