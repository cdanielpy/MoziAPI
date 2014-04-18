#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 13/04/2014

@author: daniel
@contact: cdaniel.py@gmail.com
@summary: Clase para generacion de sentencias con interseccion de tablas
'''

#importamos los modulos y clases necesarias



class Union(object):
    '''
    Clase para generacion de sentencias con interseccion de tablas
    '''

    NOMBRE_CLASE = 'Union'

    NORMAL = 'JOIN'
    IZQUIERDA = 'LEFT OUTER JOIN'
    DERECHA = ' RIGHT OUTER JOIN'


    __CLAUSULA = '%s %s AS %s ON %s'



    def __init__(self, **kwargs):
        '''
        Inicializador de la clase
        
        cTipo        = [NORMAL | IZQUIERDA | DERECHA]
        oRestriccion = instacia de Restriccion donde se indican
                        la relacion entre campos de las tablas
        parametros   => cAlias = ClaseOTD
        
        '''

        super(Union, self).__init__()

        # si se paso los parametros como corresponden
        if kwargs and len(kwargs) is 3:

            #extraemos el tipo de union
            cTipo = kwargs.pop('cTipo')
            
            #extraemos la restriccion
            oRestriccion = kwargs.pop('oRestriccion')

            #tomamos el alias, que llega como clave
            self._cAlias = kwargs.keys().pop()

            #la clase hija de OTDbase, que llega como valor
            self._oTabla = kwargs.values().pop()

            if type(self._oTabla) is type \
                and type(self._cAlias) is str:

                #creamos la instancia de la clase
                self._oTabla = self._oTabla(cAlias = self._cAlias)

                #combinamos todo
                self.__cCondicionSQL = Union.__CLAUSULA % (cTipo
                                                        , self._oTabla.cNombreTabla
                                                        , self._cAlias
                                                        , oRestriccion.getCondiciones(self._oTabla)
                                                        )

        else:
            # sino, excepcion
            raise Exception(Union.NOMBRE_CLASE
                            + ': El parametro debe ser una clase hija de '
                            + 'OTDBase y un alias para la misma!'
                            )


    def __str__(self): return self.__cCondicionSQL

    def __getUnion(self): return self.__cCondicionSQL


    def setUniones(self, oClaseOTD):
        '''
        Genera las clausulas resultante de la union de tablas
        
        '''

        #combinamos la lista de campos de las tablas involucradas
        oClaseOTD._cListaCampos = oClaseOTD.listaCampos + ', '
        oClaseOTD._cListaCampos+= self._oTabla.listaCampos
        oClaseOTD._cSelect = None

        #devolvemos la clausula de interseccion de tablas
        return self.__cCondicionSQL


    @staticmethod
    def Normal(**kwargs):
        '''
        Devuelve la instancia de Union de tipo JOIN
        
        parametros => diccionario de tipo {'alias':ClaseOTD}
        
        '''

        import warnings

        #advertencia de componente deprecado
        warnings.showwarning('Union.Normal(): deprecado, recurrir directamente al constructor de la clase!'
                             , DeprecationWarning
                             , __file__
                             , 0
                             )

        # si el parametro NO es un diccionario
        if type(kwargs) is not dict:

            raise Exception(Union.NOMBRE_CLASE
                            + ".Normal: El parametro se debe pasar "
                            + "{'alias':ClaseOTD}!"
                            )

        return Union(cTipo = Union.NORMAL, **kwargs)


    union = property(fget=__getUnion, doc='Devuelve la clausula de union')
