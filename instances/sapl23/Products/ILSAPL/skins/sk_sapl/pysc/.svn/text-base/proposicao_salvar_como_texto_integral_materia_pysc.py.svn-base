## Script (Python) "proposicao_salvar_como_texto_integral_materia_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=cod_proposicao, cod_materia, ind_sobrescrever=0
##title=
##
ok = 0
tip_prop = container.proposicao_tipo_texto_integral_pysc(cod_proposicao)
id = str(cod_materia) + '_texto_integral'
try:
    doc = context.sapl_documentos.materia[id]
    if (int(ind_sobrescrever)==1):
        doc=''     
        context.sapl_documentos.materia.manage_delObjects(id)
        if (tip_prop == 'XML'):
            context.sapl_documentos.materia.manage_addFile(id=id, file=context.sapl_documentos.proposicao[cod_proposicao].renderXML(xsl="__default__"), content_type='text/xml')
        else:
            tmp_copy = context.sapl_documentos.proposicao.manage_copyObjects(ids=str(cod_proposicao))
            tmp_id = context.sapl_documentos.materia.manage_pasteObjects(tmp_copy)[0]['new_id']
            context.sapl_documentos.materia.manage_renameObjects(ids=list([tmp_id]),new_ids=list([id]))
        ok = 1
except KeyError:
    if (tip_prop == 'XML'):
        context.sapl_documentos.materia.manage_addFile(id=id, file=context.sapl_documentos.proposicao[cod_proposicao].renderXML(xsl="__default__"), content_type='text/xml')
    else:
        tmp_copy = context.sapl_documentos.proposicao.manage_copyObjects(ids=str(cod_proposicao))
        tmp_id = context.sapl_documentos.materia.manage_pasteObjects(tmp_copy)[0]['new_id']
        context.sapl_documentos.materia.manage_renameObjects(ids=list([tmp_id]),new_ids=list([id]))
    ok = 1
context.REQUEST.RESPONSE.setHeader('Content-type', 'text/html')
return ok
