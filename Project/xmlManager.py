#초단기실황조회

from xml.dom.minidom import parse, parseString
from xml.etree import ElementTree


xmlFD = -1

#### xml 관련 함수 구현
def LoadXMLFromFile():
    fileName = str(input ("please input file name to load :"))
    global xmlFD, xml_Doc
    try:
        xmlFD = open(fileName, 'r', encoding = 'UTF-8')
    except IOError:
        print ("invalid file name or path")
    else:
        try:
            dom = parse(xmlFD)
        except Exception:
            print ("loading fail!!!")
        else:
            print ("XML Document loading complete")
            xml_Doc = dom
            return dom
    return None

def PrintDomtoXML():
    if checkDocument():
        print(xml_Doc.toxml())



def checkDocument():
    global xml_Doc
    if xml_Doc == None:
        print ("Error : Document is empty")
        return False
    return True