<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="ISO-8859-1" indent="yes"/>
    <xsl:variable name="xslt">/XSLT/Editor/SD_GenericEditor.xslt</xsl:variable>
    <xsl:variable name="xslt_v">/XSLT/Editor/SD_GenericViewer.xslt</xsl:variable>
    <xsl:template match="/strdoc">
        <html>
            <head>
                <META Http-Equiv="Cache-Control" Content="no-cache" />
                <META Http-Equiv="Pragma" Content="no-cache" />
                <META Http-Equiv="Expires" Content="Tue, 20 Aug 1996 14:25:27 GMT" />
                <title>Editor de Documento Estruturado</title>
            </head>
            <body>
                <a name="{@id}"></a>
                <center>
                    <h1>StrDoc Editor</h1>
                    <h3><xsl:value-of select="@id"/>(<xsl:value-of select="@type"/>)<a style="text-decoration: none;" href="renderXMLforEditing?xslt={$xslt}"> [Edição] </a><a style="text-decoration: none;" href="renderXMLforEditing?xslt={$xslt_v}"> [Somente Leitura] </a><a style="text-decoration: none;" href="renderXML?xsl=__default__"> [Formato Final] </a></h3>
                </center>
                <hr/>
                <xsl:apply-templates/>
            </body>
        </html>
    </xsl:template>
    <xsl:template match="sde_child">
        <div style="padding:2px 0px 2px 20px;">
            <xsl:variable name="chd_color">
                <xsl:choose>
                    <xsl:when test="@opt='yes'">#CCFFCC</xsl:when>
                    <xsl:otherwise>#FFCCCC</xsl:otherwise>
                </xsl:choose>
            </xsl:variable>
            <a href="renderXMLforEditing?action=CREATE&amp;p_path={@path}&amp;p_type={@type}&amp;p_pos={@pos}&amp;xslt={$xslt}#SDE_TARGET" style="border-style:solid; border-width:1px; font-size: 7pt; font-family: sans-serif; background-color: {$chd_color}; color:black; text-decoration: none; text-transform: uppercase;">+ <xsl:value-of select="@name"/></a>
        </div>
    </xsl:template>
    <xsl:template name="sd_element" match="sd_element">
        <a name="{@id}"></a>
        <div style="padding:5px 0px 0px 20px;">
            <table border="0" celpadding="0" cellspacing="0" width="100%" style="background-color: #FFFFCC;">
                <tr>
                    <td style="background-color: #FFFFCC; height: 12pt; vertical-align: middle; font-family: courier; font-size: 10pt; font-weight: bold; top=0px;"><a style="color: #0000FF; text-decoration: none;" href="renderXMLforEditing?action=EDIT&amp;p_id={@id}&amp;xslt={$xslt}#{@id}"><xsl:value-of select="@type_name"/></a></td>
                    <xsl:if test="@editing='yes'">
                        <td width="10" style="height: 10pt; vertical-align: middle;"><a href="javascript: document.form_edit.submit()"><img height="8" vspace="0" src="/XSLT/Editor/icons/salva.gif" alt="Salvar" title="Salvar" border="0" /></a></td>
                        <td width="5"> </td>
                        <td width="10" style="height: 10pt; vertical-align: middle;"><a href="renderXMLforEditing?xslt={$xslt}#{@id}"><img height="8" vspace="0" src="/XSLT/Editor/icons/volta.gif" alt="Retornar" title="Retornar" border="0" /></a></td>
                        <td width="5"> </td>
                    </xsl:if>
                    <xsl:if test="@up='yes'">
                        <td width="10" style="height: 10pt; vertical-align: middle;"><a href="renderXMLforEditing?action=MOVE_UP&amp;p_path={@path}&amp;p_id={@id}&amp;xslt={$xslt}#{../@id}"><img height="8" vspace="0" src="/XSLT/Editor/icons/seta_up.gif" alt="Acima" title="Acima" border="0" /></a></td>
                        <td width="5"> </td>
                    </xsl:if>
                    <xsl:if test="@down='yes'">
                        <td width="10" style="height: 10pt; vertical-align: middle;"><a href="renderXMLforEditing?action=MOVE_DOWN&amp;p_path={@path}&amp;p_id={@id}&amp;xslt={$xslt}#{../@id}"><img height="8" vspace="0" src="/XSLT/Editor/icons/seta_dn.gif" alt="Abaixo" title="Abaixo" border="0" /></a></td>
                        <td width="5"> </td>
                    </xsl:if>
                    <td width="10" style="height: 10pt; vertical-align: middle;"><a href="renderXMLforEditing?action=CUT&amp;p_path={@path}&amp;p_id={@id}&amp;xslt={$xslt}#{../@id}"><img height="8" vspace="0" src="/XSLT/Editor/icons/recorta.png" alt="Recortar" title="Recortar" border="0" /></a></td>
                    <td width="5"> </td>
                    <td width="10" style="height: 10pt; vertical-align: middle;"><a href="renderXMLforEditing?action=COPY&amp;p_path={@path}&amp;p_id={@id}&amp;xslt={$xslt}#{../@id}"><img height="8" vspace="0" src="/XSLT/Editor/icons/copia.png" alt="Copiar" title="Copiar" border="0" /></a></td>
                    <td width="5"> </td>
                    <xsl:if test="@paste='yes'">
                        <td width="10" style="height: 10pt; vertical-align: middle;"><a href="renderXMLforEditing?action=PASTE&amp;p_path={@path}{@id}/&amp;p_pos=0&amp;xslt={$xslt}#{../@id}"><img height="8" vspace="0" src="/XSLT/Editor/icons/cola.png" alt="Colar" title="Colar" border="0" /></a></td>
                        <td width="5"> </td>
                    </xsl:if>
                    <td width="10" style="height: 10pt; vertical-align: middle;"><a href="renderXMLforEditing?action=DELETE&amp;p_path={@path}&amp;p_id={@id}&amp;xslt={$xslt}#{../@id}"><img height="8" vspace="0" src="/XSLT/Editor/icons/exclui.gif" alt="Excluir" title="Excluir" border="0" /></a></td>
                    <td width="5"> </td>
                </tr>
            </table>
            <xsl:choose>
                <xsl:when test="@editing='yes'">
                    <a name="SDE_TARGET"></a>
                    <form name="form_edit" method="POST" action="renderXMLforEditing#{@id}">
                        <input type="hidden" name="action" value="SAVE"/>
                        <input type="hidden" name="p_path" value="{@path}"/>
                        <input type="hidden" name="p_id" value="{@id}"/>
                        <input type="hidden" name="xslt" value="{$xslt}"/>
                        <xsl:if test="boolean(sde_attr)">
                            <div style="padding:1px 0px 0px 0px;">
                                <table border="0" celpadding="0" cellspacing="0" width="100%" style="background-color: #FFFFCC;">
                                    <tr>
                                        <td width="20"> </td>
                                        <xsl:for-each select="sde_attr">
                                            <td style="background-color: #FFFFCC; height: 11pt; vertical-align: middle; font-family: courier; font-size: 10pt; top=0px;"><xsl:value-of select="@name"/>: <input style="width: 50px;" type="text" name="tat_{@id}" value="{.}"/></td>
                                        </xsl:for-each>
                                    </tr>
                                </table>
                            </div>
                        </xsl:if>
                        <textarea style="width: 99%; height: auto;" name="txa_text">
                            <xsl:value-of select="sde_text"/>
                        </textarea>
                    </form>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:if test="boolean(sde_attr)">
                        <div style="padding:1px 0px 0px 0px;">
                            <table border="0" celpadding="0" cellspacing="0" width="100%" style="background-color: #FFFFCC;">
                                <tr>
                                    <td width="20"> </td>
                                    <xsl:for-each select="sde_attr">
                                        <td style="background-color: #FFFFCC; height: 11pt; vertical-align: middle; font-family: courier; font-size: 10pt; top=0px;">[<xsl:value-of select="@name"/>: <xsl:value-of select="."/>]</td>
                                    </xsl:for-each>
                                </tr>
                            </table>
                        </div>
                    </xsl:if>
                    <xsl:value-of select="sde_text"/>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:apply-templates select="sde_child | sd_element"/>
        </div>
    </xsl:template>	
</xsl:stylesheet>
