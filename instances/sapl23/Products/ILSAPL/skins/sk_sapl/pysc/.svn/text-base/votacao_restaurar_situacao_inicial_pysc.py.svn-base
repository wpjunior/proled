## Script (Python) "votacao_restaurar_situacao_inicial_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=cod_materia
##title=
##

try:
    context.zsql.votacao_restaurar_parlamentar_zsql(cod_materia=cod_materia)
    context.zsql.votacao_restaurar_zsql(cod_materia=cod_materia)
except:
    pass

return 1
