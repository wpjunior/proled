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

def StrDocElem_addForm(self, REQUEST):
    "HTML para adicionar um novo objeto StrDocElem"
    return """
<HTML>
<HEAD><TITLE>Add StrDocElement</TITLE></HEAD>
<BODY BGCOLOR="#FFFFFF" LINK="#000099" VLINK="#555555">
<H2>Add StrDocElement</H2>
<form action="StrDocElem_add"><table>
<tr><th>Id</th>
    <td><input type=text name=id value="Automatic assignment" disabled=true></td>
</tr>
<tr><th>Type</th>
    <td><input type=text name=type></td>
</tr>
<tr><td></td><td><input type=submit value=" Add "></td></tr>
</table></form>
</body></html>
"""

def StrDocElem_add(self,REQUEST):
    "Método para adicionar um objeto StrDocElem"
    print "### DEBUG: StrDocElem_add: id do self: %s - %s" % (self.id,`self`)
    print "### DEBUG: StrDocElem_add: id do self.this(): %s - %s" % (self.this().id,`self.this()`)
    request = REQUEST
    RESPONSE =  request.RESPONSE
    temp_id = self.newElemId()
    request.set('id',temp_id)
    instance = StrDocElem(request,self.this())
    instance.reindex_object()
        
    # add the instance to the ObjectManager
    self._setObject(request.id,instance)
    instance=getattr(self.this(),request.id)
    if request.has_key('position'):
        offset = request.position
    else:
        offset = 0
    self.manage_move_objects_to_top (request, temp_id)
    if offset > 0:
        self.manage_move_objects_down (request, temp_id, offset)
    return instance

class StrDocElem(OrderedFolder,CatalogAware):
    "Classe de elementos de documentos estruturados"
    meta_type = 'SDE-Document-Element'
    filtered_meta_types = []

    def __init__(self,REQUEST,container):
        self.id = REQUEST.id
        self._setProperty("type",'')
        self._setProperty("text",'')
        if REQUEST.has_key('type'):
            self.type = REQUEST['type']
            doc=container.document()
            print "### DEBUG - __init__ - doc: %s - %s" % (doc.id, `doc`)
            defpath=container.definitionPath()+'/'+self.type
            print "### DEBUG - defpath : %s " % defpath
            defelem=doc.definitionElement(element_path=defpath)
            print "### DEBUG - defelem : %s - %s " % (defelem.id, `defelem`)
            for p in defelem.objectValues('SDE-Template-Attribute'):
                self.manage_addProperty(id='@'+p.id+'@', value='', type='string')
            if hasattr(defelem,"initial_text"):
                if defelem.initial_text != "":
                    self.text = defelem.initial_text

    # *** attributes
    def attributes(self):
        defelem = self.definitionElement(obj=self)
        attr = []
        for a in self.propertyItems():
            if ((a[0][0] == '@') and (a[0][-1] == '@')):
                attr_id = a[0][1:-1]
                try:
                    attr_name = defelem[attr_id].name()
                except:
                    attr_name = attr_id
                attr.append (list ((attr_id,a[1],attr_name)))
        return attr

    # *** definitionPath
    def definitionPath (self,absolute=0):
        return self.parent().definitionPath(absolute) + "/" + self.type

    # *** getAttribute
    def getAttribute (self,attribute=''):
        return self.getProperty('@'+attribute+'@','')

    # *** has_own_value
    def has_own_value(self):
        defelem = self.definitionElement(obj=self)
        if hasattr(defelem, "has_own_value"):
            return defelem.has_own_value
        else:
            return ""
            
    def setNewIdForChildren(self, recursive=1, obj=""):
        if obj:            
            self=obj
        for t_obj in self.objectValues():            
            OrderedFolder.manage_renameObject(self, t_obj.id, self.newElemId())
            if recursive:
                t_obj.setNewIdForChildren (recursive=recursive, obj=t_obj)

    def _get_id(self, id):
        # This is a overriding of the CopyContainer._get_id method, 
        # located in OFS/CopySupport.py
        new_id = id
        session=self.REQUEST.SESSION
        if session.has_key('SDE_clip_type'):
            if session['SDE_clip_type'] == 'COPY':
                new_id = self.newElemId()
        print "### DEBUG: _get_id: old=%s new=%s" % (id,new_id)
        return new_id
        
    # *** manage_beforeDelete (EVENT)
    def manage_beforeDelete (self, item, containeR):
        defElem = item.definitionElement(obj=item)
        if 'SDE_BeforeDelete' in defElem.objectIds('Script (Python)'):
            defElem.SDE_BeforeDelete(item)
        return
        
    # *** manage_afterAdd (EVENT)
    def manage_afterAdd (self, item, containeR):
        print "### DEBUG: AfterAdd para o item %s" % item.id
        defElem = item.definitionElement(obj=item)
        print "### DEBUG: id do defelem: %s" % defElem.id
        if 'SDE_AfterInsert' in defElem.objectIds('Script (Python)'):
            print "### DEBUG: Achou Python de evento"
            print defElem.SDE_AfterInsert(item)
        return        

    # *** manage_afterClone (EVENT)
    def manage_afterClone (self, item):
        print "### DEBUG: AfterClone para o item %s" % item.id
        session=self.REQUEST.SESSION
        if session.has_key('SDE_clip_type'):
            if session['SDE_clip_type'] == 'COPY':
                self.setNewIdForChildren(recursive=1,obj=self)
        return
#        return self.manage_afterAdd (item, containeR=None)


    # *** parent
    def parent (self):
        return self.aq_parent

    # *** render
    def render(self):
        printed = ""
        printed+= str(self.text)
        for x in (self.objectValues()):
            printed+= str(x.render())
        return printed

    # *** renderHTML
    def renderHTML(self,indent=0):
        printed = ""
        i = indent * 8
        printed+= "<div style=\"padding-left: %ipx;\">%s</div>" % (i,self.text)
        for x in (self.objectValues()):
            printed+= str(x.renderHTML(indent+4))
        printed+= "\n"
        return printed

    # *** renderHTMLforEditing
    def renderHTMLforEditing (self,indent=0,elem_id=""):
        printed =""
        i = indent * 8
        defelem = self.definitionElement(obj=self)
        attr = self.attributes()
        printed+= "<a name=\"%s\"></a>" % self.id
        if (elem_id == self.id):
            printed+= "<form method=\"post\" action=\"%s/save\">" % self.absolute_url()
            printed+= "    <p>(%s)<br>" % defelem.name()
            for a in attr:
                printed+= a[2] + ':<input type="text" size="10" name="txattr_' + a[0] + '" value="' + a[1] + '">&nbsp;&nbsp;&nbsp;'
            if self.has_own_value():
                printed+= "    <textarea name=\"textedit\" cols=\"%i\" rows=\"4\" style=\"padding-left: %ipx;\">%s</textarea><br>" % (130-indent,i,self.text)
            else:
                printed+= "    <input name=\"textedit\" type=\"hidden\" value=\"%s\">" % self.text
            printed+= "    <input name=\"cmd\" type=\"submit\" value=\"Gravar\">"
            printed+= "    <input name=\"cmd\" type=\"submit\" value=\"Excluir\">"
            printed+= "    <input type=\"reset\" value=\"Original\">"

            tmpObjs = self.possibleChild(obj=self)
            if (tmpObjs != []):
                printed+= "    <select name=\"selChild\" onChange=AddChildOnSelect('%s',this)>" % self.absolute_url()
                printed+= "        <option selected>Inserir filho...</option>"
                opt = 0
                for obj in tmpObjs:
                    printed+= "        <option value=\"%i\">%s</option>" % (opt, obj[2])
                    opt = opt + 1
                printed+= "    </select>"
            printed+= "</p>"
            printed+= "</form>"
        else:
            strlink = "(%s)" % defelem.name()
            str_attr = ''
            for a in attr:
                if str_attr:
                    str_attr = str_attr + '&nbsp;&nbsp;&nbsp;'
                else:
                    str_attr = '['
                str_attr = str_attr + a[2] + '="' + a[1] + '";'
            if str_attr:
                str_attr = str_attr[:-1] + ']'
            printed+= "<p style=\"padding-left: %ipx; white-space: pre;\"><a class=\"elem\" href=\"renderHTMLforEditing?elem_id=%s#%s\">%s</a> %s" % (i,self.id,self.id,strlink,str_attr)
            printed+= "%s</p>" % self.text
        for x in (self.objectValues()):
            printed+= x.renderHTMLforEditing(indent+4,elem_id)
        return printed

    # *** renderXML
    def renderXML (self,indent=""):
        printed=""
        pref = self.template().xmlns_prefix
        xmltag = self.definitionElement(obj=self).xmlTag()
        attr = self.attributes()
        str_attr = ''
        for a in attr:
            str_attr = str_attr + ' ' + a[0] + '="' + str(a[1]) + '"'
        printed+= "%s<%s:%s id=\"%s\"%s>" % (indent,pref,xmltag,self.id,str_attr)
        if self.has_own_value():
            printed+= "%s<%s:%s_text>%s</%s:%s_text>" % (indent+"   ",pref,xmltag,self.text,pref,xmltag)
        for x in (self.objectValues("SDE-Document-Element")):
            printed+= x.renderXML(indent+"   ")
        printed+= "%s</%s:%s>" % (indent,pref,xmltag)
        return printed

    # *** renderXMLforEditing
    def renderXMLforEditing (self,indent=0, id_edit='', path='', prev='', next=''):
        "Método de renderização XML"
        
        session = self.REQUEST.SESSION
        printed=""
        spaces = ''
        for i in range (0,indent * 4):
            spaces = spaces + ' '

        defelem = self.definitionElement(obj=self)
        attr = self.attributes()
        chd = self.possibleChild(obj=self)
        id = self.id

        if path:
            c_path = path + id + '/'
        else:
            c_path = id + '/'

        if (id_edit==id) and (defelem.has_own_value):
            str_edit_attrib = 'yes'
        else:
            str_edit_attrib = 'no'

        str_moveup_attrib = 'no'
        if prev:
            if prev.type == self.type:
                str_moveup_attrib = 'yes'

        str_movedn_attrib = 'no'
        if next:
            if next.type == self.type:
                str_movedn_attrib = 'yes'
                
        str_canpaste_attrib = 'no'
        if session.has_key('SDE_clip_key'):
            if session['SDE_clip_key']:
                for c in chd:
                    if c[0] == session['SDE_clip_object_type']:
                        str_canpaste_attrib = 'yes'
                        break;

        printed+= '%s<sd_element id="%s" type="%s" type_name="%s" editing="%s" path="%s" up="%s" down="%s" paste="%s">\n' % (spaces, id, self.type, defelem.name(), str_edit_attrib, path, str_moveup_attrib, str_movedn_attrib, str_canpaste_attrib)
        if defelem.has_own_value:
            printed+= '%s    <sde_text>%s</sde_text>\n' % (spaces, self.text)
        if attr != []:
            for a in attr:
                printed+= '%s    <sde_attr id="%s" name="%s">%s</sde_attr>\n' % (spaces, a[0], a[2], a[1])
        for c in chd:
            if c[1] == 0:
                if c[3]:
                    str_opt = "yes"
                else:
                    str_opt = "no"
                printed+= '%s    <sde_child type="%s" name="%s" pos="%s" opt="%s" path="%s"></sde_child>\n' % (spaces, c[0],c[2],c[1], str_opt, c_path)
        pos = 0
        t_prev = ''
        t_next = ''
        t_objs = self.objectValues()
        t_i = 0
        t_max = len(t_objs) - 1
        while t_i <= t_max:
            x = t_objs[t_i]
            if t_i > 0:
                t_prev = t_objs[t_i - 1]
            else:
                t_prev = ''
            if t_i < (t_max):
                t_next = t_objs[t_i + 1]
            else:
                t_next = ''
            printed+= x.renderXMLforEditing(indent+1, id_edit, path + id + '/', t_prev, t_next)
            pos = pos + 1
            for c in chd:
                if c[1] == pos:
                    if c[3]:
                        str_opt = "yes"
                    else:
                        str_opt = "no"
                    printed+= '%s    <sde_child type="%s" name="%s" pos="%s" opt="%s" path="%s"></sde_child>\n' % (spaces, c[0],c[2],c[1], str_opt, c_path)
            t_i = t_i + 1
        for c in chd:
            if c[1] > pos:
                if c[3]:
                    str_opt = "yes"
                else:
                    str_opt = "no"
                printed+= '%s    <sde_child type="%s" name="%s" pos="%s" opt="%s" path="%s"></sde_child>\n' % (spaces, c[0],c[2],c[1], str_opt, c_path)
        printed+= '%s</sd_element>\n' % spaces
        return printed
        
    def add_to_clipboard (self, op_type, REQUEST):
        """ Método que coloca uma referência do objeto na área de teransferência (clipboard).
            se op_type = 'CUT', quando a operação de "paste" for realizada, o objeto será movido,
            senão (se op_type='COPY') o objeto será copiado. """
        
        session=self.REQUEST.SESSION
        session['SDE_clip_object_type'] = self.type    
        if op_type == 'COPY':
            v_clip_key = self.parent().manage_copyObjects(self.id)
        elif op_type == 'CUT':
            v_clip_key = self.parent().manage_cutObjects(self.id)
        else:
            return 0
        
        session['SDE_clip_type'] = op_type
        session['SDE_clip_key'] = v_clip_key
        
        return

    def move_up(self):
        self.parent().manage_move_objects_up(self.REQUEST, self.id, 1)
        defElem = self.definitionElement(obj=self)
        if 'SDE_AfterMove' in defElem.objectIds('Script (Python)'):
            defElem.SDE_AfterMove(self, "UP")
        return

    def move_down(self):
        self.parent().manage_move_objects_down(self.REQUEST, self.id, 1)
        defElem = self.definitionElement(obj=self)
        if 'SDE_AfterMove' in defElem.objectIds('Script (Python)'):
            defElem.SDE_AfterMove(self, "DOWN")
        return

    def save(self):
        "Método para salvar os textos digitados"
        request = self.REQUEST
        RESPONSE = request.RESPONSE
        act = request.cmd
        anchor = ""
        father = self.parent()
        if act == "Gravar":
            self.manage_changeProperties(text=request.textedit)
            dic_attr = {}
            attr = self.attributes()
            for a in attr:
                if request.has_key('txattr_' + a[0]):
                    self.saveAttribute(a[0],request['txattr_'+a[0]])
            if len(dic_attr) > 0:
                self.manage_changeProperties(dic_attr)
            if (father.meta_type == "SDE-Document"):
                anchor = ""
            else:
                anchor = "?elem_id=%s#%s" % (father.id, father.id)
        elif act == "Excluir":
            request.set('id',self.id)
            self.parent().delChild()
        return RESPONSE.redirect (self.document().absolute_url() + "/renderHTMLforEditing" + anchor)

    # *** saveAttribute
    def saveAttribute(self,attribute='',value=''):
        dic={}
        dic['@'+attribute+'@'] = value
        self.manage_changeProperties(dic)
        return
