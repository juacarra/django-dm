#!/usr/bin/env python
# -*- coding: utf-8 -*-

# dlgAplicacion -- Permite crear y modificar una aplicacion de Django.
#                 
                 
# (c) Juan Carrasco 2008
# juacarrag@gmail.com

# This file is part of Django-DM.
#
# Django-DM is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Django-DM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


import gtk

from lib.GladeConnect import *

from lib.dialogos import dlgAviso, dlgError

class dlgAplicacion(GladeConnect):
    def __init__(self, nombre=None, padre=None):
        GladeConnect.__init__(self, 'glade/principal.glade','dlgAplicacion')
        
        if padre is None:
            self.padre = self.dlgAplicacion
        else:
            self.padre = padre
        
        self.dlgAplicacion.set_transient_for(padre)

    def on_btnAceptar_clicked(self, *args):
        self.on_dlgAplicacion_destroy()

    def on_btnCancelar_clicked(self, *args):
        self.on_dlgAplicacion_destroy()
        
    def on_dlgAplicacion_destroy(self, *args):
        self.salir()
        
    def salir(self):
        if __name__ == '__main__':
            gtk.main_quit()
        else:
            self.dlgAplicacion.hide()
        
if __name__ == '__main__':
    app = dlgAplicacion()
    gtk.main()
        
