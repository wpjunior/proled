from Products.StructuredDoc import StrDoc
from Products.StructuredDoc import StrDocElem
from Products.StructuredDoc import StrDocDef
from Products.StructuredDoc import StrDocElemDef
from Products.StructuredDoc import StrDocAttrDef
from Products.StructuredDoc import StrDocElemDefLink

def initialize (context):
  context.registerClass(StrDoc.StrDoc,
                        constructors=(StrDoc.StrDoc_addForm,StrDoc.StrDoc_add),
                        icon='Icons/StrDocImage.gif')
  context.registerClass(StrDocElem.StrDocElem,
                        constructors=(StrDocElem.StrDocElem_addForm,StrDocElem.StrDocElem_add),
                        icon='Icons/StrDocElemImage.gif')
  context.registerClass(StrDocDef.StrDocDef,
                        constructors=(StrDocDef.StrDocDef_addForm,StrDocDef.StrDocDef_add),
                        icon='Icons/StrDocDefImage.gif')
  context.registerClass(StrDocElemDef.StrDocElemDef,
                        constructors=(StrDocElemDef.StrDocElemDef_addForm,StrDocElemDef.StrDocElemDef_add),
                        icon='Icons/StrDocElemDefImage.gif')
  context.registerClass(StrDocAttrDef.StrDocAttrDef,
                        constructors=(StrDocAttrDef.StrDocAttrDef_addForm,StrDocAttrDef.StrDocAttrDef_add),
                        icon='Icons/StrDocAttrDefImage.gif')
  context.registerClass(StrDocElemDefLink.StrDocElemDefLink,
                        constructors=(StrDocElemDefLink.StrDocElemDefLink_addForm,
                                      StrDocElemDefLink.StrDocElemDefLink_add),
                        icon='Icons/StrDocElemDefLinkImage.gif')
