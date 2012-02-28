### Script a ser rodado durante o processo de migração de dados de versões anteriores do SAPL.
### ESTE SCRIPT NÃO DEVE SER EXECUTADO DIRETAMENTE. ELE É CHAMADO PELO SHELL SCRIPT sapl_migracao.sh
### Criado por Ciciliati, em 07/04/2006
### Versão do SAPL: 2.1
## Versão deste script: 1.0 - Ciciliati - 07/04/2006

import App.version_txt
from OFS.Image import File

### Funções genéricas
def _renameObj(container,id_old,id_new):
  obj =  container._getOb(id_old)
  container._delObject(id_old)
  obj._setId(id_new)
  container._setObject(id_new,obj,set_owner='0')

def _copyFile(f_from, f_to, id, keep_new=False):
  obj_id = id
  if hasattr(f_to,id):
    if keep_new:
      obj_id = 'old_' + id
    else:
      _renameObj (f_to, id, 'new_' + id)
  oldobj = f_from._getOb(id)
  newobj = File(obj_id,oldobj.title,'',oldobj.content_type)
  newobj.size = oldobj.size
  newobj.data = oldobj.data[:]
  f_to._setObject(obj_id, newobj)

def _prepTransaction():
  ### Prepara mecanismo de transação do ZODB
  versao = App.version_txt.version_txt()

  if versao.find('Zope 2.7') > -1:
    t=get_transaction()
  else:
    import transaction
    t=transaction.get()
  return t

### Renomear o python script '/sapl' para 'sapl.py'
_renameObj(app,'sapl','sapl.py')
print "ok... 'sapl' renomeado para 'sapl.py'"

### Criar o mount-point do Data.fs antigo em '/sapl'
app.manage_addProduct['ZODBMountPoint'].manage_addMounts(paths=['/sapl'],create_mount_points=1)
print "ok... Criado o mount-point para o 'Data.fs' antigo em '/sapl'"

### Migrar usuários
print "..... Iniciando migracao de usuarios"
acl = app.acl_users
users=acl.getUserNames()
for u in app.sapl.acl_users.getUsers():
  t_id = u.getUserName()
  if t_id in users:
    print ".....    ATENCAO: Usuario '%s' ja existe na versao atual." % t_id
    t_id = 'old_' + t_id
    print ".....       O usuario da versao anterior foi criado com o username '%s'" % t_id
  t_pwd = u._getPassword()
  acl._addUser(t_id,t_pwd,t_pwd,list(u.getRoles()),[])
  print ".....    Migrado usuario %s" % t_id
print "ok... Concluida migracao de usuarios"

### Migrar propriedades do /sapl para /sapl_documentos/props_sapl
props = app.sapl_documentos.props_sapl
for p in app.sapl.propertyItems():
  if p[0] != 'versao':
    setattr(props,p[0],p[1])
print "ok... Concluida migracao dos dados da Casa"

t = _prepTransaction()
t.commit()
print "ok... Primeiro commit efetuado com sucesso."

### Migrar documentos (cuidado com versões antigas do SAPL)

# Migrar matérias
print "..... Iniciando migracao de materias"
erro = False
fo = app.sapl.documentos.materia
fd = app.sapl_documentos.materia
for obj in fo.objectItems('File'):
  print "  ...    Iniciando migracao da materia '%s'" % obj[0] 
  if obj[1].size > 0:
    _copyFile (fo, fd, obj[0])
    print "  ...    Migrada materia '%s'" % obj[0] 
    try:
      t = _prepTransaction()
      t.commit()
      print "  ok.    Commit da materia efetuado com sucesso"
    except:
      erro = True
      print "  ***    Commit da materia deu ERRO - A MATERIA NAO FOI GRAVADA!!!"
      t.abort()
  else:
    print "  ***    Materia %s NÃO FOI MIGRADA: TAMANHO ZERO!!!" % obj[0]
###############???????? É necessário fazer algo com o catálogo?
###############???????? Cuidado com a mudança de nomenclatura de objetos
if erro:
  print "!!!!! ATENCAO: Migracao de materias concluida com alguns erros."
else:
  print "ok... Concluida migracao de materias sem nenhum erro."

# Migrar normas
print "..... Iniciando migracao de normas"
erro = False
fo = app.sapl.documentos.norma_juridica
fd = app.sapl_documentos.norma_juridica
print "  ... Iniciando migracao de normas armazenadas em 'File'"
for obj in fo.objectItems('File'):
  print "  ...    Iniciando migracao da norma '%s'" % obj[0] 
  if obj[1].size > 0:
    _copyFile (fo, fd, obj[0])
    print "  ...    Migrada norma '%s'" % obj[0]
    try:
      t = _prepTransaction()
      t.commit()
      print "  ok.    Commit da norma efetuado com sucesso"
    except:
      erro = True
      print "  ***    Commit da norma deu ERRO - A NORMA NAO FOI GRAVADA!!!"
      t.abort()
  else:
    print "  ***    Norma %s NÃO FOI MIGRADA: TAMANHO ZERO!!!" % obj[0]
print "  ... Iniciando migracao de normas armazenadas em 'NuxDocument'"
############  !!! INCORPORAR Produto NuxDocument no SAPL 2.1
for obj in fo.objectItems('NuxDocument'):
  print "  ...    Iniciando migracao da norma '%s'" % obj[0] 
  fd.manage_addFile(id=obj[0])
  new = fd[obj[0]]
  new.manage_edit(title=old[1].title,filedata=old[1].getRaw(),content_type=old[1].content_type())
  try:
    t = _prepTransaction()
    t.commit()
    print "  ok.    Commit da norma efetuado com sucesso"
  except:
    erro = True
    print "  ***    Commit da norma deu ERRO - A NORMA NAO FOI GRAVADA!!!"
    t.abort()
  print "  ...    Migrada norma '%s'" % obj[0]
############ ????????  É necessário fazer algo com o catálogo?
if erro:
  print "!!!!! ATENCAO: Migracao de normas concluida com alguns erros."
else:
  print "ok... Concluida migracao de normas"

# Migrar modelos de proposições
### Considerando qu até o momento (abr/2006) nenhuma casa
### notificou haver criado seus próprios modelos de proposição,
### os modelos importados serão deixados inativos, prefixados 
### como old.

# Migrar proposições
# Apenas copiar... a migração do SDE 0 para o SDE 1 será feita abaixo (ou por script externo)
print "..... Iniciando migracao de proposições"
erro = False
fo = app.sapl.documentos.proposicao
fd = app.sapl_documentos.proposicao
############ Migrando apenas proposições tipo File (Arquivo Externo)
for obj in fo.objectItems('File'):
  print "  ...    Iniciando migracao da proposicao '%s'" % obj[0] 
  if obj[1].size > 0:
    _copyFile (fo, fd, obj[0])
    print "  ...    Migrada proposicao '%s'" % obj[0] 
    try:
      t = _prepTransaction()
      t.commit()
      print "  ok.    Commit da proposicao efetuado com sucesso"
    except:
      erro = True
      print "  ***    Commit da proposicao deu ERRO - A PROPOSICAO NAO FOI GRAVADA!!!"
      t.abort()
  else:
    print "  ***    Proposicao %s NÃO FOI MIGRADA: TAMANHO ZERO!!!" % obj[0]
if erro:
  print "!!!!! ATENCAO: Migracao de proposicoes concluida com alguns erros."
else:
  print "ok... Concluida migracao de proposicoes sem nenhum erro."

### Migrar o logotipo
fo = app.sapl.imagens                      #fo = folder de origem
fd = app.sapl_documentos.props_sapl        #fd = folder de destino
logo_id = 'logo_casa'                      #logo_id = id do logotipo
if hasattr(fo, logo_id):
  old_logo = getattr(fo, logo_id)
  if hasattr(fd, logo_id):
    _renameObj(fd,logo_id,'new_'+logo_id)
  fd.manage_addImage(id=logo_id,file='')
  new_logo = fd._getOb(logo_id)
  new_logo.data = old_logo.data
  new_logo.size = old_logo.size
  new_logo.width = old_logo.width
  new_logo.height = old_logo.height
  new_logo.content_type = old_logo.content_type
  print "ok... Logotipo encontrado e migrado"

t = _prepTransaction()
t.commit()
print "ok... Commit do logotipo efetuado com sucesso."

### Remover o mount-point '/sapl'
app._delObject('sapl')
print "ok... Mount-point da base antiga removido com sucesso"

### Renomear '/sapl.py' para '/sapl'
_renameObj(app,'sapl.py','sapl')
print "ok... 'sapl.py' renomeado para 'sapl'"

t = _prepTransaction()
t.commit()
print "ok... Commit final efetuado com sucesso"

