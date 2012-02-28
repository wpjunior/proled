## Script (Python) "data_converter_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=data
##title=
##
"""
  Funcaoo: Converter a data do formato DD/MM/AAAA para
          o formato AAAA/MM/DD, e depois converter em dia da semana
          Ex: sexta-feira.
  
  Argumento: Data a ser convertida.
  
  Retorno: Dia da semana.
"""

diasemana=['Domingo','Segunda-feira','Terça-feira','Quarta-feira','Quinta-feira','Sexta-feira','Sábado']

if data != '':
    data=data[6:] + '/' + data[3:5] + '/' + data[0:2]
    dia=DateTime(data)
    dia_semana = DateTime.dow(dia)
    return diasemana[dia_semana]
else:
   return ''
