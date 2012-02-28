### Script a ser rodado com "zopectl run" durante o processo de instalacao do SAPL.
### Criado por Ciciliati, em 26/10/2005
### Versao do SAPL: 2.3
### Versao deste script: 1.2 - Gustavo Lepri - 29/10/2008

import App.version_txt

versao = App.version_txt.version_txt()

if versao.find('Zope 2.7') > -1:
  t=get_transaction()
else:
  import transaction
  t=transaction.get()

### Criar "sapl"
##### 1 - Configurar ambiente de seguranca
####### 1.1 - Identificar um usuario com perfil 'Manager"
i=0
t_username = ""
l_users=app.acl_users.getUsers()
while i < len(l_users):
    if l_users[i].has_role('Manager'):
        t_username = l_users[i].name
        break
    i=i+1
if not t_username:
    print "*** ERRO! Na foi encontrado um usuário administrador do Zope.Contacte o Interlegis. ***"
######## 1.2 - Registrar esse usuario nesta sessao
from AccessControl.SecurityManagement import newSecurityManager
adminuser=app.acl_users.getUser(t_username).__of__(app.acl_users)
newSecurityManager (None, adminuser)

### Adicionar o SAPL ###
app.manage_addProduct['ILSAPL'].manage_addSAPL(id='sapl',title='SAPL-Sistema de Apoio ao Processo Legislativo', database='MySQL')
  
### Criar "sapl_documentos"  

if 'sapl_documentos' not in app.sapl.objectIds():
    app.sapl.manage_delFolder('/sapl/sapl_documentos')

    # Criar mount_point do sapl_documentos
    app.manage_addProduct['ZODBMountPoint'].manage_addMounts(paths=['/sapl/sapl_documentos'],create_mount_points=1)
    # Importar conteudo de 'sapl_documentos' para o folder
    for o in ['props_sapl.zexp','modelo.zexp','proposicao.zexp','parlamentar.zexp','materia.zexp','norma_juridica.zexp','oradores.zexp']:
        app.sapl.sapl_documentos.manage_importObject(o)

### Gravar alteracoes
t.commit()
