#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 13/04/2014

@author: daniel
@contact: cdaniel.py@gmail.com
@summary: prueba de modulos y clases

    Utilizamos una conexion a una BD mysql/mariadb y la base de datos de ejemplo
    EMPLOYEES, que se puede descargar en el siguiente enlace http://launchpad.net/test-db/

'''
from testing.mysqlutiles import MySqlUtiles
from testing.otds import Employee
from org.moziapi.restricciones import Restriccion



if __name__ == '__main__':
    #iniciamos la conexion a la BD
    oConexion = MySqlUtiles('localhost', '', 'employees', 'root', 'Admin159')
    
    lResultado = oConexion.lConectar()
    
    #si no se conecto
    if lResultado[0] != 1: raise Exception(lResultado[1])
    
    #una consulta basica
    #lResultado = oConexion.lEjecutarConsulta(Employee().filtrar(Restriccion.Ig(_nId = 10008)))
    lResultado = oConexion.lEjecutarConsulta(Employee().filtrar(Restriccion.Entre(_nId = [10008, 10015])))
    
    if lResultado[0] != 1: raise Exception(lResultado[1])
    
    
    n = 0
    f = Employee()._dicCampos.keys()
    for fila in lResultado[1]:
        print fila
        emp = Employee(**dict(zip(f, fila)))
        n+= 1
        print emp
        if n > 10: break
        