## Script (Python) "relatoria_atual_obter_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=codigo="", data=""
##title=
##
"""
  Fun��o: retornar a relatoria atual: cod_parlamentar e dat_designacao do parlamentar na composi��o da Comiss�o
  
  Argumento: Dados: codigo=cod_parlamentar, data=dat_desig_relator

"""  

import string

x=str(codigo) + ' - ' + str(data)

return x



