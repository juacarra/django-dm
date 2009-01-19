#!/usr/bin/env python
# -*- coding: utf-8 -*-

# parser_modelos -- Permite leer y escribir modelos de Django.
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


class Modelos:
    __ruta = '' 
    __modelos = [] 
        
    def __init__(self, ruta):
        self.__ruta = ruta
        
    def set_ruta(self, ruta): 
        self.__ruta = ruta
       
    def set_modelos(self, modelos):
        #self.__lee_modelos()
        self.__modelos = modelos
        self.__escribe_modelos()
    
    def get_ruta(self):
        return self.__ruta
        
    def get_modelos(self):
        self.__lee_modelos()
        return self.__modelos
        
    def __lee_modelos(self):
        self.__modelos = []
        campos = []
        clase = ''
        devuelve = ''
        bandera = False
       
        modelos = open(self.__ruta, 'r')
        
        for linea in modelos:
             
            if linea.find('class') is not -1:
                bandera = True
                clase = linea.split('class')[1].split('(')[0].split(' ')[1]
            
            elif bandera:
                if linea.find('=') is not -1:
                    campo = linea.split(' = models.')[0]
                    campo = campo.replace(' ', '').replace('\n', '')
                    tipo = linea.replace('\n', '').split(' = models.')[1]
                    campos.append([campo, tipo])
                    
                else:
                    if linea.find('def __str__(self):') is not -1:
                        pass
                    elif linea.find('return') is not -1:
                        devuelve = linea.split('return')[1].replace('self.', '')
                        devuelve = devuelve.replace(' ', '').replace('\n', '')
                        
                        self.__modelos.append([clase, campos, devuelve])
                        bandera = False
                        campos = []
                    else:
                        self.__modelos.append((clase, campos, devuelve))
                        bandera = False
                        campos = []
    
    def __escribe_modelos(self):
    
        modelos = open(self.__ruta, 'w')
                
    
        modelos.write('from django.db import models\n')
        
        for modelo in self.__modelos:
            modelos.write('\n')
            modelos.write('class %s(models.Model):\n' % modelo[0])
            for campo in modelo[1]:
                modelos.write('    %s = models.%s\n' % (campo [0], campo[1]))
            if modelo [2] <> '':
                modelos.write('    def __str__(self):\n')
                modelos.write('        return self.%s\n' % modelo[2])           
                         
                                        
if __name__ == '__main__':

    ruta = '/home/juacarra/Escritorio/modelos/models.py'
    ruta1 = '/home/juacarra/Escritorio/modelos/models1.py'
    
    modelos= [('Poll', 
                    [('question', 'CharField(max_length=200)'),
                    ('pub_date', "DateTimeField('date published')")], 
                'question'), 
            ('Choice', 
                    [('poll', 'ForeignKey(Poll)'), 
                    ('choice', 'CharField(max_length=200)'), 
                    ('votes', 'IntegerField()')], 
                'choice')]
                 
          
    
    #app = Modelos(ruta1)
    #app.set_modelos(modelos)
   
    app = Modelos(ruta)
    
    print 'modelos en %s' % app.get_ruta() 
    
    for modelo in app.get_modelos():
        print ''
        print 'Clase', modelo[0]
        for campo in modelo[1]:
            print 'campo %s tipo %s' % (campo[0], campo[1])
        print 'Devuelve', modelo[2]
        print ''
    
    print app.get_modelos()
   

        
        
        
        
        
   
