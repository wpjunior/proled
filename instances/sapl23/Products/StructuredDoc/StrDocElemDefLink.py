# -*- coding: iso-8859-1 -*-

from OFS.OrderedFolder import OrderedFolder
from Products.ZCatalog.CatalogAwareness import CatalogAware
from OFS.ObjectManager import ObjectManager
from OFS.PropertyManager import PropertyManager
import string

def StrDocElemDefLink_addForm(self, REQUEST):
    "HTML para adicionar um novo objeto StrDocElemDefLink"
    return """
<HTML>
<HEAD><TITLE>Add StrDocElemDefLink</TITLE></HEAD>
<BODY BGCOLOR="#FFFFFF" LINK="#000099" VLINK="#555555">
<H2>Add StrDocElemDefLink</H2>
<form action="StrDocElemDefLink_add"><table>
<tr><th>Id</th>
    <td><input type=text name=id></td>
</tr>
<tr><td></td><td><input type=submit value=" Add "></td></tr>
</table></form>
</body></html>
"""

def StrDocElemDefLink_add(self,REQUEST):
    "Método de adição de objetos StrDocElemDefLink"
    request = REQUEST
    instance = StrDocElemDefLink(request)
    instance.reindex_object()
    self._setObject(request.id,instance)
    instance=getattr(self.this(),request.id)
    REQUEST.RESPONSE.redirect(instance.aq_parent.absolute_url() + '/manage_main')

class StrDocElemDefLink(OrderedFolder,CatalogAware,ObjectManager,PropertyManager):
    "Classe de Link para definição de elementos de documentos estruturados"
    meta_type="SDE-Template-Link"
    filtered_meta_types = []
    def __init__(self,REQUEST):
        self.id = REQUEST.id
        self.manage_addProperty('link_to','','string')
        self.manage_addProperty('optional','','boolean')
        self.manage_addProperty('multiple','','boolean')
        self.manage_addProperty('exclusivity_group','-1','int')

    # *** isMultiple
    def isMultiple(self):
        return self.multiple

    # *** isOptional
    def isOptional(self):
        return self.optional

    # *** name
    def name(self):
        return self.restrictedTraverse(self.link_to).name()

    # *** possibleChild
    def possibleChild (self):
        return self.restrictedTraverse(self.link_to).possibleChild()

    # *** xmlTag
    def xmlTag(self):
        original = self.restrictedTraverse(self.link_to)
        xmltag = original.xmlTag()
        if xmltag == "":
            return string.lower(original.id)
        else:
            return xmltag
