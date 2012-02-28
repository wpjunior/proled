#!/bin/sh
###################################################################################################
### Preparação
### Script para migracao dos dados do SAPL 2.1/2.2 para o SAPL 2.3

NEW_INST="/var/interlegis/SAPL-2.3-beta/instances/sapl23"
MYSQL_PATH="/var/interlegis/SAPL-2.3-beta/mysql"
PYTHON_EGG_CACHE="$NEW_INST/var/.python-eggs"

export PYTHON_EGG_CACHE

if [ -d /var/lib/zope2.8/instance/sapl ]; then
    INST_PATH="/var/lib/zope2.8/instance/sapl"
elif [ -d /var/lib/zope2.9/instance/sapl ]; then
    INST_PATH="/var/lib/zope2.9/instance/sapl"
else
    echo "********* ERRO **********";
    echo "Não foi encontrada nenhuma instalação antiga do SAPL";
    echo "Copie os arquivos Data.fs, DocumentosSapl.fs e sapl_old.sql em $NEW_INST/old";
    echo "*************************";
    exit 1;
fi

if [ -d $path ]; then
    INST_PATH=$path
else
    echo "********* ERRO **********";
    echo "*  O diretório informado não existe.   *"
    echo "*  Reinicie o script de migração e informe o caminho corretamente.   *"
    echo "*************************";
   exit 1;
fi

if [ ! "$USER" = 'root' ]; then
   echo "********* ERRO **********";
   echo "*   Este script deve ser executado pelo usuário 'root'.";
   echo "*   Chame-o com o comando 'sudo ./sapl_migracao.sh'.";
   echo "*************************";
   exit 1;
fi

if [ ! -f "$NEW_INST/old/Data.fs" ]; then
   echo "********* ERRO **********";
   echo "*   O arquivo Data.fs da versão anterior do SAPL não está no diretório correto.";
   echo "*   Grave-o em '$NEW_INST/old' e tente novamente.";
   echo "*************************";
   exit 1;
fi
echo "ok... Encontrado o arquivo Data.fs da versao anterior"

if [ ! -f "$INST_PATH/DocumentosSapl.fs" ] && [ ! -f "$NEWS_INST/old/DocumentosSapl.fs" ]; then
   echo "********* ERRO **********";
   echo "*   O arquivo DocumentosSapl.fs da versão anterior do SAPL não está no diretório correto.";
   echo "*   Grave-o em '$NEW_INST/old' e tente novamente.";
   echo "*************************";
   exit 1;
fi
echo "ok... Encontrado o arquivo DocumentosSapl.fs da versao anterior"

if [ ! -f "$NEW_INST/old/sapl_old.sql" ]; then
   echo "********* ERRO **********";
   echo "*   O arquivo de backup do MySQL da versão anterior do SAPL não está no diretório correto.";
   echo "*   Grave-o em '$NEW_INST/old', com o nome 'sapl_old.sql', e tente novamente.";
   echo "*************************";
   exit 1;
fi
echo "ok... Encontrado o arquivo sapl_old.sql"

# Pára o SAPL, se estiver em execução
kill `ps ax | grep \/sapl\/ | grep \/run.py | cut -d" " -f1`
echo "ok... SAPL antigo parado."

$NEW_INST/bin/zopectl stop
echo "ok... SAPL 2.3 parado"

# Acertar a propriedade do arquivo old/Data.fs para que possa ser utilizado pelo zope
chown zope.zope $NEW_INST/old/Data.fs && echo "ok... Ajustado o proprietário do arquivo old/Data.fs"

###################################################################################################
### Importação dos dados do banco relacional (MySQL)

# Fazer a importacao dos dados antigos, inclusive com a substituicao das novas tabelas
# Depois, realizar a insercao das novas tabelas e colunas nas tabelas existentes

$MYSQL_PATH/bin/mysql -uroot interlegis < $NEW_INST/old/sapl_old.sql
echo "ok... Importado o arquivo do backup do MySQL"

$MYSQL_PATH/bin/mysql -uroot interlegis < $NEW_INST/Products/ILSAPL/instalacao/sapl_migracao_banco.sql
echo "ok... Atualizado o banco para a nova estrutura do SAPL 2.3"

###################################################################################################
### Importação e ajuste do ZODB
# Antes de chamar o sapl_migracao.py, parar o Zope (ou verificar se esta parado) e 
# fazer COPIA DE SEGURANCA DO Data.fs e do DocumentosSapl.fs

# Verificar se existe outros arquivos

if [ -f $NEW_INST/var/DocumentosSapl.fs.index ]; then
    rm -f $NEW_INST/var/DocumentosSapl.fs.index
fi
if [ -f $NEW_INST/var/DocumentosSapl.fs.lock ]; then
    rm -f $NEW_INST/var/DocumentosSapl.fs.lock
fi
if [ -f $NEW_INST/var/DocumentosSapl.fs.tmp ]; then
    rm -f $NEW_INST/var/DocumentosSapl.fs.index
fi

# Fazer a copia do DocumentosSapl.fs para o novo path
cp $INST_PATH/var/DocumentosSapl.fs $NEW_INST/var/
chown zope.zope $NEW_INST/var/DocumentosSapl.fs
echo "ok... Arquivo DocumentosSapl.fs copiado"

# Fazer a migracao dos dados do antigo SAPL
$NEW_INST/bin/zopectl run $NEW_INST/Products/ILSAPL/instalacao/sapl_migracao.py
