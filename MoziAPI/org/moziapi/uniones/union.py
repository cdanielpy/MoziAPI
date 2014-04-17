#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 13/04/2014

@author: daniel
@contact: cdaniel.py@gmail.com
@summary: Clase para generacion de sentencias con interseccion de tablas
'''

class Union(object):
    '''
    Clase para generacion de sentencias con interseccion de tablas
    '''

    NOMBRE_CLASE = 'Union'

    NORMAL = 'JOIN'
    IZQUIERDA = 'LEFT OUTER JOIN'
    DERECHA = ' RIGHT OUTER JOIN'


    def __init__(self, clsClaseOtd, cAlias, cTipo):
        '''
        Inicializador de la clase
        
        clsClaseOtd = clase derivada de OTDBase
        cAlias      = alias para la tabla en la relacion
        cTipo       = [NORMAL | IZQUIERDA | DERECHA]
        
        '''

        super(Union, self).__init__()

        #si se paso los parametros como corresponden
        if type(clsClaseOtd) is type and type(cAlias) is str and type(cTipo) is str:
            self.cTabla = clsClaseOtd().cNombreTabla
            self.cAlias = cAlias

            self.__cCondicionSQL = '%s %s AS %s' % (cTipo, self.cTabla, self.cAlias)

        else:
            #sino, excepcion
            raise Exception(Union.NOMBRE_CLASE
                            + ': El parametro debe ser una clase hija de OTDBase y un alias para el mismo!'
                            )


    def __str__(self): return self.__cCondicionSQL


    @staticmethod
    def Normal(**parametros):
        
        #si el parametro NO es un diccionario
        if type(parametros) is not dict:
            raise Exception(Union.NOMBRE_CLASE + ".Normal: El parametro se debe paras 'alias' = ClaseOTD")

        return Union(parametros.values().pop(), parametros.keys().pop(), Union.NORMAL)
