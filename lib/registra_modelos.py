 #!/usr/bin/env python
# -*- coding: utf-8 -*-

# registra_modelos -- Permite registrar modelos de Django en el archivo admin.py.
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
 
def escribe_admin(ruta, proyecto, aplicacion, tablas):

    admin = open(ruta, 'w')
    
    print tablas
    
    t_tablas = ""
    for tabla in tablas:
        if tabla <> "":
            t_tablas += tabla + ", "
    if t_tablas[-2:] == ", ":
        print t_tablas
        t_tablas = t_tablas[0:-2]
        print t_tablas
        
    print proyecto, aplicacion, tablas
         
    admin.write("from %s.%s.models import %s\n" % (proyecto,
                                                             aplicacion,
                                                             t_tablas))
    admin.write("from django.contrib import admin\n")
    admin.write("\n")
    for tabla in tablas:
        admin.write("admin.site.register(%s)\n" % tabla)
    
