#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 13/04/2014

@author: daniel
@contact: cdaniel.py@gmail.com
@summary: Modulo de clases derivadas de OTDBase

'''

#importamos los modulos y clases necesarias
from org.moziapi.bases.otdbase import OTDBase


class Employee(OTDBase):
    '''
    Clase para datos de la tabla [employees]
    '''


    NOMBRE_CLASE = 'Employee'

    #mapeo de nombres de campos de la tabla a atributos de la clase
    _dicCampos = {'emp_no':'_nId'
                   , 'first_name':'_cNombre'
                   , 'last_name':'_cApellido'
                   , 'gender':'_cGenero'
                   , 'hire_date':'_dFechaIngreso'
                   , 'birth_date':'_dCumpleanos'
                }


    def __init__(self, **parametros):
        '''
        Inicializador de la clase
        
        parametros = diccionario con los pares de datos atributo = valor
        
        '''

        #invocamos al inicializador de la clase base
        super(Employee, self).__init__('employees')

        #valores por defecto para atributos
        self._cNombre = ''
        self._cApellido = ''
        self._cGenero = None
        self._dFechaIngreso = None
        self._dCumpleanos = None

        #si se recibio el diccionario de parametros
        if parametros:
            #lo recorremos
            for k in parametros:
                #asignamos los valores a los atributos correspondientes
                self.__setattr__(self._dicCampos[k], parametros[k])

        self._cDescripcion = self._cNombre + ' ' + self._cApellido
