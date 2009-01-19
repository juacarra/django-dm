#!/usr/bin/env python
# -*- coding: utf-8 -*-

# dlgProyecto -- Permite configurar el archivo settings.py de un proyecto
#                de Django. 
                 
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
import lib.SimpleTree

import lib.comandos

from lib.dialogos import dlgAviso, dlgError

from lib.constantes import LANGUAGES
from lib.escribe_settings import escribe

(
NAME,
DEBUG,
ADMINS,
DATABASE_ENGINE ,           
DATABASE_NAME,            
DATABASE_USER,          
DATABASE_PASSWORD,        
DATABASE_HOST,            
DATABASE_PORT,
TIME_ZONE,
LANGUAGE_CODE,
MEDIA_ROOT
) = range(0,12)

class dlgProyecto(GladeConnect):
    def __init__(self, nombre=None, path=None, padre=None):
        GladeConnect.__init__(self, 'glade/principal.glade','dlgProyecto')
        self.path = path
        
        self.crea_columna_clase()
        
        if padre is None:
            self.padre = self.dlgProyecto
        else:
            self.padre = padre
        
        self.dlgProyecto.set_transient_for(padre)
         
        if self.path is not None and nombre is not None:
            self.entRuta.set_sensitive(False)
            self.entRuta.set_text(path)
            self.btnRuta.set_sensitive(False)
            self.entNombre.set_sensitive(False)
            self.entNombre.set_text(nombre)
            self.dlgProyecto.set_title("Proyecto: %s" % nombre)
            self.carga_datos()           
        else:
            self.dlgProyecto.set_title("Proyecto: ...")
            self.chkDebug.set_active(True)
            self.cboIdioma.set_active(8)
            self.cboEngine.set_active(0)
            self.cboZonaHoraria.set_active(0)
        
        self.verifica_guardar()
    
    def carga_datos(self):
        sys.path.append(self.path )
        
        import settings
        reload(settings)
        
        print settings.DATABASE_USER, settings.DATABASE_PASSWORD, settings.MEDIA_ROOT 
        
        modelo = self.lvwAdmin.get_model()
        for admin in settings.ADMINS:
            modelo.append(admin)
        
        for key, value in LANGUAGES.iteritems():
            if value == settings.LANGUAGE_CODE:
                self.busca_combo(self.cboIdioma, key)
                
        self.busca_combo(self.cboZonaHoraria, settings.TIME_ZONE)
        self.busca_combo(self.cboEngine, settings.DATABASE_ENGINE)
        self.entMedia.set_text(settings.MEDIA_ROOT)
        self.entHost.set_text(settings.DATABASE_HOST)
        self.entPort.set_text(settings.DATABASE_PORT)
        self.entDataBase.set_text(settings.DATABASE_NAME)
        self.entUser.set_text(settings.DATABASE_USER)
        self.entPass.set_text(settings.DATABASE_PASSWORD)
        
        sys.path.remove(self.path)
        del(settings)
    
    def busca_combo(self, combo, compara):
        cont = 0
        for dato in combo.get_model():
           
            if dato[0] == compara:
                combo.set_active(cont)
            cont += 1
    
    def crea_columna_clase(self):
        self.lvwAdmin.set_rules_hint(True)
        columnas = []
        columnas.append([0 ,'Nombre','str',None,True])
        columnas.append([1 ,'E-Mail','str',None,True])
        modelo = gtk.ListStore(*((2)*[str]))
        lib.SimpleTree.GenColsByModel(modelo, columnas, self.lvwAdmin)
            
    
    def verifica_guardar(self):
        if self.entNombre.get_text() == "":
            self.btnAceptar.set_sensitive(False)
        elif self.entDataBase.get_text() == "":
            self.btnAceptar.set_sensitive(False)
        elif self.entRuta.get_text() == "":
            self.btnAceptar.set_sensitive(False)
        elif self.cboEngine.get_active_text() <> 'sqlite3':
            if self.entUser.get_text() == "":
                self.btnAceptar.set_sensitive(False)
            #elif self.entPass.get_text() == "":
            #    self.btnAceptar.set_sensitive(False)
            elif self.entHost.get_text() == "":
                self.btnAceptar.set_sensitive(False)
            elif self.entPort.get_text() == "":
                self.btnAceptar.set_sensitive(False)
            else:
                self.btnAceptar.set_sensitive(True)
        else:
            self.btnAceptar.set_sensitive(True)
        
    def on_ent_changed(self, *args):
        self.verifica_guardar()
        
    def on_cboEngine_changed(self, *args):
        self.btnProbarCnx.set_sensitive(True)
            
        if self.cboEngine.get_active_text() == 'mysql':
            self.entPort.set_text('3306')
            
        elif self.cboEngine.get_active_text() == 'postgresql':
            self.entPort.set_text('5432')
            
        elif self.cboEngine.get_active_text() == 'postgresql_psycopg2':
            self.entPort.set_text('5432')
            
        elif self.cboEngine.get_active_text() == 'oracle':
            self.entPort.set_text('0')
            self.btnProbarCnx.set_sensitive(False)
            
        if self.cboEngine.get_active_text() == 'sqlite3':
            self.entUser.set_sensitive(False)
            self.entPass.set_sensitive(False)
            self.entHost.set_sensitive(False)
            self.entPort.set_sensitive(False)
            self.btnProbarCnx.set_sensitive(False)
            self.entUser.set_text('')
            self.entPass.set_text('')
            self.entHost.set_text('')
            self.entPort.set_text('')    
        else:
            self.entUser.set_sensitive(True)
            self.entPass.set_sensitive(True)
            self.entHost.set_sensitive(True)
            self.entPort.set_sensitive(True)
            self.entHost.set_text('127.0.0.1')
        
    def on_tbtnAnadir_clicked(self, *args):
        modelo = self.lvwAdmin.get_model()
        modelo.append(['Nombre', 'E-Mail'])
        
    def on_tbtnQuitar_clicked(self, *args):
        modelo, it = self.lvwAdmin.get_selection().get_selected()
        if modelo is None or it is None:
            return
        modelo.remove(it)

    def on_btnMedia_clicked(self, *args):
        dlg = fcdDirectorio(self.dlgProyecto)
        response = dlg.fcdDirectorio.run()
        if response == gtk.RESPONSE_OK:
            self.entMedia.set_text(dlg.fcdDirectorio.get_filename())
    
    def on_btnRuta_clicked(self, *args):
        dlg = fcdDirectorio(self.dlgProyecto)
        response = dlg.fcdDirectorio.run()
        if response == gtk.RESPONSE_OK:
            self.entRuta.set_text(dlg.fcdDirectorio.get_filename())
            
            self.path = "%s/%s" % (dlg.fcdDirectorio.get_filename(),
                                   self.entNombre.get_text())
    
    def on_btnCancelar_clicked(self, *args):
        self.on_dlgProyecto_destroy()
        
    def on_btnAceptar_clicked(self, *args):
        modelo = self.lvwAdmin.get_model()
        admins = []
        for persona in modelo:
            admins.append((persona[0],persona[1]))

        self.dic = {
            NAME:self.entNombre.get_text(),
            DEBUG:self.chkDebug.get_active(),
            ADMINS:(admins),
            DATABASE_ENGINE:self.cboEngine.get_active_text() ,           
            DATABASE_NAME:self.entDataBase.get_text(),            
            DATABASE_USER:self.entUser.get_text(),          
            DATABASE_PASSWORD:self.entPass.get_text(),        
            DATABASE_HOST:self.entHost.get_text(),            
            DATABASE_PORT:self.entPort.get_text(),
            TIME_ZONE:self.cboZonaHoraria.get_active_text(),
            LANGUAGE_CODE:LANGUAGES[self.cboIdioma.get_active_text()],
            MEDIA_ROOT:self.entMedia.get_text()
        }
        
        lib.comandos.crear_proyecto(self.path, 
                                self.entNombre.get_text())
                                
        escribe(self.path, self.dic)
        
        self.on_dlgProyecto_destroy()
        
    def on_btnProbarCnx_clicked(self, *args):
        
        import lib.prueba_conexion
        reload(lib.prueba_conexion)
        
        engine = self.cboEngine.get_active_text()
        
        if engine == "mysql":
            engine = "MySQLdb"
        elif engine == "postgresql":
            engine = "psycopg"
        elif engine == "postgresql_psycopg2":
            engine = "psycopg2"
        else:
            msg = "No se encuentra soportado para prueba de coneccion..."
            dlgAviso(self.dlgProyecto, "%s\n%s" % (engine , msg))
            return
        
        
        dbname = self.entDataBase.get_text()
        host = self.entHost.get_text()
        port = self.entPort.get_text()
        user = self.entUser.get_text()
        passwd = self.entPass.get_text()
        
        prueba = lib.prueba_conexion.PruebaConexion(engine, dbname, 
                                                    host, port, user, passwd) 
        
        respuesta = prueba.prueba() 
        
        if respuesta[0]:
            dlgAviso(self.dlgProyecto, respuesta[1])
        else:
            dlgError(self.dlgProyecto, respuesta[1], trace=False)
              
        
    def on_dlgProyecto_destroy(self, *args):
        self.salir()
        
    def salir(self):
        if __name__ == '__main__':
            gtk.main_quit()
        else:
            self.dlgProyecto.hide()
            
class fcdDirectorio(GladeConnect):
    def __init__ (self, padre = None):
        GladeConnect.__init__(self, 'glade/principal.glade','fcdDirectorio')
        self.fcdDirectorio.set_transient_for(padre)

    def on_btn_clicked(self, btn=None):
        self.fcdDirectorio.hide()
         
if __name__ == '__main__':
    app = dlgProyecto("prueba","/home/juacarra/Escritorio/Pruebas/hola", None)
    gtk.main()
