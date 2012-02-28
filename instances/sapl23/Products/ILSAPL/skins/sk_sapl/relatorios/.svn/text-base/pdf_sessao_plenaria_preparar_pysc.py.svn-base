import os

request=context.REQUEST
response=request.RESPONSE
session= request.SESSION

if context.REQUEST['data']!='':
    dat_sessao = context.REQUEST['data']
    pauta = [] # lista contendo a pauta da ordem do dia a ser impressa    
    data = context.pysc.data_converter_pysc(dat_sessao) # converte data para formato yyyy/mm/dd

    # seleciona as matérias que compõem a pauta na data escolhida
    for sessao in context.zsql.sessao_plenaria_obter_zsql(dat_sessao=data, ind_excluido=0):
        inf_basicas_dic = {} # dicionário que armazenará as informacoes basicas da sessao plenaria 
        # seleciona o tipo da sessao plenaria
        tipo_sessao = context.zsql.tipo_sessao_plenaria_obter_zsql(tip_sessao=sessao.tip_sessao,ind_excluido=0)[0]
        inf_basicas_dic["nom_sessao"] = tipo_sessao.nom_sessao
        inf_basicas_dic["num_sessao_plen"] = sessao.num_sessao_plen
        inf_basicas_dic["nom_sessao"] = tipo_sessao.nom_sessao
        inf_basicas_dic["num_legislatura"] = sessao.num_legislatura
        inf_basicas_dic["dat_inicio_sessao"] = sessao.dat_inicio_sessao
        inf_basicas_dic["hr_inicio_sessao"] = sessao.hr_inicio_sessao
        inf_basicas_dic["dat_fim_sessao"] = sessao.dat_fim_sessao
        inf_basicas_dic["hr_fim_sessao"] = sessao.hr_fim_sessao
 
        # Lista da composicao da mesa diretora
        lst_mesa = []
        for composicao in context.zsql.composicao_mesa_sessao_obter_zsql(cod_sessao_plen=sessao.cod_sessao_plen,ind_excluido=0):
            for parlamentar in context.zsql.parlamentar_obter_zsql(cod_parlamentar=composicao.cod_parlamentar, ind_excluido=0):
                for cargo in context.zsql.cargo_mesa_obter_zsql(cod_cargo=composicao.cod_cargo, ind_excluido=0):
                    dic_mesa = {}
                    dic_mesa['nom_parlamentar'] = parlamentar.nom_parlamentar
                    dic_mesa['sgl_partido'] = parlamentar.sgl_partido
                    dic_mesa['des_cargo'] = cargo.des_cargo
                    lst_mesa.append(dic_mesa)
        
        # Lista dos oradores
        lst_oradores = []
        for orador in context.zsql.oradores_obter_zsql(cod_sessao_plen=sessao.cod_sessao_plen, ind_excluido=0):
            for parlamentar in context.zsql.parlamentar_obter_zsql(cod_parlamentar=orador.cod_parlamentar, ind_excluido=0):
                dic_oradores = {}
                dic_oradores["num_ordem"] = orador.num_ordem
                dic_oradores["nom_parlamentar"] = parlamentar.nom_parlamentar
                lst_oradores.append(dic_oradores)
        
        # Lista das matérias da Ordem do Dia, incluindo o resultado das votacoes
        lst_votacao=[]
        for votacao in context.zsql.votacao_ordem_dia_obter_zsql(dat_ordem = data, ind_excluido=0):
        
            # seleciona os detalhes de uma matéria
            materia = context.zsql.materia_obter_zsql(cod_materia=votacao.cod_materia)[0]

            dic_votacao = {}
            dic_votacao["num_ordem"] = votacao.num_ordem
            dic_votacao["id_materia"] = materia.sgl_tipo_materia+" "+str(materia.num_ident_basica)+" "+str(materia.ano_ident_basica)+" - "+materia.des_tipo_materia
            dic_votacao["txt_ementa"] = materia.txt_ementa
            dic_votacao["ordem_observacao"] = votacao.ordem_observacao
            dic_votacao["nom_autor"] = ''
            autoria = context.zsql.autoria_obter_zsql(cod_materia=votacao.cod_materia, ind_primeiro_autor=1)        
            if len(autoria) > 0: # se existe autor
                autoria = autoria[0]
                autor = context.zsql.autor_obter_zsql(cod_autor=autoria.cod_autor)
                if len(autor) > 0:
                    autor = autor[0]
            
                if autor.des_tipo_autor == "Parlamentar":
                    parlamentar = context.zsql.parlamentar_obter_zsql(cod_parlamentar=autor.cod_parlamentar)[0]     
                    dic_votacao["nom_autor"] = parlamentar.nom_parlamentar
                elif autor.des_tipo_autor == "Comissao":
                    comissao = context.zsql.comissao_obter_zsql(cod_comissao=autor.cod_comissao)[0]
                    dic_votacao["nom_autor"] = comissao.nom_comissao
                else:
                    dic_votacao["nom_autor"] = autor.nom_autor
            
            if votacao.tip_resultado_votacao:
                resultado = context.zsql.tipo_resultado_votacao_obter_zsql(tip_resultado_votacao=votacao.tip_resultado_votacao, ind_excluido=0)
                for i in resultado:
                    dic_votacao["nom_resultado"] = i.nom_resultado
                    if votacao.votacao_observacao:
                        dic_votacao["votacao_observacao"] = votacao.votacao_observacao
#                    else:
#                        dic_votacao["votacao_observacao"] = ""
            else:
                dic_votacao["nom_resultado"] = "Matéria não votada"
                dic_votacao["votacao_observacao"] = "Vazio"
            lst_votacao.append(dic_votacao)

        lst_expedientes = []
        dic_expedientes = None
        for tip_expediente in context.zsql.tipo_expediente_obter_zsql():
            for expediente in context.zsql.expediente_obter_zsql(cod_sessao_plen=sessao.cod_sessao_plen,cod_expediente=tip_expediente.cod_expediente, ind_excluido=0):
                dic_expedientes = {}
                dic_expedientes["nom_expediente"] = tip_expediente.nom_expediente
                dic_expedientes["txt_expediente"] = expediente.txt_expediente
            if dic_expedientes:
                lst_expedientes.append(dic_expedientes)

    # obtém as propriedades da casa legislativa para montar o cabeçalho e o rodapé da página
    cabecalho={}

    # tenta buscar o logotipo da casa LOGO_CASA
    if hasattr(context.sapl_documentos.props_sapl,'logo_casa.gif'):
        imagem = context.sapl_documentos.props_sapl['logo_casa.gif'].absolute_url()
    else:
        imagem = context.imagens.absolute_url() + "/brasao_transp.gif"
    
    #Abaixo é gerado o dic do rodapé da página (linha 7)
    casa={}
    aux=context.sapl_documentos.props_sapl.propertyItems()
    for item in aux:
        casa[item[0]]=item[1]
    localidade=context.zsql.localidade_obter_zsql(cod_localidade=casa["cod_localidade"])
    data_emissao= DateTime().strftime("%d/%m/%Y")
    rodape= casa
    rodape['data_emissao']= data_emissao

    inf_basicas_dic['nom_camara']= casa['nom_casa']
    REQUEST=context.REQUEST
    for local in context.zsql.localidade_obter_zsql(cod_localidade = casa['cod_localidade']):
        rodape['nom_localidade']= "   "+local.nom_localidade
        rodape['sgl_uf']= local.sgl_uf

#    return lst_votacao
    sessao=session.id
    caminho = context.pdf_sessao_plenaria_gerar(rodape, sessao, imagem, inf_basicas_dic, lst_mesa, lst_oradores, lst_votacao, lst_expedientes)
    if caminho=='aviso':
        return response.redirect('mensagem_emitir_proc')
    else:
       response.redirect(caminho)
