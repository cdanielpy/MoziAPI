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
from moziapi.decoradores.relaciones import Muchos_a_Uno, Uno_a_Muchos


class Department(OTDBase):
    '''
    Clase para datos de la tabla [departmens]
    
    '''


    NOMBRE_CLASE = 'Department'

    # mapeo de nombres de campos de la tabla a atributos de la clase
    _dicCampos = {'dept_no':'nId'
                   , 'dept_name':'cDescripcion'
                }


    def __init__(self, **parametros):
        '''
        Inicializador de la clase
        
        parametros = diccionario con los pares de datos atributo = valor
        
        '''

        # invocamos al inicializador de la clase base
        super(Department, self).__init__('departments', **parametros)




class DeptEmp(OTDBase):
    '''
    Clase para datos de la tabla [dept_emp]
    
    '''

    NOMBRE_CLASE = 'DeptEmp'

    # mapeo de nombres de campos de la tabla a atributos de la clase
    _dicCampos = {'emp_no':'nEmployeeId'
                   , 'dept_no':'cDepartmentId'
                   , 'from_date': 'dDesde'
                   , 'to_date':'dHasta'
                   }


    def __init__(self, **parametros):
        '''
        Inicializador de la clase
        
        parametros = diccionario con los pares de datos atributo = valor
        
        '''

        # valores por defecto para atributos
        self.nEmployeeId = 0
        self.cDepartmentId = ''
        self.dDesde = None
        self.dHasta = None

        # invocamos al inicializador de la clase base
        super(DeptEmp, self).__init__('dept_emp', **parametros)

        self.cDescripcion = str(self.nEmployeeId) + ' on ' + self.cDepartmentId


    @Muchos_a_Uno(clase=Department, fk='cDepartmentId', atr='oDepartment')
    def __getDepartment(self): return self.oDepartment


    Department = property(fget=__getDepartment,
                          doc='Devuelve la instancia de Department relacionada'
                          )



class Employee(OTDBase):
    '''
    Clase para datos de la tabla [employees]
    
    '''


    NOMBRE_CLASE = 'Employee'

    # mapeo de nombres de campos de la tabla a atributos de la clase
    _dicCampos = {'emp_no':'nId'
                   , 'first_name':'cNombre'
                   , 'last_name':'cApellido'
                   , 'gender':'cGenero'
                   , 'hire_date':'dFechaIngreso'
                   , 'birth_date':'dCumpleanos'
                }


    def __init__(self, **parametros):
        '''
        Inicializador de la clase
        
        parametros = diccionario con los pares de datos atributo = valor
        
        '''

        # valores por defecto para atributos
        self.cNombre = ''
        self.cApellido = ''
        self.cGenero = None
        self.dFechaIngreso = None
        self.dCumpleanos = None

        # invocamos al inicializador de la clase base
        super(Employee, self).__init__('employees', **parametros)

        self.cDescripcion = self.cNombre + ' ' + self.cApellido


    @Uno_a_Muchos(clase=DeptEmp, fk='nEmployeeId', atr='lDeptEmp')
    def __getDeptEmp(self): return self.lDeptEmp


    DeptEmps = property(fget=__getDeptEmp,
                    doc='Devuelve la lista de instancias de DeptEmp asociadas'
                    )