# -*- coding: utf-8 -*-

import urllib
import sys
import os

PORTA = sys.argv[1]
USUARIO = sys.argv[2]
SENHA = sys.argv[3]

#A classe abaixo é utilizada para a autenticação automática durante o processo de instalação

class MyUrlOpener(urllib.FancyURLopener):
    def prompt_user_passwd(self, host, realm):
       return (USUARIO,SENHA)
    def __init__(self, *args):
       urllib.FancyURLopener.__init__(self, *args)

#Define o uso do usuário e da senha sempre que aberta uma URL
urllib._urlopener = MyUrlOpener()

#Tenta importar o XSD
os.system('echo -e \"\\033[1m-> XSD:\\033[m\"')

try:
	urllib.urlopen("http://localhost:%s/sapl/manage_importObject?file=XSD.zexp&set_owner:int=1&username=%s&password=%s"%(PORTA,USUARIO,SENHA))

except Exception,error:
	os.system('echo -e \"\\033[31m-> Falha na importação do XSD!\\033[m\"')
	print str(error)	

os.system('echo -e \"\\033[32m-> XSD importado!\\033[m\"')

#Tenta importar o XSLT
os.system('echo -e \"\\033[1m-> XSLT:\\033[m\"')
try:

	urllib.urlopen("http://localhost:%s/sapl/manage_importObject?file=XSLT.zexp&set_owner:int=1"%PORTA)

except Exception,error:
	os.system('echo -e \"\\033[31m-> Falha na importação do XSLT!\\033[m\"')
	print str(error)	

os.system('echo -e \"\\033[32m-> XSLT importado!\\033[m\"')