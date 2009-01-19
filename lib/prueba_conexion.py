#!/usr/bin/env python
# -*- coding: utf-8 -*-

# prueba_conexion -- Permite realizar una prueba de conexion a alguna
#                    base de datos.

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


import sys

FALTA = []

try:
    import MySQLdb 
except:
    FALTA.append("MySQLdb")

try:
    import psycopg 
except:
    FALTA.append("psycopg")

try:
    import psycopg2 
except:
    FALTA.append("psycopg2")
    
try:
    from sqlite3 import dbapi2 as sqlite
except ImportError:
    from pysqlite2 import dbapi2 as sqlite


class PruebaConexion:
    """devuelve tupla 
        False o True: dependiendo del exito de la prueba de conexion
        mensaje: de error o prueba exitosa"""
        
    def __init__(self, engine, dbname, host=None, 
                 port=None, user=None, passwd=None):
                 
        self.engine = engine
        self.dbname = dbname
        self.host = host
        self.port = port
        self. user = user
        self.passwd = passwd
        
    def prueba_conexion(self):
        if self.engine == "sqlite3":
            kwargs = {
                'database': self.dbname,
                'detect_types': sqlite.PARSE_DECLTYPES | sqlite.PARSE_COLNAMES,
            }
            
            try:
                sqlite.connect(**kwargs)
            except Exception, details:
                return False, "Error"               
            
        if self.engine == "MySQLdb":
            kwargs = {}
            if self.user:
                kwargs['user'] = self.user
            if self.dbname:
                kwargs['db'] = self.dbname
            if self.passwd:
                kwargs['passwd'] = self.passwd
            if self.host.startswith('/'):
                kwargs['unix_socket'] = self.host
            elif self.host:
                kwargs['host'] = self.host
            if self.port:
                kwargs['port'] = int(self.port)
            
            try:        
                MySQLdb.connect(**kwargs)    
            except Exception, details:
                return False, "Error de conexion con MySQL.\n" \
                     "Revise los parametros de conexion..."
                
        if self.engine == "psycopg" or self.engine == "psycopg2":
            conn_string = ""
            if self.dbname:     
                conn_string = "dbname=%s" % self.dbname
            if self.user:
                conn_string += " user=%s" % self.user
            if self.passwd:
                conn_string += " password='%s'" % self.passwd
            if self.host:
                conn_string += " host=%s" % self.host
            if self.port:
                conn_string += " port=%s" % self.port
            if self.engine == "psycopg":     
                try:
                    psycopg.connect(conn_string)
                except Exception, details:
                    return False, "Error de conexion con Postgres.\n" \
                         "Revise los parametros de conexion..."
            else:
                try:
                    psycopg.connect(conn_string)
                except Exception, details:
                    return False, "Error de conexion con Postgres.\n" \
                         "Revise los parametros de conexion..."
            
        return True, "La prueba se realizo con exito..."
            
              
    def prueba(self):
        
        for i in xrange(len(FALTA)):
            
            if self.engine == FALTA[i]:
            
                return False, "No se encuentra el modulo %s.\n" \
                    "Solicite a su administrador de sistema que instale \n" \
                    "el paquete de %s para python" % (self.engine, self.engine)        
            
            return self.prueba_conexion()
        
        
if __name__ == "__main__":
  
    engine = "psycopg"
    dbname = "demo"
    #dbname = "/home/juacarra/Escritorio/asdfghjh"
    host = "192.168.1.2"
    port = "5432"
    user = "juacarra"
    passwd = "juacarra"
        
    app = PruebaConexion(engine, dbname, host, port, user, passwd)
    print app.prueba()
    
    
    
