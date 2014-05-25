# -*- coding: utf-8 -*-
'''
Created on 22/04/2014

@author: cgaray
@contact: cdaniel.py@gmail.com
@summary: Modulo de decoradores de tipos de relaciones entre OTDs
'''

#importamos los modulos y clases necesarias
from moziapi.restricciones import Restriccion


class Uno_a_Muchos(object):
    '''
    Clase decoradora de metodos de relacion (1 - N) entre instancias de OTDBase
    
    '''

    def __init__(self, **kwargs):
        '''
        Inicializador de la clase
        
        clase = clase OTD que representa a la tabla relacionada
        fk    = nombre del atributo de la clase RELACIONADA que es referencia
                a la clave foranea de enlace
        
        '''

        #tomamos los valores de parametros
        self.__cAtrFk = kwargs['fk']
        self.__oOTD = kwargs['clase']
        self.__cNombreAtributo = kwargs['atr']


    def __call__(self, original_func):
        '''
        Este metodo se ejecuta cuando se llama al metodo decorado
        
        '''

        #tomamos una referencia a la esta clase decoradora
        dec = self

        #asignamos las instancias
        def asignador(oPadre):
            #si el atributo aun no existe
            if not hasattr(oPadre, dec.__cNombreAtributo):
                #lo asignamos
                setattr(oPadre, dec.__cNombreAtributo
                           , tuple(oPadre.conexion.lRecuperar(
                                dec.__oOTD
                                , Restriccion.Ig(**{dec.__cAtrFk : oPadre.nId})
                                )))

            #devolvemos la llamada a la funcion original
            return original_func(oPadre)

        return asignador


class Muchos_a_Uno(object):
    '''
    Clase decoradora de metodos de relacion (N - 1) entre instancias OTDBase
    
    '''

    def __init__(self, **kwargs):
        '''
        Inicializador de la clase
        
        clase = clase OTD que representa a la tabla relacionada
        fk    = nombre del atributo de la clase RELACIONADA que es referencia
                a la clave foranea de enlace
        
        '''

        #tomamos los valores de parametros
        self.__cAtrFk = kwargs['fk']
        self.__oOTD = kwargs['clase']
        self.__cNombreAtributo = kwargs['atr']


    def __call__(self, original_func):
        '''
        Este metodo se ejecuta cuando se llama al metodo decorado
        
        '''

        #tomamos una referencia a la esta clase decoradora
        dec = self

        #asignamos las instancias
        def asignador(oPadre):
            #si el atributo aun no existe
            if not hasattr(oPadre, dec.__cNombreAtributo):
                #obtenemos las instancias relacionadas
                for i in oPadre.conexion.lRecuperar(dec.__oOTD
                                , Restriccion.Ig(**{'nId':getattr(oPadre
                                                             , dec.__cAtrFk)})
                                ):
                    #lo asignamos
                    setattr(oPadre, dec.__cNombreAtributo, i)
                    break

            #devolvemos la llamada a la funcion original
            return original_func(oPadre)

        return asignador