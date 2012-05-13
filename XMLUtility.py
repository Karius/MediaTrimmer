# -*- coding: gbk -*-

from xml.dom.minidom import parse, parseString
from xml.dom.minidom import getDOMImplementation

# 根据 sstr 的内容来返回其内容是 True 还是 False
# sstr 可以是 int 数字类型或者是字符串类型，ANSI 和 Unicode 字符串均可，不区分大小写
# 比如 sstr = "0" or sstr = 0 or sstr = "False" or sstr = "false" or sstr = "disable" or sstr = "disable" 本函数均返回 False
# sstr = "1" or sstr = 1 or sstr = "True" or sstr = "true" or sstr = "Enable" or sstr = "enable" 本函数均返回 True
# defV 为默认值
def Str2Bool (sstr, defV = None):
    if defV is None:
        defV = False

    result = False
    if sstr is None:
        result = defV
    elif isinstance (sstr, int):
        result = (sstr != 0)
    elif isinstance (sstr, str):
        lstr = sstr.lower ().strip ()
        if lstr == "true" or lstr == "enable":
            result = True
        elif lstr == "false" or lstr == "disable":
            result = False
        else:
            try:
                if int (lstr) > 0:
                    result = True
            except:
                pass
    return result


class XMLParser:
    # 解析 XML 文件，并返回 XMLDOM
    def ParseFile (self, fname):
        xmlDom = None
        try:
            xmlDom = parse (fname)
        except :
            pass
        return xmlDom

    # 解析 XML 字符串，并返回 XMLDOM
    def ParseString (self, xmlStr):
        xmlDom = None
        try:
            xmlDom = parseString (xmlStr)
        except :
            pass
        return xmlDom

    # 取得指定节点的属性列表
    def getNodeAttribList (self, node):
        return node.attributes

    # 取得指定节点的属性
    def getNodeAttrib (self, node, attrName):
        attrList = self.getNodeAttribList (node)
        if attrList is None:
            return None
        if attrName in attrList.keys ():
            return attrList[attrName]
        return None

    # 取得节点属性名
    def getNodeAttribValue (self, node, attrName):
        attr = self.getNodeAttrib (node, attrName)
        if attr is None:
            return None
        return attr.value

    # 取得属性值
    def getAttribValue (self, attr):
        return attr.value


    # 快速取得指定节点的属性列表
    def getSpeicNodeAttribList (self, parentNode, nodeName):
        node = self.getSpeicNode (parentNode, nodeName)
        return node.attributes

    # 快速取得指定节点的属性
    def getSpeicNodeAttrib (self, parentNode, nodeName, attrName):
        attrList = self.getSpeicNodeAttribList (parentNode, nodeName)
        if attrList is None:
            return None
        if attrName in attrList.keys ():
            return attrList[attrName]
        return None

    # 快速取得指定节点的属性值
    def getSpeicNodeAttribValue (self, parentNode, nodeName, attrName):
        attrList = self.getSpeicNodeAttribList (parentNode, nodeName)
        if attrList is None:
            return None
        if attrName in attrList.keys ():
            return attrList[attrName].value  # Or: attrList[attrName].name
        return None


    # 快速取得指定节点列表
    def getSpeicNodeList (self, parentNode, nodeName):
        nodeTree = nodeName.split ("/")
        nodeName = nodeTree.pop ()

        for childNodeName in nodeTree:
            parentNode = self.getFirstNode (parentNode, childNodeName)
            if parentNode is None:
                return []
        #return parentNode.getElementsByTagName (nodeName)
        return self.getChildNodeList (parentNode, nodeName)


    # 快速获得指定节点
    def getSpeicNode (self, parentNode, nodeName):
        nodeTree = nodeName.split ("/")
        for childNodeName in nodeTree:
            # print childNodeName
            parentNode = self.getFirstNode (parentNode, childNodeName)
            # print parentNode
            if parentNode is None:
                return None
        return parentNode

    # 快速获得指定节点的文本内容
    def getSpeicNodeText (self, parentNode, nodeName, defaultText = None):
        chNode = self.getSpeicNode (parentNode, nodeName)
        if chNode is None:
            if defaultText is None:
                defaultText = ''
            return defaultText
        return self.getNodeText (chNode)


    # 获取指定节点的首个子节点
    # def getFirstNode (self, xdom, name):
    #     elementList = xdom.getElementsByTagName(name) # 如果子节点的子节点有符合这个 name 的，则 getElementsByTagName 会取得子节点的子节点，这不是我们所希望的
    #     if len (elementList) > 0:
    #         return elementList[0]
    #     return None
    def getFirstNode (self, xdom, name):
        for node in xdom.childNodes:
            if node.nodeType == node.ELEMENT_NODE and node.nodeName == name:
                return node
        return None

    # 取名字相符的全部子节点（节点列表）
    def getChildNodeList (self, xdom, name):
        nodeList = []
        for node in xdom.childNodes:
            if node.nodeType == node.ELEMENT_NODE and node.nodeName == name:
                nodeList.append (node)
        return nodeList

    # 获取节点的文本内容
    def getNodeText (self, node, defVal = None):
        if node is None:
            return defVal
        for childNode in node.childNodes:
            if childNode.nodeType in (node.TEXT_NODE, node.CDATA_SECTION_NODE):
                return childNode.data
        return defVal

    # 一些更高层次的工具函数
    # parentNode : 父节点
    # nodeName   : 要取的节点名称，支持树节点
    # attrName   : 要取的属性名称
    # defVal     : 默认值，当索取属性不存在时返回的值
    # nulStrRetDefVal : 当取得属性虽然存在，但其值内容却是 "" 这样的空字符串时是否需要返回 defVal，默认为是
    def GetXmlAttrValue (self, parentNode, nodeName, attrName, defVal, nulStrRetDefVal = None):
        x = XMLParser ()
        val = x.getSpeicNodeAttribValue (userNode, nodeName, attrName)
        if val is None:
            return defval
        if nulStrRetDefVal is None:
            nulStrRetDefVal = True
        if nulStrRetDefVal and val == '':
            return defVal
        return val

    # parentNode : 父节点
    # nodeName   : 要取的节点名称，支持树节点
    # defVal     : 默认值，当索取属性不存在时返回的值
    # nulStrRetDefVal : 当取得节点虽然存在，但其值内容却是 "" 这样的空字符串时是否需要返回 defVal，默认为是
    def GetXmlNodeValue (self, parentNode, nodeName, defVal, nulStrRetDefVal = None):
        x = XMLParser ()
        val = x.getSpeicNodeText (parentNode, nodeName)
        if val is None:
            return defVal
        if nulStrRetDefVal is None:
            nulStrRetDefVal = True
        if nulStrRetDefVal and val == '':
            return defVal
        return val

    # parentNode : 父节点
    # nodeName   : 要取的节点名称，支持树节点
    # defVal     : 默认值，int 类型，当索取属性不存在时返回的值
    def GetXmlNodeValueInt (self, parentNode, nodeName, defVal):
        # 最后一个参数为 True 表明：如果节点不存在或节点内容为 "" 这样的空字符串，将返回 None
        retVal = self.GetXmlNodeValue (parentNode, nodeName, None, True)
        if retVal is None:
            return defVal
        try:
            return int (retVal)
        except:  # ValueError
            return defVal

    # parentNode : 父节点
    # nodeName   : 要取的节点名称，支持树节点
    # defVal     : 默认值，Float 类型，当索取属性不存在时返回的值
    def GetXmlNodeValueFloat (self, parentNode, nodeName, defVal):
        # 最后一个参数为 True 表明：如果节点不存在或节点内容为 "" 这样的空字符串，将返回 None
        retVal = self.GetXmlNodeValue (parentNode, nodeName, None, True)
        if retVal is None:
            return defVal
        try:
            return float (retVal)
        except:  # ValueError
            return defVal

    # parentNode : 父节点
    # nodeName   : 要取的节点名称，支持树节点
    # defVal     : 默认值，Bool 类型，当索取属性不存在时返回的值
    def GetXmlNodeValueBool (self, parentNode, nodeName, defVal):
        # 最后一个参数为 True 表明：如果节点不存在或节点内容为 "" 这样的空字符串，将返回 None
        retVal = self.GetXmlNodeValue (parentNode, nodeName, None, True)
        if retVal is None:
            return defVal
        return Str2Bool (retVal, defVal)

    # parentNode : 父节点
    # nodeName   : 要取的节点名称，支持树节点
    # defVal     : 默认值，list 类型，当索取属性不存在时返回的值
    # sep        : 字符串间隔符号，默认为 ";"
    def GetXmlNodeValueList (self, parentNode, nodeName, defVal, sep = None):
        # 最后一个参数为 True 表明：如果节点不存在或节点内容为 "" 这样的空字符串，将返回 None
        retVal = self.GetXmlNodeValue (parentNode, nodeName, None, True)
        if retVal is None:
            return defVal
        try:
            if sep is None:
                sep = ";"
            return retVal.split (sep)
        except:  # ValueError
            return defVal


class XMLCreater:
    def __init__ (self):
        self.__impl = getDOMImplementation()

    # 创建 XML Document
    def createDocument (self, rootTag):
        return self.__impl.createDocument(None, rootTag, None)

    # 取得 XML 文档根节点
    def getDocumentRoot (self, xDoc):
        return xDoc.documentElement

    # # 在父节点下插入一个空子节点
    # def insertNode (self, xDoc, parentNode, nodeName):
    #     childNode = xDoc.createElement (nodeName)
    #     if childNode is not None:
    #         parentNode.appendChild (childNode)
    #     return childNode

    # 根据指定的节点名在父节点下插入一个空节点
    def insertSpeicNode (self, xDoc, parentNode, nodeName):
        x = XMLParser ()

        nodeNameList = nodeName.split ("/")
        textParentNodeName = nodeNameList.pop ()

        for childNodeName in nodeNameList:
            childNode = x.getSpeicNode (parentNode, childNodeName)
            if childNode is None:
                newChildNode = xDoc.createElement (childNodeName)
                parentNode.appendChild (newChildNode)
                parentNode = newChildNode
                #parentNode = self.insertNode (xDoc, parentNode, childNodeName)
            else:
                parentNode = childNode

        newTextNode = xDoc.createElement (textParentNodeName)
        parentNode.appendChild (newTextNode)
        return newTextNode

    # 在节点中插入文本值
    def insertNodeText (self, xDoc, node, value, type = 'text'):
        if value.find (']]>') > -1:
            type = 'text'
        if type == 'cdata':
            textNode = xDoc.createCDATASection (value)
        else:
            textNode = xDoc.createTextNode (value)
        node.appendChild (textNode)
        return node

    # def insertSpeicNodeText (self, nodeName, value, type = 'text'):
    #     if value.find (']]>') > -1:
    #         type = 'text'
    #     if type == 'cdata':
    #         textNode = self.__xDoc.createCDATASection (value)
    #     else:
    #         textNode = self.__xDoc.createTextNode (value)
    #     newTextNode = self.insertSpeicNode (nodeName)
    #     newTextNode.appendChild (textNode)
    #     return newTextNode

    # 根据指定的节点名插入一个文本节点
    def insertSpeicNodeText (self, xDoc, parentNode, nodeName, value, type = 'text'):
        newTextNode = self.insertSpeicNode (xDoc, parentNode, nodeName)
        self.insertNodeText (xDoc, newTextNode, value, type)
        return newTextNode
    
    # # 在父节点下插入一个子文本节点
    # def insertChildNodeText (self, xDoc, parentNode, name, value, type = 'text'):
    #     childNode = self.insertNode (xDoc, parentNode, name)
    #     return self.insertNodeText (xDoc, childNode, value, type)

    def toSimpleString (self, xDoc, encoding = None):
        if encoding is None:
            encoding = "utf-8"
        return xDoc.toxml (encoding)

    def toString (self, xDoc, indent = None, newl = None, encoding = None):
        if indent is None:
            indent = ''
        if newl is None:
            newl = '\n'
        if encoding is None:
            encoding = "utf-8"
        return xDoc.toprettyxml (indent, newl, encoding)

    def toFile (self, xDoc, fname, indent = None, addindent = None, newl = None, encoding = None):
        if indent is None:
            indent = ''
        if addindent is None:
            addindent = ''
        if newl is None:
            newl = '\n'
        if encoding is None:
            encoding = "utf-8"
        f = file (fname, 'w')
        import codecs
        writer = codecs.lookup('utf-8')[3](f)
        xDoc.writexml (writer, indent, addindent, newl, encoding)
        writer.close ()        


    def Indent (self, dom, node, indent = 0):
        # Copy child list because it will change soon
        children = node.childNodes[:]
        # Main node doesn't need to be indented
        if indent:
            text = dom.createTextNode ('\n' + '  ' * indent)
            node.parentNode.insertBefore(text, node)
        if children:
            # Append newline after last child, except for text nodes
            if children[-1].nodeType == node.ELEMENT_NODE:
                text = dom.createTextNode('\n' + '  ' * indent)
                node.appendChild(text)
            # Indent children which are elements
            for n in children:
                if n.nodeType == node.ELEMENT_NODE:
                    self.Indent(dom, n, indent + 1)

    def toFilePretty (self, xDoc, fname, encoding = None):
        domcopy = xDoc.cloneNode (True)
        self.Indent(domcopy, domcopy.documentElement)
        f = file(fname, 'wb')
        import codecs
        writer = codecs.lookup('utf-8')[3](f)
        domcopy.writexml(writer, encoding = 'utf-8')
        domcopy.unlink()

def parserTest ():
    xstr = "<conf><menu><shake>1</shake></menu><shake>2</shake></conf>"
    
    x = XMLParser ()
    mdom = x.ParseString (xstr)
    root = x.getFirstNode (mdom, "conf")
    print x.getSpeicNodeText (root, "shake")
    print x.getSpeicNodeList (root, "shake")

def parserTest2 ():
    xstr = "<conf><menu><shake>1</shake></menu><shake>2</shake></conf>"
    
    x = XMLParser ()
    xdom = x.ParseFile ('Fishes.xml')
    root = x.getFirstNode (xdom, "Fishes")

    fishNodeList = x.getSpeicNodeList (root, "Fish")
    for fishNode in fishNodeList:
        print x.getSpeicNodeText (fishNode, "ID"), x.getSpeicNodeText (fishNode, "Name")

def createrTest ():
    # x = XMLCreater ('data')
    # #print x.toString ()
    # x.insertSpeicNode ("common/main")
    # x.insertSpeicNodeText ("common/cookies", "fdas")
    # x.insertSpeicNodeText ("user", "testuser & <")
    # x.insertSpeicNodeText ("user", "testuser & <")
    # # x.toFile ("1.xml", '', '')
    # x.toFilePretty ("1.xml")
    x = XMLCreater ()
    #print x.toString ()
    xDoc = x.createDocument ("data")
    root = x.getDocumentRoot (xDoc)

    x.insertSpeicNode (xDoc, root, "common/main")
    x.insertSpeicNodeText (xDoc, root, "common/cookies", "fdas")
    x.insertSpeicNodeText (xDoc, root, "user", "testuser & <")
    x.insertSpeicNodeText (xDoc, root, "user", "testuser & <")
    # x.toFile ("1.xml", '', '')
    x.toFilePretty (xDoc, "1.xml")


def attribTest ():
    x = XMLParser ()
    mdom = x.ParseFile ("kxcfg.xml")
    root = x.getFirstNode (mdom, "data")

    #print x.getSpeicNodeAttribList (root, "user/module/fishpond/buy/enforceid").keys ()
    print x.getSpeicNodeAttribValue (root, "user/module/fishpond/buy/enforceid", "enable")

if __name__ == '__main__':
    createrTest ()
    #attribTest ()
    #parserTest2 ()
