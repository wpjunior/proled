# -*- coding: iso-8859-1 -*-

"""
from OFS.SimpleItem import SimpleItem
from Globals import Persistent
from Acquisition import Implicit
"""
from OFS.OrderedFolder import OrderedFolder
from Products.ZCatalog.CatalogAwareness import CatalogAware
from OFS.ObjectManager import ObjectManager
from OFS.PropertyManager import PropertyManager
import string

def StrDocDef_addForm(self, REQUEST):
    "HTML para adicionar um novo objeto StrDocDef"
    return """
<HTML>
<HEAD><TITLE>Add StructuredDocumentDefinition</TITLE></HEAD>
<BODY BGCOLOR="#FFFFFF" LINK="#000099" VLINK="#555555">
<H2>Add StructuredDocumentDefinition</H2>
<form action="StrDocDef_add"><table>
<tr><th>Id</th>
    <td><input type=text name=id></td>
</tr>
<tr><th>XML Namespace Prefix</th>
    <td><input type=text name=xmlns_prefix></td>
</tr>
<tr><td></td><td><input type=submit value=" Add "></td></tr>
</table></form>
</body></html>
"""

def StrDocDef_add(self,REQUEST):
    "Método para adicionar um objeto StrDocDef"
    instance = StrDocDef(REQUEST)
    instance.reindex_object()
    self._setObject(REQUEST.id,instance)
    instance=getattr(self.this(),REQUEST.id)
    instance.manage_editProperties(REQUEST)
    REQUEST.RESPONSE.redirect(instance.aq_parent.absolute_url() + '/manage_main')
    #   return instance

# ------------------------------------------------------------------------------
# CLASS DEFINITION
# ------------------------------------------------------------------------------
class StrDocDef(OrderedFolder,CatalogAware,ObjectManager,PropertyManager):
    "Classe de definição (modelo) de documentos estruturados"
    meta_type = 'SDE-Template'
    filtered_meta_types = []
    __tEmPtYPe = {'product': 'StructuredDoc', 'name': 'SDE-Template-Element', 'permission': 'Add StrDocElementDefinitions', 'interfaces': [], 'visibility': 'Global', 'instance': None, 'action': 'manage_addProduct/StructuredDoc/StrDocElemDef_addForm', 'container_filter': None}
    filtered_meta_types.append(__tEmPtYPe)
    __tEmPtYPe = {'product': 'StructuredDoc', 'name': 'SDE-Template-Link', 'permission': 'Add StrDocElemDefLinks', 'interfaces': [], 'visibility': 'Global', 'instance': None, 'action': 'manage_addProduct/StructuredDoc/StrDocElemDefLink_addForm', 'container_filter': None}
    filtered_meta_types.append(__tEmPtYPe)

    def __init__(self,REQUEST):
        self.id = REQUEST.id
        self._setProperty("xmlns_prefix",'')
        self._setProperty("xml_tag",'')
        self._setProperty("default_xslt_for_html",'')
        self._setProperty("default_xslt_for_editor",'')

# ------------------------------------------------------------------------------
# PRIVATE METHODS
# ------------------------------------------------------------------------------
    # *** getDefElement
    def getDefElement(self,subtree,obj=''):
        if obj:
            self=obj
        if subtree == []:
            return self
        else:
            child_id = subtree.pop(0)
            child = self.restrictedTraverse(child_id)
            if child.meta_type == "SDE-Template-Link":
                child = child.restrictedTraverse(child.link_to)
            return child.getDefElement(subtree=subtree,obj=child)

    # *** possibleChild
    def possibleChild(self,obj=''):
        if obj:
            self=obj
        chd=[]
        pos=0
        for x in self.objectValues(['SDE-Template-Element','SDE-Template-Link']):
            elm=[]
            elm.append (x.id)
            elm.append (x.isOptional())
            elm.append (x.isMultiple())
            elm.append (pos)
            elm.append (x.exclusivity_group)
            elm.append (x.name())
            chd.append (elm)
            pos = pos + 1
        return chd

    # *** xmlTag
    def xmlTag(self):
        if self.xml_tag == "":
            return string.lower(self.id)
        else:
            return self.xml_tag

# ------------------------------------------------------------------------------
# PUBLIC METHODS
# ------------------------------------------------------------------------------
    # *** renderXSD
    def renderXSD(self,indent=""):
        """ renderXSD - Returns a XML-Schema file representing the Template """
        tag = self.xmlTag()
        group_open = -1
        shift = "   "
        printed=""
        printed+= "%s<?xml version=\"1.0\" ?>\n" % indent
        printed+= "%s<xs:schema xmlns:xs=\"http://www.w3.org/2001/XMLSchema\"\n" % indent
        printed+= "%s           targetNamespace=\"/XSD/%s\"\n" % (indent,self.id)
        printed+= "%s           xmlns=\"/XSD/%s\"\n" % (indent,self.id)
        printed+= "%s           elementFormDefault=\"qualified\">\n" % indent
        printed+= "%s   <xs:element name=\"%s\">\n" % (indent,tag)
        printed+= "%s      <xs:complexType>\n" % indent
        printed+= "%s         <xs:sequence>\n" % indent

        subtree = self.objectValues(["SDE-Template-Element","SDE-Template-Link"])

        if len(subtree) > 0:
            for x in subtree:
                if x.exclusivity_group != group_open:
                    if group_open != -1:
                        printed+= "%s            </xs:choice>\n" % indent
                        shift = shift[0:-3]
                    printed+= "%s            <xs:choice>\n" % indent
                    group_open = x.exclusivity_group
                    shift = shift + "   "
                if x.isOptional():
                    minOccurs = "0"
                else:
                    minOccurs = "1"
                if x.isMultiple():
                    maxOccurs = "unbounded"
                else:
                    maxOccurs = "1"
                tag_x = x.xmlTag()
                printed+= "%s         <xs:element name=\"%s\" type=\"%sType\" minOccurs=\"%s\" maxOccurs=\"%s\"/>\n" % (indent+shift,tag_x,tag_x,minOccurs,maxOccurs)
            if group_open != -1:
                printed+= "%s            </xs:choice>\n" % indent
                group_open = -1
                shift = shift[0:-3]
        printed+= "%s         </xs:sequence>\n" % indent
        printed+= "%s         <xs:attribute name=\"id\" type=\"xs:string\" />\n" % indent
        printed+= "%s      </xs:complexType>\n" % indent
        printed+= "%s   </xs:element>\n" % indent

        subtree = self.objectValues("SDE-Template-Element")
        for x in subtree:
            printed+= x.renderXSD(indent+"   ")
        printed+= "%s</xs:schema>\n" % indent
        self.REQUEST.RESPONSE.setHeader('Content-type', 'text/xml')
        return printed
