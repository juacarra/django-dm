#!/usr/bin/env python
# -*- coding: utf-8 -*-

# comandos.py -- Permite crear y ejecutar un proyecto de Django.
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


import os
import sys

DJANGO_ADMIN = 'django-admin.py'
MANAGE = 'manage.py'
STARTAPP = 'startapp'

#sys.platform devuelve el os    os.name


def crear_proyecto(path, nombre_proyecto):
    comando = "cd %s;%s %s %s" % (os.path.dirname(path), 
                                  DJANGO_ADMIN,
                                  'startproject', 
                                  nombre_proyecto)    
    os.system(comando)
    
def crear_aplicacion(path, nombre):
    comando = "cd %s;%s %s %s %s" % (path, "python", MANAGE, STARTAPP, nombre)
    os.system(comando)
    
def ejecuta(path):
    comando = "cd %s;python %s %s" % (os.path.dirname(path), 
                                  MANAGE,
                                  'syncdb')   
    os.system(comando)
        
    comando = "cd %s;python %s %s" % (os.path.dirname(path), 
                                  MANAGE,
                                  'runserver')
    
    os.system(comando)
    
if __name__ == '__main__':
    
    #crear_proyecto('/home/juacarra/Escritorio/Pruebas/asdf','asdf')
    crear_aplicacion("/home/juacarra/Escritorio/Pruebas/hola","app1")
    
    
