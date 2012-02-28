###############################################################################
#
# Copyright (c) 2005 by Interlegis
#
# GNU General Public Licence (GPL)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
#
###############################################################################

from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.CMFCore.utils import getToolByName
from Products.ILSAPL.config import PROJECTNAME, SKINS_DIR, SKIN_NAME, GLOBALS
from StringIO import StringIO
import string


def install(self):
    """
    Instala o produto.
    """

    portal = getToolByName(self, 'portal_url').getPortalObject()
    out = StringIO()

    out.write('Iniciando a instalacao do produto %s.\n' % PROJECTNAME)
    installSkins(self, portal, out)
    out.write('O produto %s foi instalado com sucesso.' % PROJECTNAME)

    return out.getvalue()


def uninstall(self):
    """
    Desinstala o produto.
    """

    portal = getToolByName(self, 'portal_url').getPortalObject()
    out = StringIO()

    out.write('Iniciando a desinstalacao do produto %s.\n' % PROJECTNAME)
    uninstallSkins(self, portal, out)
    out.write('O produto %s foi desinstalado com sucesso.' % PROJECTNAME)

    return out.getvalue()


def installSkins(self, portal, out):
    """
    Instala as skins em portal_skins e regitra os layers correspondentes.
    """

    skins_tool = getToolByName(portal, 'portal_skins')
    skins = skins_tool.getSkinSelections()

    for skin in skins:
        path = skins_tool.getSkinPath(skin)
        path = map(string.strip, string.split(path,','))
        if SKIN_NAME not in path:
            try:
                path.insert(path.index('custom') + 1, SKIN_NAME)
            except ValueError:
                path.append(SKIN_NAME)

            path = string.join(path, ', ')
            skins_tool.addSkinSelection(skin, path)
            out.write('Adicionado %s na skin %s\n' % (SKIN_NAME, skin))
        else:
            out.write('Saltando a skin %s, %s ja esta configurado\n' % (skin, SKIN_NAME))

    skins = skins_tool.getSkinSelections()

    if SKIN_NAME not in skins_tool.objectIds():
        addDirectoryViews(skins_tool, SKINS_DIR, GLOBALS)
        out.write('Adicionado o directory view %s ao portal_skins\n' % SKIN_NAME)
    else:
        out.write('O directory view %s ja existe no portal_skins\n' % SKIN_NAME)


def uninstallSkins(self, portal, out):
    """
    Desinstala as skins de portal_skins e remove os layers correspondentes.
    """

    skins_tool = getToolByName(portal, 'portal_skins')
    skins = skins_tool.getSkinSelections()

    for skin in skins:
        path = skins_tool.getSkinPath(skin)
        path = map(string.strip, string.split(path,','))
        if SKIN_NAME in path:
            path.remove(SKIN_NAME)
            path = string.join(path, ', ')
            skins_tool.addSkinSelection(skin, path)
            out.write('Removido %s da skin %s\n' % (SKIN_NAME, skin))

    if SKIN_NAME in skins_tool.objectIds():
        skins_tool._delObject(SKIN_NAME)
        out.write('Removido %s do portal_skins\n' % SKIN_NAME)

