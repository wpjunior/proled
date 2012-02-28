# -*- coding: iso-8859-1 -*-

from Products.ZCatalog.CatalogAwareness import CatalogAware
from OFS.ObjectManager import ObjectManager
from OFS.PropertyManager import PropertyManager
from OFS.SimpleItem import SimpleItem

def StrDocAttrDef_addForm(self, REQUEST):
    "HTML para adicionar um novo objeto StrDocAttrDef"
    return """
<HTML>
<HEAD><TITLE>Add StrDocAttrDef</TITLE></HEAD>
<BODY BGCOLOR="#FFFFFF" LINK="#000099" VLINK="#555555">
<H2>Add StrDocAttrDef</H2>
<form action="StrDocAttrDef_add"><table>
<tr><th>Id</th>
    <td><input type=text name=id></td>
</tr>
<tr><td></td><td><input type=submit value=" Add "></td></tr>
</table></form>
</body></html>
"""

def StrDocAttrDef_add(self,REQUEST):
    "Método de adição de objetos StrDocAttrDef"
    request = REQUEST
    instance = StrDocAttrDef(request)
    instance.reindex_object()
    self._setObject(request.id,instance)
    instance=getattr(self.this(),request.id)
    instance.manage_editProperties(request)
    REQUEST.RESPONSE.redirect(instance.aq_parent.absolute_url() + '/manage_main')
    #   return instance

class StrDocAttrDef(CatalogAware,PropertyManager,ObjectManager):
    "Classe de definição de atributos de documentos estruturados"
    meta_type="SDE-Template-Attribute"
    def __init__(self,REQUEST):
        self.lista_xsd_type=('anySimpleType','anyURI','base64Binary','boolean','byte','date','dateTime',
                             'decimal','double','duration','ENTITIES','ENTITY','float','gDay','gMonth',
                             'gMonthDay','gYear','gYearMonth','hexBinary','ID','IDREF','IDREFS','int',
                             'integer','language','long','Name','NCName','negativeInteger','NMTOKEN',
                             'NMTOKENS','nonNegativeInteger','nonPositiveInteger','normalizedString',
                             'NOTATION','positiveInteger','QName','short','string','time','token',
                             'unsignedByte','unsignedInt','unsignedLong','unsignedShort')
        self.lista_xsd_use = ('optional','required','prohibited')
        self.id = REQUEST.id
        self.manage_addProperty('xsd_type','lista_xsd_type','selection')
        self.manage_addProperty('xsd_use','lista_xsd_use','selection')
        self.manage_addProperty('xsd_default','','string')
        self.manage_addProperty('xsd_fixed','','string')
        self.manage_addProperty('attribute_name','','string')

    def name(self):
        if self.attribute_name:
            return self.attribute_name
        else:
            return self.id
