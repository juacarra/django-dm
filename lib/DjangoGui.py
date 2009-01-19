#!/usr/bin/env python
# -*- coding: utf-8 -*-

# DjangoGui.py -- Permite leer y escribir la configuracion de un archivo
#                 *.DjangoGui 
                 
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

def lee(path):
    archivo = open(path,"r")
    nombre = ""
    aplicaciones = []
    for linea in archivo:
        if linea.split("=")[0] == "NOMBRE":
            nombre = linea.split("=")[1].replace("\n","")
        if linea.split("=")[0] == "APLICACION":
            aplicaciones = linea.split("=")[1].replace("\n","")
            aplicaciones = aplicaciones.split(";")[0:-1]
    return nombre, path.replace(nombre + ".DjangoGui" , ""), aplicaciones
    
def escribe(modelo):
    padre = modelo.get_iter_first()        
    while padre <> None:
        nombre = modelo.get_value(padre,0)
        path = modelo.get_value(padre,1)
        archivo = open("%s/%s%s" % (path, nombre, ".DjangoGui") ,'w')
        archivo.write("NOMBRE=%s\n" % nombre)
    
        puntero = modelo.iter_children(padre)
        padre = modelo.iter_next(padre)
        app = ""
        while puntero<> None:
            app += modelo.get_value(puntero,0) + ";"
            puntero = modelo.iter_next(puntero)
        
        archivo.write("APLICACION=%s\n" % app)
        archivo.close()
    
        
if __name__ == '__main__':
    print lee("/home/juacarra/Escritorio/Pruebas/hola/hola.DjangoGui")


        
