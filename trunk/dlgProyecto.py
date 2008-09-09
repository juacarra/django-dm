#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk

from lib.GladeConnect import *
import lib.SimpleTree

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
    def __init__(self, nombre=None, path=None):
        GladeConnect.__init__(self, 'glade/principal.glade','dlgProyecto')
        self.path = path
        
        self.crea_columna_clase()
        
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
        if  self.cboEngine.get_active_text() == 'mysql':
            self.entPort.set_text('3306')
        elif self.cboEngine.get_active_text() == 'postgresql':
            self.entPort.set_text('5432')
        elif self.cboEngine.get_active_text() == 'postgresql_psycopg2':
            self.entPort.set_text('5432')
        elif self.cboEngine.get_active_text() == 'ado_mssql':
            self.entPort.set_text('0')
            
        if self.cboEngine.get_active_text() == 'sqlite3':
            self.entUser.set_sensitive(False)
            self.entPass.set_sensitive(False)
            self.entHost.set_sensitive(False)
            self.entPort.set_sensitive(False)
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
        
        #escribe(self.path, dic)************************************************************************
        self.path = self.entRuta.get_text()
        self.on_dlgProyecto_destroy()
        
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
    app = dlgProyecto()
    gtk.main()
