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

def StrDoc_addForm(self, REQUEST):
    "HTML para adicionar um novo objeto StrDoc"
    return """
<HTML>
<HEAD><TITLE>Add StructuredDocument</TITLE></HEAD>
<BODY BGCOLOR="#FFFFFF" LINK="#000099" VLINK="#555555">
<H2>Add StructuredDocument</H2>
<form action="manage_addStrDoc"><table>
<tr><th>Id</th>
    <td><input type=text name=id></td>
</tr>
<tr><th>Template Path</th>
    <td><input type=text name="template_path"></td>
</tr>
<tr><th>Document Type</th>
    <td><input type=text name="type"></td>
</tr>
<tr><td></td><td><input type=submit value=" Add "></td></tr>
</table></form>
</body></html>
"""

def StrDoc_add(self,REQUEST):
    "Método para adicionar um objeto StrDoc"
    instance = StrDoc(REQUEST)
    instance.reindex_object()
    self._setObject(REQUEST.id,instance)
    return instance

class StrDoc(OrderedFolder,CatalogAware):
    "Classe de documentos estruturados"
    meta_type = 'SDE-Document'
    filtered_meta_types = []

    def __init__(self,REQUEST):
        self.id = REQUEST.id
        self._setProperty("template_path",REQUEST.template_path)
        self._setProperty("type",REQUEST.type)
        self._setProperty("nextElemId",1)

    # *** addChild
    def addChild (self,ch_type='',ch_position='',obj=''):
        request = self.REQUEST
        RESPONSE =  request.RESPONSE
        if obj:
            self=obj
        if ch_type:
            request.set('type',ch_type)
        if ch_position:
            request.set('position',int(ch_position))
        newElem = self.manage_addProduct['StructuredDoc'].StrDocElem_add(request)
        return newElem.id

    def addChildFromClipboard (self,ch_position='',obj=''):
        request = self.REQUEST
        session = request.SESSION
        if session.has_key('SDE_clip_key'):
            if session['SDE_clip_key']:
                if obj:
                    self=obj
                clip_type = session['SDE_clip_type']     
                self.manage_pasteObjects(session['SDE_clip_key'])
                session['SDE_clip_type'] = ''
                session['SDE_clip_key'] = ''
                session['SDE_clip_object_type'] = ''
                #if clip_type == 'CUT':
                #    pass    
                #elif clip_type == 'COPY':
                #    pass
                #    # No caso de cópia: recriar IDs, verificar se objetos-filho são diferentes
                #    #self.setNewIdForChildren(recursive=1,obj=self)
        return

    # *** checksum
    def checksum (self, obj=''):
        "Método que calcula um checksum do conteúdo do documento estruturado"
        from zlib import crc32
        if obj:
            self=obj
        crc = 0L
        i = 0
        t = 0
        for x in self.objectValues():
            i = i + 1
            crc = crc + (i * x.checksum(x))
            t = t + i
        if (i > 0):
            crc = crc / t
        else:
            crc = 0L
        if (self.meta_type == 'SDE-Document-Element'):
            crc = crc + crc32(self.id + self.text)
        return crc

    # *** definitionElement
    def definitionElement(self,element_path='',obj=''):
        if obj:
            self = obj
        if element_path == '':
            element_path = self.definitionPath(0)
        subtree = string.split(element_path,"/")
        temp_name = subtree.pop(0)
        return self.template().getDefElement(subtree=subtree)

    # *** definitionPath
    def definitionPath(self,absolute=0):
        if absolute:
            return self.template_path + "/" + self.type
        else:
            return self.type

    # *** delChild
    def delChild(self):
        request = self.REQUEST
        RESPONSE = request.RESPONSE
        if request.has_key ('id'):
            self.manage_delObjects(request.id)
        return RESPONSE.redirect (self.document().absolute_url() + "/renderHTMLforEditing")

    # *** document
    def document(self):
      # return container.this() *** this was the ZClass version.
        return self.this()

    # *** getElements
    def getElements(self,type='',obj=''):
        if obj:
            self = obj
        result = []
        for x in self.objectValues('SDE-Document-Element'):
            if (not type) or (x.type == type):
                result.append(x)
            temp = x.getElements(type,obj=x)
            if temp != []:
                result.extend(temp)
        return result

    # *** getXML
    def getXML(self,xsl=''):
        tpt = self.template()
        pref = tpt.xmlns_prefix
        tag = tpt.xmlTag()
        server = self.REQUEST['SERVER_URL']
        printed = ''
        printed+= "<?xml version=\"1.0\" encoding=\"ISO-8859-1\" ?>\n"   # generalizar o encoding
        if xsl:
            if (xsl!="__default__"):
                printed+= "<?xml-stylesheet type=\"text/xsl\" href=\"%s\"?>\n" % xsl
            elif (tpt.default_xslt_for_html):
                printed+= "<?xml-stylesheet type=\"text/xsl\" href=\"%s\"?>\n" % tpt.default_xslt_for_html
        printed+= "<%s:%s id=\"%s\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"" %(pref,tag,self.id)
        printed+= "       xmlns:%s=\"/XSD/%s\"" % (pref, self.type)
        printed+= "       xsi:noNamespaceSchemaLocation=\"/XSD/%s.xsd\">" % self.type
        for x in (self.objectValues("SDE-Document-Element")):
            printed+= x.renderXML("   ")
        printed+= "</%s:%s>" % (pref,tag)
        return printed

    # *** isInvalid
    def isInvalid(self,obj=''):
        if obj:
            self = obj
        request = self.REQUEST
        RESPONSE = request.RESPONSE
        tpt = self.definitionElement(obj=self).objectValues(['SDE-Template-Element','SDE-Template-Link'])
        doc = self.objectValues('SDE-Document-Element')
        exc = []
        if ((len(doc) == 0) and (self.meta_type == 'SDE-Document')):
            exc.append ("Documento Inválido: Está Vazio.")
        if (len(exc) == 0):
            it = 0
            max_it = len(tpt)
            instance_found = 0
            for e in doc:
                while ((e.type != tpt[it].id) and (it < max_it)):
                    if ((not tpt[it].isOptional()) and (not instance_found) and \
                       (e.definitionElement(obj=e).exclusivity_group == -1)):
                        exc.append ("Verificando \"%s\": Elemento obrigatório, \"%s\", não foi encontrado antes \
                                     do elemento \"%s\"" % (self.type, tpt[it].id,e.type))
                    it = it + 1
                    instance_found = 0
                if (e.type == tpt[it].id):
                    if (instance_found and (not tpt[it].isMultiple())):
                        exc.append ("Verificando \"%s\": O elemento \"%s\" não admite mais de uma ocorrência \
                                     nesse contexto." % (self.type,tpt[it].id))
                    instance_found = 1
            while (it < max_it):
                if (not instance_found) and (not tpt[it].isOptional() and (tpt[it].exclusivity_group == -1)):
                    exc.append ("Verificando \"%s\": Elemento obrigatório, \"%s\", não foi encontrado após o \
                                 último elemento." % (self.type,tpt[it].id))
                it = it + 1
                instance_found = 0
        if (len(exc) == 0):
            for e in doc:
                exc_child = e.isInvalid(obj=e)
                if (len(exc_child) > 0):
                    for x in exc_child:
                        exc.append (x)
        return exc

    # *** newElemId
    def newElemId(self):
        newId = "SDE" + str(self.nextElemId)
        self.manage_changeProperties(nextElemId= int(self.nextElemId) + 1)
        return newId

    # *** possibleChild
    def possibleChild(self,debug=0,obj=''):
        "***debug***"
        if obj:
            self=obj
        elmdef = self.definitionElement(obj=self)
        tpt = elmdef.possibleChild(obj=elmdef)

        #***
        if debug:
            print "<html><body>"
            print tpt
            print "<hr>"
        #***

        doc = []
        for x in self.objectValues():
            elm = []
            elm.append(x.type)
            elm.append(x.id)
            elm.append(self.getObjectPosition(x.id))
            elm.append(x.definitionElement(obj=x).exclusivity_group)
            doc.append (elm)

        #***
        if debug:
            print doc
            print "<hr>"
        #***

        excl_grp = []
        chd = []
        i = 0
        pos = 0
        m = len(tpt)
        jump = ""
        for x in doc:
            if (x[0] == jump):
                chd[-1][1] = (x[2] + 1)
                pos = pos + 1
                continue
            elif (x[3] != -1):
                excl_grp.append (x[3])
            jump = x[0]
            while (i < m) and (x[0] != tpt[i][0]):
                if tpt[i][4] not in excl_grp:
                    elm = []
                    elm.append (tpt[i][0])
                    elm.append (pos)
                    elm.append (tpt[i][5])
                    elm.append (tpt[i][1])
                    chd.append (elm)
                i = i + 1
            pos = x[2]
            if (i < m):
                pos = pos + 1
                if (tpt[i][2]):
                    elm = []
                    elm.append (tpt[i][0])
                    elm.append (pos)
                    elm.append (tpt[i][5])
                    elm.append ((1==1))
                    chd.append (elm)
            i = i + 1
        while (i < m):
            if tpt[i][4] not in excl_grp:
                elm = []
                elm.append (tpt[i][0])
                elm.append (pos)
                elm.append (tpt[i][5])
                elm.append (tpt[i][1])
                chd.append (elm)
            i = i + 1

        #***
        if debug:
            print excl_grp
            print "<hr>"
            print chd
            print "<hr>"
            print "</body></html>"
            return chd
        else:
            return chd
        #***

    # *** possibleChildDebug
    def possibleChildDebug(self):
        return self.possibleChild(debug=1)

    # *** renderHTML
    def renderHTML(self):
        "Renderiza o documento em HTML para visualização. Útil para browsers que não suportam XML."
        printed=""
        printed+= "<html>\n"
        for x in (self.objectValues()):
            printed+= x.renderHTML()
        printed+= "\n</html>"
        return printed

    # *** renderHTMLforEditing
    def renderHTMLforEditing(self,validation=0,REQUEST=None):
        "Renderiza o documento em HTML para Edição. Útil para browsers que não suportam XML."
        printed=""
        request = REQUEST
        if not request.AUTHENTICATED_USER.has_permission('EditStructuredDocument',self):
            return self.renderHTML()
        elem_id = ""
        if request.has_key("elem_id"):
            elem_id = request.elem_id
        printed+= "<html>\n"
        printed+= "<head>"
        printed+= "    <script type=\"text/javascript\">"
        printed+= "        function AddChildOnSelect (strContext, selSelectObject)"
        printed+= "        {"
        printed+= "            if (selSelectObject.options[selSelectObject.selectedIndex].value != \"\")"
        printed+= "            {"
        printed+= "                location.href=(strContext + '/renderHTMLforEditing_addChild?opt=' + \
                                   selSelectObject.options[selSelectObject.selectedIndex].value)"
        printed+= "            }"
        printed+= "        }"
        printed+= "    </script>"
        printed+= "    <style>"
        printed+= "        a.elem:link     { text-decoration:none; color: blue; }"
        printed+= "        a.elem:visited  { text-decoration:none; color: blue; }"
        printed+= "        a.elem:hover    { text-decoration:underline; color: red; }"
        printed+= "    </style>"
        printed+= "</head>\n"
        printed+= "<body style=\"font-family: \'times new roman\'; font-size: 12pt;\">\n"
        if elem_id == "":
            printed+= "<form method=\"post\" action=\"%s/save\">\n" % self.absolute_url()
            tmpObjs = self.possibleChild()
            if (tmpObjs != []):
                printed+= "    <select name=\"selChild\" onChange=AddChildOnSelect('%s',this)>" % self.absolute_url()
                printed+= "        <option selected>Inserir filho...</option>"
                opt = 0
                for obj in tmpObjs:
                    printed+= "        <option value=\"%i\">%s</option>" % (opt, obj[2])
                    opt = opt + 1
                printed+= "    </select>"
            printed+= "</form>"
        else:
            printed+= "<p><a href=\"renderHTMLforEditing\">(Raiz)</a></p>"
        for x in (self.objectValues()):
            printed+= x.renderHTMLforEditing(indent=0,elem_id=elem_id)
        if (validation):
            printed+= "<hr>"
            printed+= "<h3>Validação do Documento</h3>"
            errors = self.isInvalid()
            if (errors):
                printed+= "<ul>"
                for e in errors:
                    printed+= "<li>%s</li>" % e
                printed+= "</ul>"
            else:
                printed+= "Documento Válido."
        printed+= "\n</body>"
        printed+= "\n</html>"
        return printed

    # *** renderHTMLforEditing
    def renderHTMLforEditing_addChild(self,REQUEST):
        "Método para adicionar elementos ao documento, usando a interface renderHTML."
        request = REQUEST
        RESPONSE = request.RESPONSE
        option = string.atoi(request.opt)
        chd = self.possibleChild()[option]
        request.set ('type',chd[0])
        request.set ('position',chd[1])
        newElemId = self.addChild()
        return RESPONSE.redirect (self.document().absolute_url() + "/renderHTMLforEditing?elem_id=" + \
                                  newElemId + "#" + newElemId)

    # *** renderXML
    def renderXML(self,xsl=''):
        "Renderiza o documento em XML, de acordo com a estrutura definida no modelo."
        printed = self.getXML(xsl)
        self.REQUEST.RESPONSE.setHeader('Content-type', 'text/xml')
        return printed

    def renderXMLforEditing(self,xslt=None, action=None, p_type=None, p_pos=None, p_id=None, p_path=None):
        """ Renderiza o documento em XML, em estrutura especial para edição.
        'action'   parameters             description
        EDIT       p_id                   renders the sd_element which has (id=p_id) with the attribute editing='yes'
        MOVE_UP    p_path, p_id           move one position up the element identified by p_id located at p_path
        MOVE_DOWN  p_path, p_id           move one position down the element identified by p_id located at p_path
        CREATE     p_path, p_type, p_pos  creates, under the element p_path, a child of type p_type at the p_pos position
        DELETE     p_path, p_id           removes the element p_id located in p_path
        SAVE       p_path, p_id, REQUEST  saves the changes to the element p_id located in p_path
                                          in REQUEST object there shall be a form called 'form_edit' containing
                                          a object (textarea) called 'txa_text' and several objects (text) named
                                          tat_??????, where ?????? is an attribute name (sde_attr)
        CUT        p_path, p_id           mark as 'cut' the element identified by p_id located at p_path and put it and
                                          its subtree into the clipboard
        COPY       p_path, p_id           put a copy of the referred element and its subtree into the clipboard
        PASTE      p_path, p_pos          put the contents of the clipboard under the element p_path """
        request = self.REQUEST
        response = request.RESPONSE
        printed=""

        if (action == 'CREATE'):
            e = self.restrictedTraverse(p_path)
            p_id = e.addChild (p_type, int(p_pos),obj=e)
            action = 'EDIT'
        elif (action == 'DELETE'):
            e = self.restrictedTraverse(p_path)
            e.manage_delObjects(p_id)
        elif (action == 'SAVE'):
            from Products.PythonScripts.standard import html_quote
            e = self.restrictedTraverse(p_path + p_id)
            e.manage_changeProperties(text=html_quote(request.txa_text))
            for x in request.form.keys():
                if x[0:4] == 'tat_':
                    attrN = x[4:]
                    attrV = request[x]
                    e.saveAttribute(attrN,attrV)
        elif (action == 'MOVE_UP'):
            e = self.restrictedTraverse(p_path + p_id)
            e.move_up()
        elif (action == 'MOVE_DOWN'):
            e = self.restrictedTraverse(p_path + p_id)
            e.move_down()
        elif (action in ['CUT','COPY']):
            e = self.restrictedTraverse(p_path + p_id)
            e.add_to_clipboard(action,request)
        elif (action == 'PASTE'):
            e = self.restrictedTraverse(p_path)
            e.addChildFromClipboard(int(p_pos),obj=e)
        if (action == 'EDIT'):
            id_edit = p_id
        else:
            id_edit = ''

        chd = self.possibleChild(obj=self)

        #
        #if not request.AUTHENTICATED_USER.has_permission('EditStructuredDocument',context):
        #    return context.renderHTML()
        #

        response.setHeader('Content-type', 'text/xml')

        printed+= '<?xml version="1.0" encoding="ISO-8859-1"?>\n'  #aqui tbm encoding poderia ser parametrizado
        if xslt:
            tpt = self.template()
            if (xslt!="__default__"):
                printed+= '<?xml-stylesheet type="text/xsl" href="%s"?>\n' % xslt
            elif (tpt.default_xslt_for_editor):
                printed+= '<?xml-stylesheet type="text/xsl" href="%s"?>\n' % tpt.default_xslt_for_editor
        printed+= '<strdoc id="%s" type="%s">\n' % (self.id, self.type)
        for c in chd:
            if c[1] == 0:
                if c[3]:
                    str_opt = "yes"
                else:
                    str_opt = "no"
                printed+= '    <sde_child type="%s" name="%s" pos="%s" opt="%s" path=""></sde_child>\n' % (c[0], c[2], c[1], str_opt)
        pos = 0
        for x in (self.objectValues()):
            printed+= x.renderXMLforEditing(indent=1, id_edit=id_edit)
            pos = pos + 1
            for c in chd:
                if c[1] == pos:
                    if c[3]:
                        str_opt = "yes"
                    else:
                        str_opt = "no"
                    printed+= '    <sde_child type="%s" name="%s" pos="%s" opt="%s" path=""></sde_child>\n' % (c[0], c[2], c[1], str_opt)
        for c in chd:
            if c[1] > pos:
                if c[3]:
                    str_opt = "yes"
                else:
                    str_opt = "no"
                printed+= '    <sde_child type="%s" name="%s" pos="%s" opt="%s" path=""></sde_child>\n' % (c[0], c[2], c[1], str_opt)
        printed+= '</strdoc>\n'
        response.setHeader('Content-type', 'text/xml')
        return printed

    # *** template
    def template (self):
        return self.restrictedTraverse(self.template_path + "/" + self.type)
