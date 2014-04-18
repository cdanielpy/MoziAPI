#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 13/04/2014

@author: daniel
@contact: cdaniel.py@gmail.com
@summary: Modulo de clases derivadas de OTDBase

'''

# importamos los modulos y clases necesarias
from moziapi.bases import OTDBase


class Employee(OTDBase):
    '''
    Clase para datos de la tabla [employees]
    '''


    NOMBRE_CLASE = 'Employee'

    # mapeo de nombres de campos de la tabla a atributos de la clase
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

        # valores por defecto para atributos
        self._cNombre = ''
        self._cApellido = ''
        self._cGenero = None
        self._dFechaIngreso = None
        self._dCumpleanos = None

        # invocamos al inicializador de la clase base
        super(Employee, self).__init__('employees', **parametros)

        self._cDescripcion = self._cNombre + ' ' + self._cApellido



class Department(OTDBase):
    '''
    Clase para datos de la tabla [departmens]
    '''


    NOMBRE_CLASE = 'Department'

    # mapeo de nombres de campos de la tabla a atributos de la clase
    _dicCampos = {'dept_no':'_nId'
                   , 'dept_name':'_cDescripcion'
                }


    def __init__(self, **parametros):
        '''
        Inicializador de la clase
        
        parametros = diccionario con los pares de datos atributo = valor
        
        '''

        # invocamos al inicializador de la clase base
        super(Department, self).__init__('departments')

        # si se recibio el diccionario de parametros
        if parametros:
            # lo recorremos
            for k in parametros:
                # asignamos los valores a los atributos correspondientes
                self.__setattr__(self._dicCampos[k], parametros[k])



class DepEmp(OTDBase):
    '''
    Clase para datos de la tabla [dept_emp]
    '''


    NOMBRE_CLASE = 'DepEmp'

    # mapeo de nombres de campos de la tabla a atributos de la clase
    _dicCampos = {'emp_no':'_nEmployeeId'
                   , 'dept_no':'_cDepartmentId'
                   , 'from_date': '_dDesde'
                   , 'to_date':'_dHasta'
                }


    def __init__(self, **parametros):
        '''
        Inicializador de la clase
        
        parametros = diccionario con los pares de datos atributo = valor
        
        '''

        # invocamos al inicializador de la clase base
        super(DepEmp, self).__init__('dept_emp')

        # valores por defecto para atributos
        self._nEmployeeId = 0
        self._cDepartmentId = ''
        self._dDesde = None
        self._dHasta = None

        # si se recibio el diccionario de parametros
        if parametros:
            # lo recorremos
            for k in parametros:
                # asignamos los valores a los atributos correspondientes
                self.__setattr__(self._dicCampos[k], parametros[k])
