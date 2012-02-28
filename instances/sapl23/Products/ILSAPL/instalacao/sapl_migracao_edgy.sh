#!/bin/sh
###################################################################################################
### Preparação

INST_PATH="/var/lib/zope2.9/instance/sapl"

if [ ! "$USER" = 'root' ]; then
   echo "********* ERRO **********";
   echo "*   Este script deve ser executado pelo usuário 'root'.";
   echo "*   Chame-o com o comando 'sudo ./sapl_migracao.sh'.";
   echo "*************************";
   exit 1;
fi

if [ ! -f "$INST_PATH/old/Data.fs" ]; then
   echo "********* ERRO **********";
   echo "*   O arquivo Data.fs da versão anterior do SAPL não está no diretório correto.";
   echo "*   Grave-o em '$INST_PATH/old' e tente novamente.";
   echo "*************************";
   exit 1;
fi
echo "ok... Encontrado arquivo Data.fs"

if [ ! -f "$INST_PATH/old/sapl.sql" ]; then
   echo "********* ERRO **********";
   echo "*   O arquivo de backup do MySQL da versão anterior do SAPL não está no diretório correto.";
   echo "*   Grave-o em '$INST_PATH/old', com o nome 'sapl.sql', e tente novamente.";
   echo "*************************";
   exit 1;
fi
echo "ok... Encontrado arquivo sapl.sql"

# Pára o SAPL, se estiver em execução
kill `ps ax | grep \/sapl\/ | grep \/run.py | cut -d" " -f2`
echo "ok... SAPL parado."

# Acertar a propriedade do arquivo old/Data.fs para que possa ser utilizado pelo zope
chown zope.zope $INST_PATH/old/Data.fs && echo "ok... Ajustado o proprietário do arquivo old/Data.fs"

###################################################################################################
### Importação dos dados do banco relacional (MySQL)

# Preciso de um arquivo apenas com os dados, e com comandos insert que qualifiquem as colunas.
# Vou importar o arquivo de backup para um database temporário, justamente para poder exportar
# os dados em um script no formato necessário.

# cria o database temporario e o carrega com os dados do backup
mysql -uroot -e "create database tmp_sapl_old;" || { echo "Não foi possível criar base de dados temporária 'tmp_sapl_old' no MySQL."; exit 1; }
echo "ok... Criada a base temporária 'tmp_sapl_old' no MySQL."
mysql -uroot tmp_sapl_old <$INST_PATH/old/sapl.sql || { echo "Não foi possível importar o arquivo de backup na base temporária."; exit 1; }
echo "ok... Importado o arquivo de backup na base temporária."

# exporta no formato desejado (apenas dados, inserts com qualificação de colunas)
mysqldump -t -c -uroot tmp_sapl_old > $INST_PATH/old/apenas_dados.sql || { echo "Não foi possível exportar dados a partir da base temporária."; exit 1; }
echo "ok... Dados exportados no formato adequado a partir da base temporária."
# exclui a base de dados temporária
mysql -uroot -e "drop database tmp_sapl_old;" || { echo "Não foi possível apagar a base de dados temporária."; exit 1; }
echo "ok... Base de dados temporária excluída com sucesso."

# recria o banco de dados do sapl21. Antes, faz um backup do banco 'interlegis' existente.
mysqldump -uroot interlegis > $INST_PATH/old/bkp_sapl21.sql || { echo "Não foi possível fazer backup do banco da dados 'interlegis'."; exit 1; }
echo "ok... Backup da base 'interlegis' realizado com sucesso. Foi gravado o arquivo 'bkp_sapl21.sql'."
mysql -uroot -e "drop database interlegis;" || { echo "Não foi possível apagar a base de dados 'interlegis'."; exit 1; }
echo "ok... Base de dados 'interlegis' excluída com sucesso."
mysql -uroot <$INST_PATH/Products/ILSAPL/instalacao/sapl.sql || { echo "Não foi possível recriar base 'interlegis'."; exit 1; }
echo "ok... Base de dados 'interlegis' recriada com sucesso."

# importa para o banco 'interlegis' os dados do backup já em formato apropriado
mysql -uroot interlegis <$INST_PATH/old/apenas_dados.sql || { echo "Não foi possível importar dados para a base 'interlegis'."; exit 1; }
echo "ok... Dados importados para o SAPL com sucesso. Foram adicionados à base 'interlegis'."


###################################################################################################
### Importação e ajuste do ZODB
# Antes de chamar o sapl_migracao.py, parar o Zope (ou verificar se esta parado) e 
# fazer COPIA DE SEGURANCA DO Data.fs e do DocumentosSapl.fs



