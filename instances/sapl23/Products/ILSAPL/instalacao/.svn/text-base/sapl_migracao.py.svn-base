### Script a ser rodado durante o processo de migração de dados de versões anteriores do SAPL.
### ESTE SCRIPT NÃO DEVE SER EXECUTADO DIRETAMENTE. ELE É CHAMADO PELO SHELL SCRIPT sapl_migracao.sh
### Criado por Ciciliati, em 07/04/2006
### Versão do SAPL: 2.3
## Versão deste script: 1.1 - Gustvo Lepri - 29/10/2008

import App.version_txt
from OFS.Image import File

def _prepTransaction():
  ### Prepara mecanismo de transação do ZODB
  versao = App.version_txt.version_txt()

  if versao.find('Zope 2.7') > -1:
    t=get_transaction()
  else:
    import transaction
    t=transaction.get()
  return t

### Remover o mount-point '/sapl/sapl_documentos'
### Essa remocao eh necessaria para evitar um erro com a migracao do banco
app.sapl._delObject('sapl_documentos')
print "ok... Mount-point dos documentos removido com sucesso"

### Criar o mount-point do Data.fs antigo em '/sapl_old'
app.manage_addProduct['ZODBMountPoint'].manage_addMounts(paths=['/sapl_old'],create_mount_points=1)
print "ok... Criado o mount-point para o 'Data.fs' antigo em '/sapl_old'"

### Migrar usuários
print "..... Iniciando migracao de usuarios"
acl = app.sapl.acl_users
users=acl.getUserNames()
for u in app.sapl_old.acl_users.getUsers():
  t_id = u.getUserName()
  if t_id in users:
    print ".....    ATENCAO: Usuario '%s' ja existe na versao atual." % t_id
    t_id = 'old_' + t_id
    print ".....       O usuario da versao anterior foi criado com o username '%s'" % t_id
  t_pwd = u._getPassword()
  acl._addUser(t_id,t_pwd,t_pwd,list(u.getRoles()),[])
  print ".....    Migrado usuario %s" % t_id
print "ok... Concluida migracao de usuarios"

### Recriar o mount-point do DocumentosSapl.fs antigo em '/sapl/sapl_documentos'
app.manage_addProduct['ZODBMountPoint'].manage_addMounts(paths=['/sapl/sapl_documentos'],create_mount_points=1)
print "ok... Recriado o mount-point para o 'DocumentosSapl.fs' em '/sapl/sapl_documentos'"

# Importar a pasta oradores
app.sapl.sapl_documentos.manage_importObject('oradores.zexp')
print "ok... Diretório 'oradores' importado com sucesso"

### Remover o mount-point '/sapl_old'
app._delObject('sapl_old')
print "ok... Mount-point da base antiga removido com sucesso"

t = _prepTransaction()
t.commit()
print "ok... Commit final efetuado com sucesso"
