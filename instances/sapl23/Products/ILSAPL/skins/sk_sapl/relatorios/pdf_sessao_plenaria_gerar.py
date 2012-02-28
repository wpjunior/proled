##parameters=rodape_dic, sessao='', imagem, inf_basicas_dic, lst_mesa, lst_oradores, lst_votacao, lst_expedientes
"""Script para geração do PDF das sessoes plenarias
   Autor: Gustavo Lepri
   versão: 1.0
"""
from trml2pdf import parseString
from cStringIO import StringIO
import time

def cabecalho(inf_basicas_dic,imagem):
    """
    """
    tmp=''
    tmp+='\t\t\t\t<image x="2.1cm" y="25.7cm" width="59" height="62" file="' + imagem + '"/>\n'
    tmp+='\t\t\t\t<lines>2cm 24.5cm 19cm 24.5cm</lines>\n'
    tmp+='\t\t\t\t<setFont name="Helvetica" size="16"/>\n'
    tmp+='\t\t\t\t<drawString x="5cm" y="27.2cm">' + str(inf_basicas_dic["nom_camara"]) + '</drawString>\n'
    tmp+='\t\t\t\t<setFont name="Helvetica" size="14"/>\n'
    tmp+='\t\t\t\t<drawString x="5cm" y="26.5cm">Sistema de Apoio ao Processo Legislativo</drawString>\n'
    tmp+='\t\t\t\t<setFont name="Helvetica" size="14"/>\n'
    tmp+='\t\t\t\t<drawCentredString x="10.5cm" y="25.2cm">' + str(inf_basicas_dic['num_sessao_plen']) + 'ª Sessão ' + str(inf_basicas_dic['nom_sessao']) + ' da ' + str(inf_basicas_dic['num_legislatura']) + 'ª Legislatura </drawCentredString>\n'
    return tmp

def rodape(rodape_dic):
    """
    """
    tmp=''
    linha1 = rodape_dic['end_casa']
    if rodape_dic['end_casa']!="" and rodape_dic['end_casa']!=None:
        linha1 = linha1 + " - "
    if rodape_dic['num_cep']!="" and rodape_dic['num_cep']!=None:
        linha1 = linha1 + "CEP " + rodape_dic['num_cep']
    if rodape_dic['nom_localidade']!="" and rodape_dic['nom_localidade']!=None:
        linha1 = linha1 + " - " + rodape_dic['nom_localidade']
    if rodape_dic['sgl_uf']!="" and rodape_dic['sgl_uf']!=None:
        linha1 = linha1 + " " + rodape_dic['sgl_uf']
    if rodape_dic['num_tel']!="" and rodape_dic['num_tel']!=None:
        linha1 = linha1 + " Tel: "+ rodape_dic['num_tel']
    if rodape_dic['end_web_casa']!="" and rodape_dic['end_web_casa']!=None:
        linha2 = rodape_dic['end_web_casa']
    if rodape_dic['end_email_casa']!="" and rodape_dic['end_email_casa']!=None:
        linha2 = linha2 + " - E-mail: " + rodape_dic['end_email_casa']
    if rodape_dic['data_emissao']!="" and rodape_dic['data_emissao']!=None:
        data_emissao = rodape_dic['data_emissao']

    tmp+='\t\t\t\t<lines>2cm 3.2cm 19cm 3.2cm</lines>\n'
    tmp+='\t\t\t\t<setFont name="Helvetica" size="8"/>\n'
    tmp+='\t\t\t\t<drawString x="2cm" y="3.3cm">' + data_emissao + '</drawString>\n'
    tmp+='\t\t\t\t<drawString x="17.9cm" y="3.3cm">Página <pageNumber/></drawString>\n'
    tmp+='\t\t\t\t<drawCentredString x="10.5cm" y="2.7cm">' + linha1 + '</drawCentredString>\n'
    tmp+='\t\t\t\t<drawCentredString x="10.5cm" y="2.3cm">' + linha2 + '</drawCentredString>\n'

    return tmp

def paraStyle():
    """
    """
    tmp=''
    tmp+='\t<stylesheet>\n'
#    tmp+='\t\t<blockTableStyle id="Standard_Outline">\n'
#    tmp+='\t\t\t<blockAlignment value="LEFT"/>\n'
#    tmp+='\t\t\t<blockValign value="TOP"/>\n'
#    tmp+='\t\t</blockTableStyle>\n'
    tmp+='\t\t<blockTableStyle id="votacao">\n'
    tmp+='\t\t\t<blockBackground colorName="silver" start="0,0" stop="3,0" />\n'
    tmp+='\t\t\t<lineStyle kind="GRID" colorName="silver" />\n'
    tmp +='\t\t\t<blockAlignment value="CENTER"/>\n'
    tmp+='\t\t\t<blockValign value="MIDDLE"/>\n'
    tmp+='\t\t</blockTableStyle>\n'
    tmp+='\t\t<initialize>\n'
    tmp+='\t\t\t<paraStyle name="all" alignment="justify"/>\n'
    tmp+='\t\t</initialize>\n'
    #titulo do parágrafo: é por default centralizado
    tmp+='\t\t<paraStyle name="style.Title" fontName="Helvetica" fontSize="11" leading="13" alignment="RIGHT"/>\n'
    tmp+='\t\t<paraStyle name="P1" fontName="Helvetica-Bold" fontSize="12.0" textColor="silver" leading="14" spaceBefore="6" alignment="LEFT"/>\n'
    tmp+='\t\t<paraStyle name="P2" fontName="Helvetica" fontSize="10.0" leading="10" alignment="LEFT"/>\n'
    tmp+='\t\t<paraStyle name="texto_projeto" fontName="Helvetica" fontSize="12.0" leading="12" spaceAfter="10" alignment="JUSTIFY"/>\n'
    tmp+='\t\t<paraStyle name="numOrdem" alignment="CENTER"/>\n'
    tmp+='\t</stylesheet>\n'

    return tmp

def inf_basicas(inf_basicas_dic):
    """
    """
    tmp=""
    nom_sessao = inf_basicas_dic['nom_sessao']
    num_sessao_plen = inf_basicas_dic["num_sessao_plen"]
    num_legislatura = inf_basicas_dic["num_legislatura"]
    dat_inicio_sessao = inf_basicas_dic["dat_inicio_sessao"]
    hr_inicio_sessao =  inf_basicas_dic["hr_inicio_sessao"]
    dat_fim_sessao = inf_basicas_dic["dat_fim_sessao"]
    hr_fim_sessao = inf_basicas_dic["hr_fim_sessao"]

    #iní­cio das informações basicas
    tmp+='\t\t<para style="P1">Informações Básicas</para>\n'
    tmp+='\t\t<para style="P2">\n'
    tmp+='\t\t\t<font color="white"> </font>\n'
    tmp+='\t\t</para>\n'
    tmp+='\t\t<para style="P2"><b>Tipo: </b> ' + nom_sessao + '</para>\n'
    tmp+='\t\t<para style="P2"><b>Data de inicio: </b> ' + dat_inicio_sessao + '</para>\n'
    tmp+='\t\t<para style="P2"><b>Hora de inicio: </b> ' + hr_inicio_sessao + '</para>\n'
    tmp+='\t\t<para style="P2"><b>Data de termino: </b> ' + dat_fim_sessao + '</para>\n'
    tmp+='\t\t<para style="P2"><b>Hora de termino: </b> ' + hr_fim_sessao + '</para>\n'
 
    return tmp

def mesa(lst_mesa):
    """
    
    """
    tmp=''
    tmp+='\t\t<para style="P1">Mesa Diretora</para>\n'
    tmp+='\t\t<para style="P2">\n'
    tmp+='\t\t\t<font color="white"> </font>\n'
    tmp+='\t\t</para>\n'
    for mesa in lst_mesa:
        tmp+='\t\t<para style="P2"><b>'+ mesa['des_cargo'] +':</b> ' + mesa['nom_parlamentar'] + '/' + mesa['sgl_partido'] +'</para>\n'
    return tmp

def oradores(lst_oradores):
    """
    
    """
    tmp = ''
    tmp+='\t\t<para style="P1">Oradores Inscritos</para>\n'
    tmp+='\t\t<para style="P2">\n'
    tmp+='\t\t\t<font color="white"> </font>\n'
    tmp+='\t\t</para>\n'
    for orador in lst_oradores:
        tmp+='\t\t<para style="P2">'+ str(orador['num_ordem']) +' - ' + orador['nom_parlamentar'] + '</para>\n'
    return tmp

def votacao(lst_votacao):
    """
    """

    tmp = ''
    tmp+='<para style="P1">Materias da Ordem do Dia</para>\n\n'
    tmp+='\t\t<para style="P2">\n'
    tmp+='\t\t\t<font color="white"> </font>\n'
    tmp+='\t\t</para>\n'
    tmp+='<blockTable style="votacao" repeatRows="1" colWidths="4cm,5cm,5cm,4cm">\n'
    tmp+='<tr><td >(Autor/Nº Origem)</td><td >Ementa</td><td >Observacao</td><td>Resultado da Votação</td></tr>\n'
    for votacao in lst_votacao:
        tmp+='<tr><td><para style="numOrdem">' + str(votacao['num_ordem']) + '</para>\n'
        tmp+= '<para>' + votacao['id_materia'] + '</para>\n' + '<para>' + votacao['nom_autor'] +'</para></td>\n'
        tmp+='<td><para>' + votacao['txt_ementa'] + '</para></td>\n'
        tmp+='<td><para>' + votacao['ordem_observacao'] + '</para></td>\n'
        tmp+='<td><para style="numOrdem">' + votacao['nom_resultado'] + '</para></td></tr>\n'
        #tmp+= '<para>' + votacao['votacao_observacao'] +'</para></td></tr>\n'

    tmp+='\t\t</blockTable>\n'
    return tmp

def expedientes(lst_expedientes):
    """
    
    """
    tmp = ''
    tmp+='\t\t<para style="P1">Expedientes</para>\n'
    tmp+='\t\t<para style="P2">\n'
    tmp+='\t\t\t<font color="white"> </font>\n'
    tmp+='\t\t</para>\n'
    for expediente in lst_expedientes:
        tmp+='\t\t<para style="P2"><b>' + expediente['nom_expediente'] +': </b> ' + expediente['txt_expediente'] + '</para>\n'
    return tmp


def principal(cabecalho, rodape, sessao, imagem, inf_basicas_dic):
    """
    """

    arquivoPdf=str(int(time.time()*100))+".pdf"

    tmp=''
    tmp+='<?xml version="1.0" encoding="iso-8859-1" standalone="no" ?>\n'
    tmp+='<!DOCTYPE document SYSTEM "rml_1_0.dtd">\n'
    tmp+='<document filename="relatorio.pdf">\n'
    tmp+='\t<template pageSize="(21cm, 29.7cm)" title="Sessao Plenaria" author="Interlegis" allowSplitting="20">\n'
    tmp+='\t\t<pageTemplate id="first">\n'
    tmp+='\t\t\t<pageGraphics>\n'
    tmp+=cabecalho(inf_basicas_dic,imagem)
    tmp+=rodape(rodape_dic)
    tmp+='\t\t\t</pageGraphics>\n'
    tmp+='\t\t\t<frame id="first" x1="2cm" y1="4cm" width="17cm" height="20.5cm"/>\n'
    tmp+='\t\t</pageTemplate>\n'
    tmp+='\t</template>\n'
    tmp+=paraStyle()
    tmp+='\t<story>\n'
    tmp+=inf_basicas(inf_basicas_dic)
    tmp+=mesa(lst_mesa)
    tmp+=oradores(lst_oradores)
    tmp+=votacao(lst_votacao)
    tmp+=expedientes(lst_expedientes)
    tmp+='\t</story>\n'
    tmp+='</document>\n'
    tmp_pdf=parseString(tmp)

    if hasattr(context.temp_folder,arquivoPdf):
        context.temp_folder.manage_delObjects(ids=arquivoPdf)
    context.temp_folder.manage_addFile(arquivoPdf)
    arq=context.temp_folder[arquivoPdf]
    arq.manage_edit(title='Arquivo PDF temporario.',filedata=tmp_pdf,content_type='application/pdf')

    return "/temp_folder/"+arquivoPdf

return principal(cabecalho, rodape, sessao, imagem, inf_basicas_dic)
