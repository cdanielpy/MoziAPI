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


    def __init__(self, cAlias, clsClaseOtd, cTipo):
        '''
        Inicializador de la clase
        
        cAlias      = alias para la tabla en la relacion
        clsClaseOtd = clase derivada de OTDBase
        cTipo       = [NORMAL | IZQUIERDA | DERECHA]
        
        '''

        super(Union, self).__init__()

        # si se paso los parametros como corresponden
        if type(clsClaseOtd) is type and type(cAlias) is str and type(cTipo) is str:
            self._oTabla = clsClaseOtd()
            self._cAlias = cAlias
            self._oTabla.alias = cAlias

            self.__cCondicionSQL = '%s %s AS %s' % (cTipo
                                                    , self._oTabla.cNombreTabla
                                                    , self._cAlias
                                                    )

        else:
            # sino, excepcion
            raise Exception(Union.NOMBRE_CLASE
                            + ': El parametro debe ser una clase hija de '
                            + 'OTDBase y un alias para el mismo!'
                            )


    def __str__(self): return self.__cCondicionSQL

    def __getUnion(self): return self.__cCondicionSQL


    def setUniones(self, oClaseOTD):
        '''
        Configura la sentencia resultante de la union de tablas
        '''

        oClaseOTD._cListaCampos = oClaseOTD.listaCampos + ', '
        oClaseOTD._cListaCampos+= self._oTabla.listaCampos
        oClaseOTD._cSelect = None
        return self.__cCondicionSQL


    @staticmethod
    def Normal(**parametros):
        '''
        Devuelve la instancia de Union de tipo JOIN
        
        parametros => diccionario de tipo {'alias':ClaseOTD}
        
        '''


        # si el parametro NO es un diccionario
        if type(parametros) is not dict:
            raise Exception(Union.NOMBRE_CLASE
                            + ".Normal: El parametro se debe pasar "
                            + "{'alias':ClaseOTD}!"
                            )

        return Union(parametros.keys().pop()
                     , parametros.values().pop()
                     , Union.NORMAL
                     )


    union = property(fget=__getUnion, doc='Devuelve la clausula de union')
