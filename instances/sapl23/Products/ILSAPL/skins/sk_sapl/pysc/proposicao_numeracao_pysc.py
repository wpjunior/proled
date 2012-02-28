## Script (Python) "proposicao_numeracao_pysc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=cod_proposicao
##title=
##

''' Script para a verifica��o do n�mero da proposi��o e inclus�o de um novo.'''
''' Faz a inclus�o por tipo e ano da proposi��o. '''

# Obt�m o proximo "num_proposicao" do tipo de proposicao que est� sendo inclu�da ----- 31/08/2010


# Define o ano corrente
ano_corrente = DateTime().year()

# Busca a proposi��o
tip_proposicao = context.zsql.proposicao_obter_tipo_zsql(cod_proposicao = cod_proposicao)[0].tip_proposicao

# Busca a �ltima numera��o + 1 do mesmo tipo que est� sendo inclu�da no ano
num_proposicao = context.zsql.proposicao_ultima_numeracao_obter_zsql(tip_proposicao = tip_proposicao, ano = ano_corrente)[0].num_proposicao

# ano_ultima_num = context.zsql.proposicao_ano_ult_numeracao_obter_zsql(num_proposicao = ultima_numeracao.num_proposicao)[0]

# Compara o ano e caso seja diferente, recome�a a numera��o
# if int(ano_ultima_num.dat_recebimento) != (ano_corrente):
#    numeracao = 0001
# else:
#    numeracao = ultima_numeracao.num_proposicao + 1

context.zsql.proposicao_incluir_numeracao_zsql(cod_proposicao = cod_proposicao, num_proposicao = num_proposicao)

return 1
