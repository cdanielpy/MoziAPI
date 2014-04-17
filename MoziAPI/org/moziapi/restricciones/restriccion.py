# -*- coding: utf-8 -*-
'''
Created on 11/04/2014

@author: cgaray
@contact: cdaniel.py@gmail.com
@summary: Clase para generacion de criterios de Restriccion de resultados 
'''


class Restriccion(object):
    '''
    Clase para generacion de criterios de Restriccion de resultados
    '''

    NOMBRE_CLASE = 'Restriccion'

    Y = 'AND'
    O = 'OR'

    COMO = 'LIKE'

    IGUAL = '='
    MAYOR_QUE = '>'
    MENOR_QUE = '<'

    MAYOR_O_IGUAL_QUE = '>='
    MENOR_O_IGUAL_QUE = '<='

    ENTRE = 'BETWEEN'

    def __init__(self, cAtributo, oValor, cOperador):
        '''
        Inicializador de la clase
        
        cAtributo     = nombre del atributo de la clase
        oValor        = valor del atributo de la clase
        cOperador     = operador logico o de comparacion
        cCondicionSQL = condicion en formato sql
        
        '''

        super(Restriccion, self).__init__()

        self.__cAtributo = cAtributo
        self.__oValor = oValor

        self.__cOperador = cOperador

        if cOperador is Restriccion.IGUAL:
            self.__cCondicionSQL = (" @%s@ = '%s' " if type(oValor) is str else ' @%s@ = %s ') % (cAtributo, oValor)
            
        elif cOperador is Restriccion.Y:
            self.__cCondicionSQL = ' %s AND %s '
        elif cOperador is Restriccion.O:
            self.__cCondicionSQL = ' (%s) OR (%s) '
        elif cOperador is Restriccion.ENTRE:
            self.__cCondicionSQL = ' @%s@ BETWEEN %s AND %s ' % (cAtributo, oValor[0], oValor[1])


    def __getAtributo(self): return self.__cAtributo

    def __getValor(self): return self.__oValor

    def __str__(self): return self.__cCondicionSQL


    atributo = property(fget=__getAtributo, doc='Devuelve el nombre del atributo')
    valor = property(fget=__getValor, doc='Devuelve el valor del atributo')


    def getCondiciones(self, oOTD):
        '''
        Devuelve la cadena de condiciones en formato SQL con
        los nombres de campos y sus valores
        
        oOTD = instancia de OTDBase de la cual tomar los atributos
        
        '''

        #reemplazamos en la cadena SQL los valores de atributos por sus nombres
        #de campos de tabla
        if self.__cOperador in [Restriccion.COMO, Restriccion.IGUAL, Restriccion.ENTRE]:
            return self.__cCondicionSQL.replace('@' + self.__cAtributo + '@'
                                            , oOTD._dicAtributos[self.__cAtributo]
                                            )

        elif self.__cOperador in [Restriccion.Y, Restriccion.O]:
            return self.__cCondicionSQL % (self.__cAtributo.getCondiciones(oOTD)
                                    , self.__oValor.getCondiciones(oOTD)
                                    )


    @staticmethod
    def Ig(**comparacion):
        '''
        Devuelve una instancia de Restriccion de tipo de comparacion
        con operador IGUAL
        
        parametros => atributo = valor a comparar
        
        '''

        if(type(comparacion) is not dict):
            raise Exception(Restriccion.NOMBRE_CLASE + '.Ig'
                            + ': Se debe especificar el atributo y el valor a comparar!'
                            )

        return Restriccion(comparacion.keys()[0]
                           , comparacion.values()[0]
                           , Restriccion.IGUAL
                           )

    @staticmethod
    def Entre(**comparacion):
        '''
        Devuelve una instancia de Restriccion de tipo de comparacion
        con operador IGUAL
        
        parametros => atributo = [valorMinimo, valorMaximo] a comparar
        
        '''

        if type(comparacion) is not dict \
            or type(comparacion.values().pop()) is not list:
            raise Exception(Restriccion.NOMBRE_CLASE + '.Entre'
                            + ': Se debe especificar el atributo y los valores limites!'
                            )

        return Restriccion(comparacion.keys().pop()
                           , comparacion.values().pop()
                           , Restriccion.ENTRE
                           )


    @staticmethod
    def Y(restriccion_0, restriccion_1):
        '''
        Devuelve una instancia de Restriccion de tipo de logico
        con operador Y (and)
        
        restriccion_0 = instancia de Resctriccion
        restriccion_1 = instancia de Resctriccion
        
        '''

        if(type(restriccion_0) is not Restriccion
           or type(restriccion_1) is not Restriccion):
            raise Exception(Restriccion.NOMBRE_CLASE + '.Y'
                            + ': Los parametros deben ser instancias de Restriccion!'
                            )

        return Restriccion(restriccion_0, restriccion_1, Restriccion.Y)


    @staticmethod
    def O(restriccion_0, restriccion_1):
        '''
        Devuelve una instancia de Restriccion de tipo de logico
        con operador O (or)
        
        restriccion_0 = instancia de Resctriccion
        restriccion_1 = instancia de Resctriccion
        
        '''

        if(type(restriccion_0) is not Restriccion
           or type(restriccion_1) is not Restriccion):
            raise Exception(Restriccion.NOMBRE_CLASE + '.O'
                            + ': Los parametros deben ser instancias de Restriccion!'
                            )

        return Restriccion(restriccion_0, restriccion_1, Restriccion.O)
