# -*- coding: utf-8 -*-
### Script a ser rodado com "zopectl run" durante o processo de instalação do SAPL.
### Criado por Ciciliati, em 26/10/2005
### Versão do SAPL: 2.1
### Versão deste script: 1.1 - Ciciliati - 09/05/2006

import App.version_txt

versao = App.version_txt.version_txt()

if versao.find('Zope 2.7') > -1:
  t=get_transaction()
else:
  import transaction
  t=transaction.get()

### Criar Roles
#for r in ['Administrador','Autor','Operador','Operador Parlamentar','Operador Ordem Dia','Operador Norma','Operador Tabela Auxiliar','Operador Mesa Diretora','Operador Comissao','Operador Materia']:
#    app._addRole(r)

### Importar objetos da raiz
#for o in ['XSD.zexp','XSLT.zexp','sapl.zexp']:
#    app.manage_importObject(o)
    
### Criar "sapl_site"
#app.manage_addProduct['CMFDefault'].manage_addCMFSite(id='sapl_site',title='SAPL-Sistema de Apoio ao Processo Legislativo',create_userfolder=0)

# "Limpar" sapl_site, excluindo todos os objetos-padrão, exceto os contidos na lista abaixo.
#lista=app.sapl_site.objectIds()
#for o in ['portal_skins','portal_membership','MailHost']:
#    lista.remove(o)    
#app.sapl_site.manage_delObjects(lista)

# Adicionar um "Filesystem Directory View" apontando para o código do SAPL
#if app.Control_Panel.Products['CMFCore'].version.find('CMF-1.4') > -1:
#    app.sapl_site.manage_addProduct['CMFCore'].manage_addDirectoryView(id='sapl_skin',filepath='ILSAPL/skins/sk_sapl')
#else:
#    app.sapl_site.manage_addProduct['CMFCore'].manage_addDirectoryView(id='sapl_skin',dirpath='ILSAPL/skins/sk_sapl')

# Criar a conexão de banco de dados
#app.sapl_site.manage_addProduct['ZMySQLDA'].manage_addZMySQLConnection(id='dbcon_interlegis',title='Banco de Dados do SAPL',connection_string='interlegis sapl sapl')

# Configurar o portal_skins
#app.sapl_site.portal_skins.manage_addProduct['OFSP'].manage_addFolder(id='Custom')
#app.sapl_site.portal_skins.manage_skinLayers(add_skin=1,skinname='Skin_SAPL',skinpath=['Custom'])
#lista=app.sapl_site.portal_skins.getSkinSelections()
#lista.remove('Skin_SAPL')
#app.sapl_site.portal_skins.manage_skinLayers(del_skin=1,chosen=lista)
    
### Criar "sapl_documentos"  

# Criar mount_point do sapl_documentos
app.manage_addProduct['ZODBMountPoint'].manage_addMounts(paths=['/sapl_documentos'],create_mount_points=1)

# Importar conteúdo de 'sapl_documentos' para o folder
for o in ['props_sapl.zexp','modelo.zexp','proposicao.zexp','parlamentar.zexp','materia.zexp','norma_juridica.zexp','XSD.zexp','XSLT.zexp']:
    p.sapl_documentos.manage_importObject(o)

### Criar 'Cookie Crumbler'    
app.manage_addProduct['CMFCore'].manage_addCC(id='cookie_authentication')

### Criar usuários 'padrão'
app.acl_users._addUser(name='saploper',password='saploper',confirm='saploper',roles=['Operador'],domains=[])
app.acl_users._addUser(name='sapladm',password='sapladm',confirm='sapladm',roles=['Administrador'],domains=[])

### Gravar alterações
t.commit()


