#!/bin/sh

# Script de Instalação - SAPL 2.3
# Adaptado por Gustavo Lepri 29/10/2008
# Nao esta sendo utilizado para instalar o SAPL - 28/05/2009

#Verificando se o usuário é root
if [ $USER != root ];
then echo -e "\n\033[1;31mEste script só funcionará se executado pelo usuário root!\n\033[m";
exit;
else clear;
fi;

#Captura de argumentos

argc=$#

#Ajuda: Informações sobre os argumentos possíveis

ajuda='Script de Instalação do SAPL 2.3\n
\n
./instalar [-h] [-p numerodaporta] [-u usuario_sapl] [-d local]\n
\n
-h			Exibe este texto de ajuda.\n
-p numerodaporta	Permite que seja escolhida a porta para o Zope (a padrão é a 8080).\n
-u numedousuario	Permite que seja escolhido o nome do usuário para o Zope (o padrão é admin).\n
-d local		Permite que seja escolhida a pasta de instalação (a padrão é '/usr/local/interlegis').\n
\n
'

#Parâmetros iniciais

porta=8080;
local=/usr/local/interlegis;
zope_sapl=/sapl23;
usuario_sapl=admin;
senha_sapl=interlegis;
pasta_tmp=/sapl_backup;
pasta_inst=$PWD;
VERSAO_MYSQL='3.23.51';
VERSAO_LIBGDBM='1.8.3';
VERSAO_DB4='4.2.52';
VERSAO_PYTHON='2.3.3';
VERSAO_ZOPE='2.7.0';
VERSAO_WV='1.0.0';

#Análise dos argumentos (falta criticar)

# while [ $1 ];
# 	do if [ $1 == -h ];			#Caso tenha pedido help
# 		then echo -e $ajuda;		#Exibe a ajuda
# 		exit;		 		#Deixa o programa
# 	elif [ $1 == -p ];			#Caso tenha especificado a porta
# 		then shift;
# 		if [ -z $1 -o $1 == '-p' -o $1 == '-d' -o $1 == '-u' ]; #Verifica se realmente especificou
# 			then echo -e '\033[1;31;5mA porta deve ser especificada! (parâmetro -p)\033[m';
# 			exit;
# 		else
# 			test $1 -gt 0 &> /dev/null  	#Verifica se é um número maior que zero
# 			if [ $? != 0 ];
# 				then echo -e '\033[1;31;5mA porta deve ser um número inteiro positivo! (Você digitou "'$1'")\033[m';
# 				exit;
# 			fi;
# 		fi;
# 		porta=$1;			#Coloca o número na variável $porta
# 	elif [ $1 == -u ];			#Caso tenha especificado o usuário
# 		then shift;
# 		if [ -z $1 -o $1 == '-p' -o $1 == '-d' -o $1 == '-u' ]; #Verifica se realmente especificou
# 			then echo -e '\033[1;31;5mO usuário deve ser especificado! (parâmetro -u)\033[m';
# 			exit;
# 		fi;
# 		usuario_sapl=$1;		#Coloca o nome do usuário na variável $usuario_sapl
# 	elif [ $1 == -d ];			#Caso tenha especificado a pasta
# 		then shift;
# 		if [ -z $1 -o $1 == '-p' -o $1 == '-d' -o $1 == '-u' ]; #Verifica se realmente especificou
# 			then echo -e '\033[1;31;5mA pasta destino deve ser especificada! (parâmetro -d)\033[m';
# 			exit;
# 		fi;
# 		if [ ${1:0:1} != '/' ];
# 			then echo -e '\033[1;31;5mDeve-se indicar o caminho completo da pasta! (Você digitou "'$1'", provavelmente deseja instalar em "'/$1'")\033[m';
# 			exit;
# 		fi;
# 		local=$1;			#Coloca na variável $local
# 	else
# 		if [ ${1:0:1} == '-' ];
# 			then echo -e '\033[1;31;5mParâmetro ('$1') inválido!\033[m';
# 		else echo -e '\033[1;31;5mArgumento "'$1'" ignorado!\033[m';
# 		fi;
# 	fi;
# shift;
# done;

#Mostra dados da instalação
echo "\033[7m-\033[4;7mInformações sobre a instalação do SAPL 2.3\033[m\033[7m-\033[m"
echo "\033[1mPorta:\033[m "$porta"   \033[m\t\033[1mUsuário:\033[m "$usuario_sapl
echo "\033[1mLocal:\033[m "$local
echo "\033[7m____________________________________________\033[m"

#Verifica se a porta está disponível

#nc localhost -z -p 1 $porta
#if [ $? == 0 ];
#then echo -e '\033[1;31;5mA porta '$porta' já está sendo usada!\033[m';
#exit;
#fi;

#Variáveis para o script de desinstalação

criouusr=nao
NOVOMYSQL=nao
NOVOMYSQLCLIENT=nao
NOVOJAVA=nao
NOVOFOP=nao
NOVOMYSQLMAX=nao
NOVOLIBPNG=nao
NOVOFREETYPE=nao
NOVOLIBWMF=nao
NOVOWV=nao

#Confere se existe hostname

if [ -z $HOSTNAME ];
then echo '\033[1;31;5mÉ necessário configurar um nome de host!\033[m';
exit;
else echo "\033[34m\n\nIniciando a instalação do SAPL 2.3...\n\033[m\n";
fi;

#Iniciando o contador de progresso

PASSO=1;

#Verificando se o usuário já existe e criando-o se necessário
echo -e '\033[1mPasso '$PASSO': Verificando se o usuário '$usuario_sapl' já existe: \033[m'
let PASSO++;
grep $usuario_sapl /etc/passwd > /dev/null
if [ $? != 0 ];
then echo -e 'Usuário inexistente, tentando criá-lo...';
echo -e '\033[7;5;1mATENÇÂO: Forneça abaixo os dados do usuário '$usuario_sapl'.\033[m';
adduser $usuario_sapl
if [ $? == 0 ];
then echo -e "\033[32m-> Usuário "$usuario_sapl" criado com sucesso! \n\033[m";
else
	echo -e "\033[1;31m-> Problemas ao tentar criar o usuário "$usuario_sapl"! \n\033[m";
	exit;
fi;
else echo -e "\033[32m-> Não foi necessário criar o usuário "$usuario_sapl", ele já existia! \n\033[m";
fi;

#Criando a pasta temporária e a do SAPL 2.3

echo -e '\033[1mPasso '$PASSO': Criando a pasta do SAPL 2.3 e a pasta temporária: \033[m'
let PASSO++;

mkdir -p $local$pasta_tmp

if [ $? == 0 ];
then echo -e "\033[32m-> Pastas local ("$local") e temporária ("$local$pasta_tmp") criadas com sucesso! \n\033[m";
else echo -e "\033[1;31mNão possível criar as seguintes pastas: "$local" e "$local$pasta_tmp"! \nCheque a mensagem a duas linhas acima (mkdir...) para resolver o problema.\033[m";
exit;
fi;

#Instalação dos pacotes

pacotes='libavalon-framework-java libxmlgraphics-commons-java libc6 libdb4.2 libdbd-mysql-perl libdbi-perl libgcc1 libglib1.2ldbl libjaxp1.3-java liblogkit-java libmysqlclient15off libnet-daemon-perl libplrpc-perl libstdc++6 libxalan2-java libxerces2-java libxslt1.1 perl-base perl-modules perl python-imaging t1lib-bin unrtf unzip xpdf zope-cmf1.6 zope-cmfcalendar1.6 zope-cmfcore1.6 zope-cmfdefault1.6 zope-cmftopic1.6 zope-common zope-dcworkflow1.6 zope-extfile mysql-client-5.0 mysql-common mysql-server-5.0 python2.4 wv zope-mysqlda python-trml2pdf'

echo -e '\033[1mPasso '$PASSO': Atualizando a lista de pacotes no repositório: \033[m'
let PASSO++;
apt-get update
if [ $? == 0 ];
then echo -e "\033[32m-> Lista de pacotes atualizados com sucesso! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao atualizar! \n\033[m";
fi;


for pacote in $pacotes; do
    echo -e '\033[1mPasso '$PASSO': Instalando o pacote' $pacote: '\033[m'
    let PASSO++;
    apt-get -y -qq install $pacote
    if [ $? == 0 ];
        then echo -e "\033[32m-> Pacote $pacote instalado com sucesso! \n\033[m";
    else echo -e "\033[1;31m-> Problemas ao tentar instalar $pacote! \n\033[m";
    fi;
done

#Criando instância do Zope para o SAPL
echo -e "\033[1mPasso "$PASSO": Criando instância do Zope para o SAPL 2.3: \033[m"
let PASSO++;
$local/bin/mkzopeinstance.py --dir=$local$zope_sapl --user=$usuario_sapl:$senha_sapl
if [ $? == 0 ];
then echo -e "\033[32m-> Instância criada com sucesso! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar criar a instância Zope! \n\033[m";
fi;

#Instalando o produto PythonModules
echo -e '\033[1mPasso '$PASSO': Instalando o produto PythonModules: \033[m'
let PASSO++;
cp -rf ../$pasta_inst/Products/PythonModules $local$zope_sapl/Products/
if [ $? == 0 ];
then echo -e "\033[32m-> Pacote PythonModules.tar.gz instalado com sucesso! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar instalar PythonModules.tar.gz! \n\033[m";
fi;

#Instalando o produto StructuredDoc
echo -e '\033[1mPasso '$PASSO': Instalando o produto StructuredDoc: \033[m'
let PASSO++;
svn co http://repositorio.interlegis.gov.br/SDE/trunk $local$zope_sapl/Products/StructuredDoc
if [ $? == 0 ];
then echo -e "\033[32m-> Pacote StructuredDoc.tar.gz instalado com sucesso! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar instalar StructuredDoc.tar.gz! \n\033[m";
fi;

#Instalando as extensões
echo -e '\033[1mPasso '$PASSO': Instalando extensões: \033[m'
let PASSO++;
cp -rf ../$pasta_inst/Products/PythonModules $local$zope_sapl/Products/
if [ $? != 0 ];
then echo -e "\033[1;31m-> Problemas ao tentar acessar a pasta "$local$zope_sapl/Extensions"! \n\033[m";
fi;
tar -xzf $pasta_inst/Extensions.tar.gz
if [ $? == 0 ];
then echo -e "\033[32m-> Pacote Extensions.tar.gz instalado com sucesso! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar instalar Extensions.tar.gz! \n\033[m";
fi;

#Alterando Grupo do usuário mysql
echo -e '\033[1mPasso '$PASSO': Alterando Grupo do usuário mysql: \033[m'
let PASSO++;
usermod mysql -g root
if [ $? == 0 ];
then echo -e "\033[32m-> Grupo do usuário mysql alterado com sucesso para root! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar alterar o grupo do usuário mysql para root! \n\033[m";
fi;

#Iniciando as bases de dados e o MySQL
echo -e '\033[1mPasso '$PASSO': Iniciando as bases de dados e o MySQL: \033[m'
let PASSO++;
mysql_install_db
if [ $? == 0 ];
then echo -e "\033[32m-> Bases de dados do MySQL iniciadas com sucesso! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar iniciar as bases de dados do MySQL! \n\033[m";
fi;
cp $pasta_inst/my.cnf /etc
if [ $? != 0 ];
then echo -e "\033[1;31m-> Problemas ao tentar copiar a pasta "$pasta_inst"/my.cnf para /etc! \n\033[m";
fi;
mysqld_safe &
if [ $? == 0 ];
then echo -e "\033[32m-> MySQL iniciado com sucesso! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar iniciar o MySQL! \n\033[m";
fi;

#Copiando o zope.conf
echo -e '\033[1mPasso '$PASSO': Copiando o zope.conf: \033[m'
let PASSO++;
cp $pasta_inst/zope.conf $local$zope_sapl/etc
if [ $? == 0 ];
then echo -e "\033[32m-> Arquivo zope.conf copiado com sucesso para "$local$zope_sapl"/etc! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar copiar o arquivo zope.conf para "$local$zope_sapl"/etc! \n\033[m";
fi;

#Adaptando o arquivo zope.conf aos parâmetros passados
echo -e '\033[1mPasso '$PASSO': Adaptando o arquivo zope.conf aos parâmetros passados: \033[m'
let PASSO++;
CONF=0;
cd $local$zope_sapl/etc
if [ $? != 0 ];
then CONF=$?;
fi;

head -n 13 zope.conf > z
if [ $? != 0 ];
then CONF=$?;
fi;
echo -e "%define INSTANCE "$local$zope_sapl >> z

tail -n 830 zope.conf | head -n 124 >> z
if [ $? != 0 ];
then CONF=$?;
fi;

echo -e "effective-user "$usuario_sapl >> z
if [ $? != 0 ];
then CONF=$?;
fi;

tail -n 705 zope.conf | head -n 626 >> z
if [ $? != 0 ];
then CONF=$?;
fi;

echo -e "address "$porta >> z
if [ $? != 0 ];
then CONF=$?;
fi;

tail -n 78 zope.conf >> z
if [ $? != 0 ];
then CONF=$?;
fi;

chmod 777 zope.conf
if [ $? != 0 ];
then CONF=$?;
fi;

rm -f zope.conf > /dev/null
if [ $? != 0 ];
then CONF=$?;
fi;

chmod 777 z
if [ $? != 0 ];
then CONF=$?;
fi;

mv z zope.conf
if [ $? != 0 ];
then CONF=$?;
fi;

if [ $CONF == 0 ];
then echo -e "\033[32m-> Arquivo zope.conf adaptado aos parêmetros passados! \n\033[m";
else echo -e "\033[1;31m-> Erro na adaptação do arquivo zope.conf aos parâmetros passados! \n\033[m";
fi;

#Atualizando base de dados do MySQL com dados do SAPL
echo -e '\033[1mPasso '$PASSO': Atualizando base de dados do MySQL com dados do SAPL: \033[m'
let PASSO++;
mysql -u root < $pasta_inst/sapl.sql
if [ $? == 0 ];
then echo -e "\033[32m-> Base de dados so MySQL atualizada com sucesso! \n\033[m";
else echo -e "\033[1;31m-> Problemas na atualização da base de dados do MySQL! \n\033[m";
fi;

#Reiniciando o MySQL para as novas permissões
echo -e '\033[1mPasso '$PASSO': Reiniciando o MySQL para as novas permissões: \033[m'
let PASSO++;
/etc/init.d/mysql restart
if [ $? == 0 ];
then echo -e "\033[32m-> MySQL reiniciado com sucesso! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar reiniciar o MySQL! \n\033[m";
fi;

#Alterando permissões para o usuário
echo -e '\033[1mPasso '$PASSO': Alterando permissões para o usuário '$usuario_sapl': \033[m'
let PASSO++;
cd $local$zope_sapl
if [ $? != 0 ];
then echo -e "\033[1;31m-> Problemas ao tentar acessar a pasta "$local$zope_sapl"! \n\033[m";
fi
chown -R $usuario_sapl.$usuario_sapl *
if [ $? == 0 ];
then echo -e "\033[32m-> O dono do conteúdo da pasta "$local$zope_sapl" agora é "$usuario_sapl". \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar alterar o dono do conteúdo da pasta "$local$zope_sapl" para "$usuario_sapl"! \n\033[m";
fi;
chmod o+t var
if [ $? == 0 ];
then echo -e "\033[32m-> Permissões da pasta var alteradas com sucesso! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar alterar as permissões da pasta var! \n\033[m";
fi;

#Criando a pasta temporária
echo -e '\033[1mPasso '$PASSO': Criando a pasta temporária: \033[m'
let PASSO++;
cd var
if [ $? != 0 ];
then echo -e "\033[1;31m-> Problemas ao tentar acessar a pasta var! \n\033[m";
fi;
mkdir tmp
if [ $? == 0 ];
then echo -e "\033[32m-> Pasta temporária criada com sucesso! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar criar a pasta temporária! \n\033[m";
fi;

#Alterando as permissões da pasta temporária para o usuário
echo -e '\033[1mPasso '$PASSO': Alterando as permissões da pasta temporária para o usuário '$usuario_sapl': \033[m'
let PASSO++;
chown -R $usuario_sapl.$usuario_sapl tmp
if [ $? == 0 ];
then echo -e "\033[32m-> O dono do conteúdo da pasta temporária agora é "$usuario_sapl". \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar alterar o dono do conteúdo da pasta temporária para "$usuario_sapl"! \n\033[m";
fi;
chmod 700 tmp
if [ $? == 0 ];
then echo -e "\033[32m-> Permissões da pasta temporária alteradas com sucesso! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar alterar as permissões da pasta temporária! \n\033[m";
fi;

#Alterando as permissões da pasta de log do Zope
echo -e '\033[1mPasso '$PASSO': Alterando as permissões da pasta de log do Zope '$local$zope_sapl/log: '\033[m'
let PASSO++;
chmod -R 777 $local$zope_sapl/log
if [ $? == 0 ];
then echo -e "\033[32m-> Permissões da pasta de log do Zope alteradas com sucesso! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar alterar as permissões da pasta de log do Zope! \n\033[m";
fi;

#Alterando as permissões da pasta var do Zope
echo -e '\033[1mPasso '$PASSO': Alterando as permissões da pasta var do Zope '$local$zope_sapl/var: '\033[m'
let PASSO++;
chmod -R 777 $local$zope_sapl/var
if [ $? == 0 ];
then echo -e "\033[32m-> Permissões da pasta var do Zope alteradas com sucesso! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar alterar as permissões da pasta var do Zope! \n\033[m";
fi;

#Criando links para os produtos de /usr/share/zope/Products
echo -e '\033[1mPasso: '$PASSO': Criando links para os produtos de /usr/share/zope/Products:\033[m'
let PASSO++;
cd $local$zope_sapl/Products
if [ $? != 0 ];
then echo -e "\033[1;31m-> Problemas ao tantar acessar a pasta "$local$zope_sapl/Produtcs"! \n\033[m";
fi;
ln -s /usr/share/zope/Products/CMFCore\:1.6/ CMFCore
if [ $? == 0 ];
then echo -e "\033[32m-> Link para o CMFCore criado! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar criar o link para o CMFCore! \n\033[m";
fi;
ln -s /usr/share/zope/Products/CMFCalendar\:1.6/ CMFCalendar
if [ $? == 0 ];
then echo -e "\033[32m-> Link para o CMFCalendar criado! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar criar o link para o CMFCalendar! \n\033[m";
fi;
ln -s /usr/share/zope/Products/CMFDefault\:1.6/ CMFDefault
if [ $? == 0 ];
then echo -e "\033[32m-> Link para o CMFDefault criado! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar criar o link para o CMFDefault! \n\033[m";
fi;
ln -s /usr/share/zope/Products/CMFTopic\:1.6/ CMFTopic
if [ $? == 0 ];
then echo -e "\033[32m-> Link para o CMFTopic criado! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar criar o link para o CMFTopic! \n\033[m";
fi;
ln -s /usr/share/zope/Products/DCWorkflow\:1.6/ DCWorkflow
if [ $? == 0 ];
then echo -e "\033[32m-> Link para o DFWorkflow criado! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar criar o link para o DFWorkflow! \n\033[m";
fi;
ln -s /usr/share/zope/Products/GenericSetup/ GenericSetup
if [ $? == 0 ];
then echo -e "\033[32m-> Link para o ExtFile criado! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar criar o link para o ExtFile! \n\033[m";
fi;
ln -s /usr/share/zope/Products/ZMySQLDA/ ZMySQLDA
if [ $? == 0 ];
then echo -e "\033[32m-> Link para o ExtFile criado! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar criar o link para o ExtFile! \n\033[m";
fi;
ln -s /usr/share/zope/Products/CMFActionIcons\:1.6/ CMFActionIcons
if [ $? == 0 ];
then echo -e "\033[32m-> Link para o ExtFile criado! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar criar o link para o ExtFile! \n\033[m";
fi;
ln -s /usr/share/zope/Products/CMFSetup\:1.6/ CMFSetup
if [ $? == 0 ];
then echo -e "\033[32m-> Link para o ExtFile criado! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar criar o link para o ExtFile! \n\033[m";
fi;
ln -s /usr/share/zope/Products/CMFUid\:1.6/ CMFUid
if [ $? == 0 ];
then echo -e "\033[32m-> Link para o ExtFile criado! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar criar o link para o ExtFile! \n\033[m";
fi;

#Iniciando e finalizando o Zope pela primeira vez
echo -e '\033[1mPasso '$PASSO': Iniciando e finalizando o Zope pela primeira vez: \033[m'
let PASSO++;
/etc/init.d/zope2.9 start
if [ $? == 0 ];
then echo -e "\033[32m-> Zope iniciado com sucesso! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar iniciar o Zope! \n\033[m";
fi;
/etc/init.d/zope2.9 stop
if [ $? == 0 ];
then echo -e "\033[32m-> Zope finalizado com sucesso! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar finalizar o Zope! \n\033[m";
fi;

#Criando a conta do administrador do Zope
echo -e '\033[1mPasso '$PASSO': Criando a conta do administrador do Zope: \033[m'
let PASSO++;
$local$zope_sapl/bin/zopectl adduser $usuario_sapl $senha_sapl
if [ $? == 0 ];
then echo -e "\033[32m-> Conta criada! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar criar a conta do administrador! \n\033[m";
fi;

#Instalando o produto TextIndexNG2-2.0.7
echo -e '\033[1mPasso '$PASSO': Instalando o produto TextIndexNG2-2.0.7 (2 pacotes): \033[m'
let PASSO++;
cd $local$zope_sapl/Products
tar -xzf $pasta_inst/TextIndexNG2.tar.gz
if [ $? == 0 ];
then echo -e "\033[32m-> Pacote TextIndexNG2.tar.gz instalado com sucesso! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar instalar TextIndexNG2.tar.gz! \n\033[m";
fi;
#chown -R $usuario_sapl.$usuario_sapl *

#Iniciando novamente o Zope, agora com a base de dados do SAPL2.1
echo -e '\033[1mPasso '$PASSO': Iniciando novamente o Zope, agora com a base de dados do SAPL2.3: \033[m'
let PASSO++;
cd $local$zope_sapl/bin
./runzope >& firststart.log &
if [ $? == 0 ];
then echo -e "\033[32m-> Zope iniciado com sucesso! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar iniciar o Zope! \n\033[m";
fi;

#Removendo o arquivo inituser para que seja possível alterar a senha do administrador do Zope
echo -e '\033[1mPasso '$PASSO': Removendo o arquivo inituser para que seja possível alterar a senha do administrador do Zope: \033[m'
let PASSO++;
rm -f $local$zope_sapl/inituser
if [ $? == 0 ];
then echo -e "\033[32m-> Arquivo "$local$zope_sapl/inituser" removido com sucesso! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar remover o arquivo "$local$zope_sapl/inituser"! \n\033[m";
fi;

#Informando senha e usuário
echo -e "\033[7m---\033[m\033[7;4;5mATENÇÃO\033[m\033[7m: Nome do usuário e senha para acesso ao Zope--\033[m"
echo -e "\033[1m\tUsuário:\033[m "$usuario_sapl"\t\033[1mSenha:\033[m "$senha_sapl
echo -e "\033[7m_________________________________________________________\033[m"
echo -e "\033[1;34mVisando a seguranca dos dados do sistema, recomendamos que a senha do "$usuario_sapl" seja alterada.\033[m\n\n"

#Importando o XSD, o XSLT e o SAPL para o Zope
echo -e '\033[1mPasso '$PASSO': Importando o XSD e o XSLT para o Zope: \033[m'
let PASSO++;
cp $pasta_inst/*.zexp $local$zope_sapl/import
chmod 777 $local$zope_sapl/Products/TextIndexNG2/Stopwords.py
chmod -R 777 $local$zope_sapl/Products/TextIndexNG2/interfaces
sleep 10
python $pasta_inst/imports.py $porta $usuario_sapl $senha_sapl
if [ $? == 0 ];
then echo -e "\033[1;32m\n-> XSD e XSLT importados com sucesso! \n\033[m";
else echo -e "\033[1;31m-> Problemas ao tentar importar o XSD e o XSLT para o Zope! \n\033[m";
fi;

echo -e "\n\n\033[5;32;1;40m-> SAPL 2.3 instalado com sucesso!\033[m \n\n\n"
