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


class dlgCampo(GladeConnect):
    nombre = ""
    tipo = ""
    opcion = ""
    
    def __init__(self, tablas, datos=None, padre=None):
        GladeConnect.__init__(self, 'glade/principal.glade','dlgCampo')
        
        if padre is None:
            self.padre = self.dlgCampo
        else:
            self.padre = padre
        self.dlgCampo.set_transient_for(padre)
        
        self.ntbTipo.set_show_tabs(False)
        self.ntbTipo.set_current_page(0)
        self.__carga_cboRelTabla(tablas)
        self.__carga_cboTipo()
        if datos is not None:
            self.__carga_datos(datos, tablas)
        
    def __carga_cboTipo(self):
        self.cboTipo.set_model(gtk.ListStore(*(3*[str])))
        modelo = self.cboTipo.get_model()
        modelo.append(["IntegerField", 0, "IntegerField"])
        modelo.append(["CharField", 1, "CharField"])
        modelo.append(["FloatField", 5, "FloatField"])
        modelo.append(["DateField", 0, "DateField"])
        modelo.append(["TimeField", 0, "TimeField"])
        modelo.append(["FileField", 3, "FileField"])
        modelo.append(["ImageField", 3, "ImageField"])
        modelo.append(["URLField", 6, "URLField"])
        modelo.append(["Relacion", 8, "relacion"])
        
    def __carga_cboRelTabla(self, tablas):
        self.cboRelTabla.set_model(gtk.ListStore(*(1*[str])))
        modelo = self.cboRelTabla.get_model()
        
        for tabla in tablas:
            modelo.append([tabla])
            
    def __carga_datos(self, datos, tablas):
        self.entNombre.set_text(datos[0])
        
        if datos[1] == "IntegerField":
            indice = 0
        elif datos[1] == "CharField":
            indice = 1
        elif datos[1] == "FloatField":
            indice = 2
        elif datos[1] == "DateField":
            indice = 3
        elif datos[1] == "TimeField":
            indice = 4
        elif datos[1] == "FileField":
            indice = 5
        elif datos[1] == "ImageField":
            indice = 6
        elif datos[1] == "URLField":
            indice = 7
        elif datos[1] == "ForeignKey":
            indice = 8
            self.rbtnRelUnoMuchos.set_active(True)            
            self.cboRelTabla.set_active(tablas.index(datos[2]))
        elif datos[1] == "ManyToManyField":    
            indice = 8
            self.rbtnRelMuchosMuchos.set_active(True)
            self.cboRelTabla.set_active(tablas.index(datos[2]))
            
        self.cboTipo.set_active(indice)
        
        opciones = datos[2].split(",")
        for opcion in opciones:
            opcion.split("=")
            if opcion.split("=")[0] == "max_length":
                self.entTextoLargo.set_text(opcion.split("=")[1])
            elif opcion.split("=")[0] == "max_digits":
                self.spnRealDigitos.set_text(opcion.split("=")[1])
            elif opcion.split("=")[0] == "decimal_places":
                self.spnRealDecimales.set_text(opcion.split("=")[1])
            elif opcion.split("=")[0] == "upload_to":
                self.entRuta.set_text(opcion.split("=")[1])    
            elif opcion.split("=")[0] == "verify_exist":
                if opcion.split("=")[1] == "True":
                    self.chkURLVerificar.Set_active(True)
                else:
                    self.chkURLVerificar.Set_active(False)
            elif opcion.split("=")[0] == "help_text":
                self.entAyuda.set_text(opcion.split("=")[1])
            elif opcion.split("=")[0] == "default":
                self.entDefecto.set_text(opcion.split("=")[1])
            
                
    def on_cboTipo_changed(self, *args):
        modelo = self.cboTipo.get_model()
        puntero = self.cboTipo.get_active_iter()
        self.ntbTipo.set_current_page(int(modelo[puntero][1]))
        
    def on_cboArchivoCargar_clicked(self, *args):
        dlg = fcdDirectorio(self.dlgCampo)
        response = dlg.fcdDirectorio.run()
        if response == gtk.RESPONSE_OK:
            self.entRuta.set_text(dlg.fcdDirectorio.get_filename())
        
    def on_btnCancelar_clicked(self, *args):
        self.salir()
        
    def on_btnAceptar_clicked(self, *args):
        modelo = self.cboTipo.get_model()
        puntero = self.cboTipo.get_active_iter()
        
        self.tipo = modelo[puntero][2]
        self.nombre = self.entNombre.get_text()
        self.opcion = ""
        
        opciones = []
        
        if self.tipo == "CharField":
            opciones.append("max_length=%s" % self.entTextoLargo.get_text())
            
        elif self.tipo == "FloatField":
            digitos = self.spnRealDigitos.get_text()
            decimales = self.spnRealDecimales.get_text()
            opciones.append("max_digits=%s, decimal_places=%s" % (digitos,
                                                                  decimales))
        elif self.tipo == "FileField" or self.tipo == "ImageField":
            opciones.append("upload_to='%s'" % self.entRuta.get_text())
        
        elif self.tipo == "URLField":
            if self.chkURLVerificar.get_active():
                valor = "True"
            else:
                valor = "False"
            opciones.append("verify_exist=%s" % valor)
                
        if self.entAyuda.get_text() <> "":
            opciones.append("help_text='%s'" % self.entAyuda.get_text())
        if self.entDefecto.get_text() <> "":
            opciones.append("default='%s'" % self.entDefecto.get_text())
        
        for dato in opciones:
            self.opcion += "%s," % dato
            
        self.opcion = self.opcion[0:-1]
        
        if self.tipo == "relacion":
            if self.rbtnRelUnoMuchos.get_active():
                self.tipo = "ForeignKey"
            else:
                self.tipo = "ManyToManyField"
            
            self.opcion = self.cboRelTabla.get_active_text()
          
        print 'campo: %s = models.%s(%s)' % (self.nombre, self.tipo, self.opcion) 
        self.salir()
        
    def on_dlgCampo_destroy(self, *args):
        self.salir()
        
    def salir(self):
        if __name__ == '__main__':
            gtk.main_quit()
        else:
            self.dlgCampo.hide()
        
class fcdDirectorio(GladeConnect):
    def __init__ (self, padre = None):
        GladeConnect.__init__(self, 'glade/principal.glade','fcdDirectorio')
        self.fcdDirectorio.set_transient_for(padre)

    def on_btn_clicked(self, btn=None):
        self.fcdDirectorio.hide()
        
if __name__ == '__main__':
    tablas = ["tabla1", "tabla2", "tabla3"]
    
    datos = ["dato_texto", "CharField",
            "max_length=10,help_text='bbbbbb',default='aaaaaa'"]
            
    datos1 = ["nombre_relacion", "ManyToManyField" ,"tabla3"]
    
    datos2 = ["dato_entero", "IntegerField", ""]
    
    datos3 = ["dato_float", "FloatField" ,"max_digits=10, decimal_places=2"]
    
    app = dlgCampo(tablas)
    gtk.main()


