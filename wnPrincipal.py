#!/usr/bin/env python
# -*- coding: utf-8 -*-

# wnPrincipal.py -- Permite manipular un proyecto de Django.
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
import lib.SimpleTree

from lib.dialogos import dlgAviso, dlgError, dlgAbrirArchivo
from lib import DjangoGui
from dlgProyecto import dlgProyecto
from dlgAplicacion import dlgAplicacion
from dlgCampo import dlgCampo
from lib.comandos import crear_aplicacion, ejecuta
from lib import escribe_urls
from lib.parser_modelos import Modelos
from lib.registra_modelos import escribe_admin
import lib.escribe_settings  

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

class wnPrincipal(GladeConnect):
    def __init__(self, nombre=None, path=None):
        GladeConnect.__init__(self, 'glade/principal.glade','wnPrincipal')
        self.wnPrincipal.set_size_request(800,600)
        self.padre = self.wnPrincipal
        self.path = path
        self.crea_columna_clase()
        self.crea_columna_campo()
        self.apps = []
        self.temp_modelos = []
        self.tablas = []
    
    def crea_columna_clase(self):
        col = gtk.TreeViewColumn('Proyecto', gtk.CellRendererText(), text=0)
        self.lvwClase.append_column(col)
        self.lvwClase.set_model(gtk.TreeStore(*(2*[str])))
        
    def crea_columna_campo(self):      
        self.lvwCampo.set_rules_hint(True)
        columnas = []
        columnas.append([0 ,'Campo','str'])
        columnas.append([1 ,'Tipo','str'])
        modelo = gtk.ListStore(*((3)*[str]))
        lib.SimpleTree.GenColsByModel(modelo, columnas, self.lvwCampo)
        
    
    def escribe_apps(self):
        sys.path.append(self.path )
        
        import settings
        reload(settings)       
              
        dic = {
            NAME:self.nombre,
            DEBUG:settings.DEBUG,
            ADMINS:settings.ADMINS,
            DATABASE_ENGINE:settings.DATABASE_ENGINE,           
            DATABASE_NAME:settings.DATABASE_NAME,            
            DATABASE_USER:settings.DATABASE_USER,          
            DATABASE_PASSWORD:settings.DATABASE_PASSWORD,        
            DATABASE_HOST:settings.DATABASE_HOST,            
            DATABASE_PORT:settings.DATABASE_PORT,
            TIME_ZONE:settings.TIME_ZONE,
            LANGUAGE_CODE:settings.LANGUAGE_CODE,
            MEDIA_ROOT:settings.MEDIA_ROOT
        }
        
        lib.escribe_settings.escribe(self.path, dic, self.apps)
        
        sys.path.remove(self.path)
        del(settings)
        
    def get_tablas(self, app=None):
        tablas = []
        modelo, puntero = self.lvwClase.get_selection().get_selected()
        
        if app <> None:
            aplicacion = app
        else: 
            if modelo[puntero][1] == "aplicacion":
                aplicacion = modelo[puntero][0]
            
            elif modelo[puntero][1] == "modelo":
                aplicacion = modelo[modelo.iter_parent(puntero)][0]
                
        for tabla in self.tablas:
            if tabla[1] == aplicacion:
                tablas.append(tabla[0])
           
        return tablas 
    
    def on_tbtnNuevoProyecto_clicked(self, *args):
        modelo = self.lvwClase.get_model()   
        dlg = dlgProyecto(padre=self.wnPrincipal)
        response = dlg.dlgProyecto.run()
        if response == gtk.RESPONSE_OK:
            path = dlg.entRuta.get_text() + "/" + dlg.entNombre.get_text()
            treeIter = modelo.append(None, [dlg.entNombre.get_text(), path])
            self.nombre = dlg.entNombre.get_text()
            self.path = path
        
        DjangoGui.escribe(self.lvwClase.get_model())
        escribe_urls.escribe(path)
        
    def on_lvwClase_cursor_changed(self,*args):
        modelo, puntero = self.lvwClase.get_selection().get_selected()
        if modelo is None:
            return
        
        modelo_lvwCampo = gtk.ListStore(*((3)*[str]))
        self.entNombre.set_text("")
            
        if modelo[puntero][1] == "aplicacion":
            aplicacion = modelo[puntero][0]
            puntero = modelo.get_iter_first()
            self.nombre = modelo[puntero][0]
            self.path = modelo[puntero][1]       
        
        elif modelo[puntero][1] == "modelo":
            clase = modelo[puntero][0]
            aplicacion = modelo[modelo.iter_parent(puntero)][0]   
            for app in self.temp_modelos:
                if app[0] == aplicacion:
                    if app[1] <> []:
                        for datos in app[1]:  
                            if datos[0] == clase:
                                self.entNombre.set_text(datos[0]) 
                                for campo in datos[1]:
                                    modelo_lvwCampo.append([campo[0],
                                            campo[1].split('(')[0],
                                            campo[1].split('(')[1][0:-1]])
            
            
        else:
            self.nombre = modelo[puntero][0]
            self.path = modelo[puntero][1]
        
        self.lvwCampo.set_model(modelo_lvwCampo)
             
       
    def on_lvwClase_row_activated(self, *args):
        modelo, puntero = self.lvwClase.get_selection().get_selected()
        if modelo is None or modelo.iter_parent(puntero) is not None:
            return
        
        proyecto = dlgProyecto(self.nombre, self.path, self.wnPrincipal)
        response = proyecto.dlgProyecto.run()
       
    def on_tbtnAgregarAplicacion_clicked(self, *args):
        modelo, puntero = self.lvwClase.get_selection().get_selected()
        if modelo is None or puntero is None:
            return
    
        dlg = dlgAplicacion(padre=self.wnPrincipal)
        response = dlg.dlgAplicacion.run()
        puntero = modelo.get_iter_first() 
            
        if response == gtk.RESPONSE_OK:
            modelo.append(puntero, [dlg.entAplicacion.get_text(), "aplicacion"])
       
            crear_aplicacion(modelo.get_value(puntero, 1),
                              dlg.entAplicacion.get_text())
            DjangoGui.escribe(self.lvwClase.get_model())
            self.apps.append("%s.%s" %(self.nombre, dlg.entAplicacion.get_text()))
            self.escribe_apps()
            
        self.lvwClase.expand_all()
            
    def on_tbtnAbrirProyecto_clicked(self, *args):
        path = dlgAbrirArchivo("DjangoGUI", self.padre , ["*.DjangoGui"])
        
        if path is not None:
            modelo = self.lvwClase.get_model()
            datos = DjangoGui.lee(path) 
            padre = modelo.append(None,[datos[0],datos[1]])
            self.path = datos[1]
            self.nombre = datos[0]
            
            for aplicacion in datos[2]:
                ruta = "%s%s/models.py" % (datos[1], aplicacion)
                app = modelo.append(padre, [aplicacion, "aplicacion"])
                modelos = Modelos(ruta)
                
                if modelos.get_modelos() <> []:    
                    self.temp_modelos.append([aplicacion, modelos.get_modelos()])
                
                for clase in modelos.get_modelos():
                    self.tablas.append([clase[0],aplicacion])
                    modelo.append(app, [clase[0], "modelo"])
                    
        self.lvwClase.expand_all()
                  
    
    def on_tbtnQuitarAplicacion_clicked(self, *args):
        pass
        
    def on_tbtnGuardarClase_clicked(self, *args):       
        modelo= self.lvwClase.get_model()
        if modelo is None:
            return
             
        for datos in self.temp_modelos:
            ruta = self.path   
            if ruta[-1] == "/":
                ruta = ruta[0:-1]
                
            ruta_models = "%s/%s/models.py" % (ruta, datos[0])
            ruta_admin = "%s/%s/admin.py" % (ruta, datos[0])
            
            p_modelo = Modelos(ruta_models)
            p_modelo.set_modelos(datos[1])
                 
            escribe_admin(ruta_admin, self.nombre, 
                          datos[0], self.get_tablas(datos[0]))
            

    def on_tbtnAnadirClase_clicked(self, *args):
        modelo, puntero = self.lvwClase.get_selection().get_selected()
        if modelo is None or puntero is None:
            return     
            
        if modelo[puntero][1] == "aplicacion" or modelo[puntero][1] == "modelo":
            try:
                self.tablas.index([self.entNombre.get_text(), modelo[puntero][0]])
                nuevo = False
            except:
                nuevo = True
                           
            if nuevo:
                aplicacion = modelo[puntero][0]
                modelo.append(puntero, [self.entNombre.get_text(), "modelo"])
                self.tablas.append([self.entNombre.get_text(),modelo[puntero][0]])

            else:
                for p_modelo in self.temp_modelos:
                    cont = 0
                    for dato in p_modelo[1]:
                        if dato[0] == modelo[puntero][0]:
                            p_modelo[1].pop(cont)
                
                modelo.set(puntero, 0, self.entNombre.get_text())
                modelo.set(puntero, 1, "modelo")
                aplicacion = modelo[modelo.iter_parent(puntero)][0]
                
                indice = self.tablas.index([self.entNombre.get_text(), 
                                            aplicacion])
                self.tablas[indice] = [self.entNombre.get_text(), aplicacion]
                
            
            
            
            self.nombre = modelo[modelo.get_iter_first()][0]
            self.path = modelo[modelo.get_iter_first()][1]
        
            campos = []
            for campo in self.lvwCampo.get_model():
                campos.append([campo[0],"%s(%s)" % (campo[1], campo[2])])
            
                         
            datos = []
            for p_modelo in self.temp_modelos:
                if p_modelo[0] == aplicacion:
                    for dato in p_modelo[1]:
                        datos.append(dato)
            
            datos.append([self.entNombre.get_text(),
                                        campos, campos[0][0]])
            
            if self.temp_modelos == []:
                self.temp_modelos.append([aplicacion, datos])
            else:    
                for p_modelo in self.temp_modelos:
                
                    if p_modelo[0] == aplicacion:
                        p_modelo[1] = datos
                    
            self.lvwClase.expand_all()
        
        
    def on_tbtnAnadir_clicked(self, *args):
        modelo = self.lvwCampo.get_model()
        dialogo = dlgCampo(self.get_tablas(), padre=self.wnPrincipal)
        response = dialogo.dlgCampo.run()
        if response == gtk.RESPONSE_OK:
            modelo.append([dialogo.nombre, dialogo.tipo, dialogo.opcion])
    
    def on_tbtnPropiedades_clicked(self, btn=None):
        modelo, puntero = self.lvwCampo.get_selection().get_selected()
        if modelo is None:
            return
        datos = [modelo[puntero][0], modelo[puntero][1], modelo[puntero][2]]
        
             
        
        dialogo = dlgCampo(self.get_tablas(), datos, self.padre)
        response = dialogo.dlgCampo.run()
        if response == gtk.RESPONSE_OK:
            modelo.set(puntero, 0, dialogo.nombre)
            modelo.set(puntero, 1, dialogo.tipo)
            modelo.set(puntero, 2, dialogo.opcion)
            
    def on_lvwCampo_row_activated(self, *args):
        self.on_tbtnPropiedades_clicked()
          
    def on_tbtnBorrar_clicked(self, *args):
        pass
    
    def on_tbtnEjecuta_clicked(self, *args):
        ejecuta(self.path)
    
    def on_wnPrincipal_destroy(self, *args):
        gtk.main_quit()
        
        
if __name__ == '__main__':
    app = wnPrincipal()
    gtk.main()
        
