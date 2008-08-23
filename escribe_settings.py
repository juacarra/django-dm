#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

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


def escribe(path, diccionario):
    archivo = open(path + "/settings.py", 'w')
    
    archivo.write("# Django settings for %s project.\n\n" % diccionario[NAME])
    
    archivo.write("DEBUG = True\n\n")
    
    archivo.write("TEMPLATE_DEBUG = DEBUG\n\n")
    
    archivo.write("ADMINS = (\n")
    for admin in diccionario[ADMINS]:
        print admin
        archivo.write("('%s', '%s'),\n" % (admin[0], admin[1]))
    archivo.write(")\n\n")

    archivo.write("MANAGERS = ADMINS\n\n")
    
    archivo.write("DATABASE_ENGINE = '%s'\n" % diccionario[DATABASE_ENGINE])
    archivo.write("DATABASE_NAME = '%s'\n" % diccionario[DATABASE_NAME])
    archivo.write("DATABASE_USER = '%s'\n" % diccionario[DATABASE_USER])
    archivo.write("DATABASE_PASSWORD = '%s'\n" % diccionario[DATABASE_PASSWORD])
    archivo.write("DATABASE_HOST = '%s'\n" % diccionario[DATABASE_HOST])
    archivo.write("DATABASE_PORT = '%s'\n\n" % diccionario[DATABASE_PORT])
    
    archivo.write("TIME_ZONE = '%s'\n\n" % diccionario[TIME_ZONE])
    
    archivo.write("LANGUAGE_CODE = '%s'\n\n" % diccionario[LANGUAGE_CODE])
    
    archivo.write("SITE_ID = 1\n\n")
    
    archivo.write("USE_I18N = True\n\n") 
    
    archivo.write("MEDIA_ROOT = '%s'\n\n" % diccionario[MEDIA_ROOT])
    
    archivo.write("MEDIA_URL = ''\n\n")
    
    archivo.write("ADMIN_MEDIA_PREFIX = '/media/'\n\n")
    
    archivo.write("SECRET_KEY = 'm9bs1%$43md25*p7x*y$^cw)&pks06()=gv2x=daqn6xyd0)*h'\n\n")
    
    archivo.write("TEMPLATE_LOADERS = (\n")
    archivo.write("    'django.template.loaders.filesystem.load_template_source',\n")
    archivo.write("    'django.template.loaders.app_directories.load_template_source',\n")
    archivo.write(")\n\n")
    
    archivo.write("MIDDLEWARE_CLASSES = (\n")
    archivo.write("    'django.middleware.common.CommonMiddleware',\n")
    archivo.write("    'django.contrib.sessions.middleware.SessionMiddleware',\n")
    archivo.write("    'django.contrib.auth.middleware.AuthenticationMiddleware',\n")
    archivo.write("    'django.middleware.doc.XViewMiddleware',\n")
    archivo.write(")\n\n")
    
    
    archivo.write("ROOT_URLCONF = '%s.urls'\n\n" % diccionario[NAME])
    
    archivo.write("TEMPLATE_DIRS = (\n")
    archivo.write(")\n\n")

    archivo.write("INSTALLED_APPS = (\n")
    archivo.write(    "'django.contrib.auth',\n")
    archivo.write(    "'django.contrib.contenttypes',\n")
    archivo.write(    "'django.contrib.sessions',\n")
    archivo.write(    "'django.contrib.sites',\n")
    archivo.write(    "'django.contrib.admin',\n")
    archivo.write(")\n\n")
    
if __name__ == "__main__":
    
    dic = {
            NAME:'nombre',
            DEBUG:'debug',
            ADMINS:(('juan carrasco','juacarrag@gmail.com'),('dos','dos@dos.dos')),
            DATABASE_ENGINE:'motor' ,           
            DATABASE_NAME:'db name',            
            DATABASE_USER:'usuadio',          
            DATABASE_PASSWORD:'pass',        
            DATABASE_HOST:'servidor',            
            DATABASE_PORT:'puerto',
            TIME_ZONE:'zona horaria',
            LANGUAGE_CODE:'idioma',
            MEDIA_ROOT:'media root'
         }
    #print dic
    
    #escribe('prueba_de_escritura_settings', dic)
