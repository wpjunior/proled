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

def StrDocElemDef_addForm(self, REQUEST):
    "HTML para adicionar um novo objeto StrDocElemDef"
    return """
<HTML>
<HEAD><TITLE>Add StrDocElementDefinition</TITLE></HEAD>
<BODY BGCOLOR="#FFFFFF" LINK="#000099" VLINK="#555555">
<H2>Add StrDocElementDefinition</H2>
<form action="StrDocElemDef_add"><table>
<tr><th>Id</th>
    <td><input type=text name=id></td>
</tr>
<tr><td></td><td><input type=submit value=" Add "></td></tr>
</table></form>
</body></html>
"""

def StrDocElemDef_add(self,REQUEST):
    "Método para adicionar um objeto StrDocElemDef"
    instance = StrDocElemDef(REQUEST)
    instance.reindex_object()
    self._setObject(REQUEST.id,instance)
    instance=getattr(self.this(),REQUEST.id)
    REQUEST.RESPONSE.redirect(instance.aq_parent.absolute_url() + '/manage_main')

# ------------------------------------------------------------------------------
# CLASS DEFINITION
# ------------------------------------------------------------------------------
class StrDocElemDef(OrderedFolder,CatalogAware,ObjectManager,PropertyManager):
    "Classe de definição de elementos de documentos estruturados"
    meta_type = 'SDE-Template-Element'

    filtered_meta_types = []
    __tEmPtYPe = {'product': 'StructuredDoc', 'name': 'SDE-Template-Element', 'permission': 'Add StrDocElementDefinitions', 'interfaces': [], 'visibility': 'Global', 'instance': None, 'action': 'manage_addProduct/StructuredDoc/StrDocElemDef_addForm', 'container_filter': None}
    filtered_meta_types.append(__tEmPtYPe)
    __tEmPtYPe = {'product': 'StructuredDoc', 'name': 'SDE-Template-Attribute', 'permission': 'Add StrDocAttrDefs', 'interfaces': [], 'visibility': 'Global', 'instance': None, 'action': 'manage_addProduct/StructuredDoc/StrDocAttrDef_addForm', 'container_filter': None}
    filtered_meta_types.append(__tEmPtYPe)
    __tEmPtYPe = {'product': 'StructuredDoc', 'name': 'SDE-Template-Link', 'permission': 'Add StrDocElemDefLinks', 'interfaces': [], 'visibility': 'Global', 'instance': None, 'action': 'manage_addProduct/StructuredDoc/StrDocElemDefLink_addForm', 'container_filter': None}
    filtered_meta_types.append(__tEmPtYPe)
    __tEmPtYPe = {'product': 'PythonScripts', 'name': 'Script (Python)', 'permission': 'Add Python Scripts', 'interfaces': [], 'visibility': 'Global', 'instance': None, 'action': 'manage_addProduct/PythonScripts/pyScriptAdd', 'container_filter': None}
    filtered_meta_types.append(__tEmPtYPe)
    del(__tEmPtYPe)

    def __init__(self,REQUEST):
        self.id = REQUEST.id
        self.manage_addProperty('initial_text','','text')
        self.manage_addProperty('optional','','boolean')
        self.manage_addProperty('multiple','','boolean')
        self.manage_addProperty('has_own_value','1','boolean')
        self.manage_addProperty('exclusivity_group','-1','int')
        self.manage_addProperty('xml_tag','','string')
        self.manage_addProperty('element_name','','string')

# ------------------------------------------------------------------------------
# PRIVATE METHODS
# ------------------------------------------------------------------------------
    # *** isMultiple
    def isMultiple(self):
        return self.multiple

    # *** isOptional
    def isOptional(self):
        return self.optional

    # *** name
    def name(self):
        if self.element_name:
            return self.element_name
        else:
            return self.id

    # *** renderXSD
    def renderXSD(self,indent=""):
        tag = self.xmlTag()
        group_open = -1
        shift = "   "
        printed=""
        printed+= "%s<xs:complexType name=\"%sType\">\n" % (indent,tag)
        printed+= "%s   <xs:sequence>\n" % indent
        if self.has_own_value:
            printed+= "%s      <xs:element name=\"%s_text\" type=\"xs:string\" />\n" % (indent,tag)
        subtree = self.objectValues(["SDE-Template-Element","SDE-Template-Link"])
        if len(subtree) > 0:
            for x in subtree:
                if x.exclusivity_group != group_open:
                    if group_open != -1:
                        printed+= "%s      </xs:choice>\n" % indent
                        shift = shift[0:-3]
                    printed+= "%s      <xs:choice>\n" % indent
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
                printed+= "%s      <xs:element name=\"%s\" type=\"%sType\" minOccurs=\"%s\" maxOccurs=\"%s\"/>\n" % (indent+shift,tag_x,tag_x,minOccurs,maxOccurs)
            if group_open != -1:
                printed+= "%s      </xs:choice>\n" % indent
                group_open = -1
                shift = shift[0:-3]
        printed+= "%s   </xs:sequence>\n" % indent
        printed+= "%s   <xs:attribute name=\"id\" type=\"xs:string\" />\n" % indent
        for a in self.objectValues('SDE-Template-Attribute'):
            printed+= '%s   <xs:attribute name="%s" type="xs:%s" />\n' % (indent,  a.id, a.xsd_type)
        printed+= "%s</xs:complexType>\n" % indent
        subtree = self.objectValues("SDE-Template-Element")
        for x in subtree:
            printed+= x.renderXSD(indent)
        return printed

    # *** xmlTag
    def xmlTag(self):
        if self.xml_tag == "":
            return string.lower(self.id)
        else:
            return self.xml_tag

