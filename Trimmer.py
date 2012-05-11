#! /usr/bin/env python
# -*- coding: utf-8 -*-


from FileLocation import FileLocationManager
from DateInfoParse import MediaDateProcessRule




if __name__ == "__main__":
    tl = (MediaDateProcessRule (["jpg", "raw", "crw", "cr2", "rw2", "nef", "nrw", "arw", "srf", "sr2", "pef", "ptx", "srw"]), \
          MediaDateProcessRule (["avi", "mov"], "thm", MediaDateProcessRule.PF_FOLLOWMAIN or MediaDateProcessRule.PF_GETINFO), \
          MediaDateProcessRule (["m2ts"], "modd", MediaDateProcessRule.PF_GETINFO), \
          MediaDateProcessRule (["mts"]), \
          MediaDateProcessRule (["m4v", "mp4"]) \
          )
