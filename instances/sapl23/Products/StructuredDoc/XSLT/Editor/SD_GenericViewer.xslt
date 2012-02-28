<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="ISO-8859-1" indent="yes"/>
    <xsl:variable name="xslt">/XSLT/Editor/SD_GenericEditor.xslt</xsl:variable>
    <xsl:variable name="xslt_v">/XSLT/Editor/SD_GenericViewer.xslt</xsl:variable>
    <xsl:template match="/strdoc">
        <html>
            <head>
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
    <xsl:template name="sd_element" match="sd_element">
        <a name="{@id}"></a>
        <div style="padding:5px 0px 0px 20px;">
            <table border="0" celpadding="0" cellspacing="0" width="100%" style="background-color: #FFFFCC;">
                <tr>
                    <td style="color: #0000FF; text-decoration: none; background-color: #FFFFCC; height: 12pt; vertical-align: middle; font-family: courier; font-size: 10pt; font-weight: bold; top=0px;"><xsl:value-of select="@type_name"/></td>
                </tr>
            </table>
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
            <xsl:apply-templates select="sd_element"/>
        </div>
    </xsl:template>	
</xsl:stylesheet>
