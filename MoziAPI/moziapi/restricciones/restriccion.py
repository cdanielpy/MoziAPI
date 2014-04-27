# -*- coding: utf-8 -*-
'''
Created on 11/04/2014

@author: cgaray
@contact: cdaniel.py@gmail.com
@summary: Clase para generacion de criterios de Restriccion de resultados 
'''

#importamos los modulos y clases necesarias
import datetime


class Restriccion(object):
    '''
    Clase para generacion de criterios de Restriccion de resultados
    '''

    NOMBRE_CLASE = 'Restriccion'

    __Y = ' AND '
    __O = ' OR '

    __COMO = " @%s@ LIKE %s "

    __IGUAL = ' @%s@ = %s '
    __NO_IGUAL = ' @%s@ <> %s '

    __MAYOR_QUE = ' @%s@ > %s '
    __MENOR_QUE = ' @%s@ < %s '

    __MAYOR_O_IGUAL_QUE = ' @%s@ >= %s '
    __MENOR_O_IGUAL_QUE = ' @%s@ <= %s '

    __ENTRE = ' @%s@ BETWEEN %s AND %s '


    def __init__(self, cAtributo, oValor, cOperador
                 , bFormatear = True, bModoAtributos = True
                 ):
        '''
        Inicializador de la clase
        
        cAtributo     = nombre del atributo de la clase
        oValor        = valor del atributo de la clase
        cOperador     = operador logico o de comparacion
        cCondicionSQL = condicion en formato sql
        bFormatear    = si el valor se formateara de acuerdo a su tipo para
                        su uso en la sentencia a generar
        bModoAtributos= si se esta generando los datos a partir de atributos
                        comparados con valores
        
        '''

        super(Restriccion, self).__init__()

        self.__cAtributo = cAtributo
        self.__oValor = oValor

        self.__cOperador = cOperador
        self.__bFormatear = bFormatear
        self.__bModoAtributos = bModoAtributos

        #evaluamos el operador
        if cOperador in (Restriccion.__IGUAL
                         , Restriccion.__NO_IGUAL
                         , Restriccion.__MENOR_QUE
                         , Restriccion.__MENOR_O_IGUAL_QUE
                         , Restriccion.__MAYOR_QUE
                         , Restriccion.__MAYOR_O_IGUAL_QUE
                         , Restriccion.__COMO
                         ):

            self.__cSql = cOperador % (cAtributo
                                        , self.__formatoValor(oValor)
                                        )

        elif cOperador in (Restriccion.__Y, Restriccion.__O):
            self.__cSql = cOperador

        elif cOperador is Restriccion.__ENTRE:
            self.__cSql = cOperador % (cAtributo
                                        , self.__formatoValor(oValor[0])
                                        , self.__formatoValor(oValor[-1])
                                        )


    def __getAtributo(self): return self.__cAtributo
    def __getValor(self): return self.__oValor
    def __str__(self): return self.__cSql


    atributo = property(fget=__getAtributo
                        , doc='Devuelve el nombre del atributo'
                        )
    valor = property(fget=__getValor, doc='Devuelve el valor del atributo')


    def getCondiciones(self, oOTD):
        '''
        Devuelve la clausula de condiciones en formato SQL con
        los nombres de campos y sus valores
        
        oOTD = instancia de OTDBase de la cual tomar los atributos
        
        '''

        # reemplazamos en la cadena SQL los valores de atributos por sus nombres
        # de campos de tabla
        if self.__cOperador in (Restriccion.__COMO
                                , Restriccion.__IGUAL
                                , Restriccion.__NO_IGUAL
                                , Restriccion.__MENOR_QUE
                                , Restriccion.__MENOR_O_IGUAL_QUE
                                , Restriccion.__MAYOR_QUE
                                , Restriccion.__MAYOR_O_IGUAL_QUE
                                , Restriccion.__ENTRE
                                ):

            if self.__bModoAtributos:
                __cTemp = oOTD.alias + '.' 
                __cTemp+= oOTD._dicAtributos[self.__cAtributo]
                return self.__cSql.replace('@' + self.__cAtributo + '@'
                                    , __cTemp
                                    )

            else:
                return self.__cSql.replace('@' + self.__cAtributo + '@'
                                            , self.__cAtributo
                                            )

        elif self.__cOperador in [Restriccion.__Y, Restriccion.__O]:

            if self.__bModoAtributos:
                return self.__cOperador.join(' (' + r.getCondiciones(oOTD) + ') ' for r in self.__oValor)

            else:
                return self.__cSql.replace('@' + self.__cAtributo + '@'
                                                , self.__cAtributo
                                                )


    @staticmethod
    def Ig(*atributos, **comparacion):
        '''
        Devuelve una instancia de Restriccion de tipo de comparacion
        con operador IGUAL (=)
        
        atributos   => tupla con nombres de atributos a comparar
        comparacion => atributo = valor a comparar
        
        '''

        #si es un diccionario con al menos un elemento
        if type(comparacion) is dict and len(comparacion) > 0:
            return Restriccion(comparacion.keys()[0]
                           , comparacion.values()[0]
                           , Restriccion.__IGUAL
                           )

        #si es una tupla con al menos dos elementos
        if type(atributos) in (list, tuple) and len(atributos) > 1:
            if type(atributos[1]) is str:
                return Restriccion(atributos[0]
                           , atributos[1]
                           , Restriccion.__IGUAL
                           , False
                           , False
                           )

            else:
                return Restriccion(atributos[0]
                               , atributos[1]
                               , Restriccion.__IGUAL
                               , True
                               , False
                               )

        #sino
        raise Exception(Restriccion.NOMBRE_CLASE + '.Ig()'
                            + ': Se debe especificar el atributo'
                            + ' y el valor a comparar!'
                            )


    @staticmethod
    def Como(*atributos, **comparacion):
        '''
        Devuelve una instancia de Restriccion de tipo de comparacion
        con operador IGUAL (like)
        
        atributos   => tupla con nombres de atributos a comparar
        comparacion => atributo = valor a comparar
        
        '''

        #si es un diccionario con al menos un elemento
        if type(comparacion) is dict and len(comparacion) > 0:
            return Restriccion(comparacion.keys()[0]
                           , comparacion.values()[0]
                           , Restriccion.__COMO
                           )

        #si es una tupla con al menos dos elementos
        if type(atributos) is tuple and len(atributos) > 1:
            return Restriccion(atributos[0]
                           , atributos[1]
                           , Restriccion.__COMO
                           , False
                           , False
                           )

        #sino
        raise Exception(Restriccion.NOMBRE_CLASE + '.Como()'
                            + ': Se debe especificar el atributo'
                            + 'y el valor a comparar!'
                            )


    @staticmethod
    def Dif(*atributos, **comparacion):
        '''
        Devuelve una instancia de Restriccion de tipo de comparacion
        con operador NO IGUAL (<>)
        
        atributos   => tupla con nombres de atributos a comparar
        comparacion => atributo = valor a comparar
        
        '''

        #si es un diccionario con al menos un elemento
        if type(comparacion) is dict and len(comparacion) > 0:
            return Restriccion(comparacion.keys()[0]
                           , comparacion.values()[0]
                           , Restriccion.__IGUAL
                           )

        #si es una tupla con al menos dos elementos
        if type(atributos) in (list, tuple) and len(atributos) > 1:
            if type(atributos[1]) is str:
                return Restriccion(atributos[0]
                           , atributos[1]
                           , Restriccion.__NO_IGUAL
                           , False
                           , False
                           )

            else:
                return Restriccion(atributos[0]
                               , atributos[1]
                               , Restriccion.__NO_IGUAL
                               , True
                               , False
                               )


    @staticmethod
    def May(*atributos, **comparacion):
        '''
        Devuelve una instancia de Restriccion de tipo de comparacion
        con operador MAYOR QUE (>)
        
        atributos   => tupla con nombres de atributos a comparar
        comparacion => atributo = valor a comparar
        
        '''

        #si es un diccionario con al menos un elemento
        if type(comparacion) is dict and len(comparacion) > 0:
            return Restriccion(comparacion.keys()[0]
                           , comparacion.values()[0]
                           , Restriccion.__MAYOR_QUE
                           )

        #si es una tupla con al menos dos elementos
        if type(atributos) is tuple and len(atributos) > 1:
            return Restriccion(atributos[0]
                           , atributos[1]
                           , Restriccion.__MAYOR_QUE
                           , False
                           , False
                           )

        #sino
        raise Exception(Restriccion.NOMBRE_CLASE + '.May()'
                            + ': Se debe especificar el atributo'
                            + ' y el valor a comparar!'
                            )


    @staticmethod
    def Men(*atributos, **comparacion):
        '''
        Devuelve una instancia de Restriccion de tipo de comparacion
        con operador MENOR QUE (<)
        
        atributos   => tupla con nombres de atributos a comparar
        comparacion => atributo = valor a comparar
        
        '''

        #si es un diccionario con al menos un elemento
        if type(comparacion) is dict and len(comparacion) > 0:
            return Restriccion(comparacion.keys()[0]
                           , comparacion.values()[0]
                           , Restriccion.__MENOR_QUE
                           )

        #si es una tupla con al menos dos elementos
        if type(atributos) is tuple and len(atributos) > 1:
            return Restriccion(atributos[0]
                           , atributos[1]
                           , Restriccion.__MENOR_QUE
                           , False
                           , False
                           )

        #sino
        raise Exception(Restriccion.NOMBRE_CLASE + '.Men()'
                            + ': Se debe especificar el atributo'
                            + ' y el valor a comparar!'
                            )

    @staticmethod
    def MayIg(*atributos, **comparacion):
        '''
        Devuelve una instancia de Restriccion de tipo de comparacion
        con operador MAYOR O IGUAL QUE (>=)
        
        atributos   => tupla con nombres de atributos a comparar
        comparacion => atributo = valor a comparar
        
        '''

        #si es un diccionario con al menos un elemento
        if type(comparacion) is dict and len(comparacion) > 0:
            return Restriccion(comparacion.keys()[0]
                           , comparacion.values()[0]
                           , Restriccion.__MAYOR_O_IGUAL_QUE
                           )

        #si es una tupla con al menos dos elementos
        if type(atributos) is tuple and len(atributos) > 1:
            return Restriccion(atributos[0]
                           , atributos[1]
                           , Restriccion.__MAYOR_O_IGUAL_QUE
                           , False
                           , False
                           )

        #sino
        raise Exception(Restriccion.NOMBRE_CLASE + '.MayIg()'
                            + ': Se debe especificar el atributo'
                            + ' y el valor a comparar!'
                            )


    @staticmethod
    def MenIg(*atributos, **comparacion):
        '''
        Devuelve una instancia de Restriccion de tipo de comparacion
        con operador MENOR O IGUAL QUE (<=)
        
        atributos   => tupla con nombres de atributos a comparar
        comparacion => atributo = valor a comparar
        
        '''

        #si es un diccionario con al menos un elemento
        if type(comparacion) is dict and len(comparacion) > 0:
            return Restriccion(comparacion.keys()[0]
                           , comparacion.values()[0]
                           , Restriccion.__MENOR_O_IGUAL_QUE
                           )

        #si es una tupla con al menos dos elementos
        if type(atributos) is tuple and len(atributos) > 1:
            return Restriccion(atributos[0]
                           , atributos[1]
                           , Restriccion.__MENOR_O_IGUAL_QUE
                           , False
                           , False
                           )

        #sino
        raise Exception(Restriccion.NOMBRE_CLASE + '.MenIg()'
                            + ': Se debe especificar el atributo'
                            + ' y el valor a comparar!'
                            )


    @staticmethod
    def Entre(**comparacion):
        '''
        Devuelve una instancia de Restriccion de tipo de comparacion
        con operador IGUAL
        
        parametros => atributo = [minimo, maximo] a comparar
        
        '''

        if type(comparacion) is not dict \
            or type(comparacion.values().pop()) not in (list, tuple):
            raise Exception(Restriccion.NOMBRE_CLASE + '.Entre()'
                            + ': Se debe especificar el atributo'
                            + ' y los valores limites!'
                            )

        return Restriccion(comparacion.keys().pop()
                           , comparacion.values().pop()
                           , Restriccion.__ENTRE
                           )


    @staticmethod
    def Y(lRestricciones):
        '''
        Devuelve una instancia de Restriccion de tipo de logico
        con operador Y (and)
        
        lRestricciones = lista de instancias de Restriccion
        
        Ej.
            [Restriccion.Ig(..), Restriccion.Entre(..), ...] 
        
        '''

        if type(lRestricciones) not in (list, tuple) or len(lRestricciones) < 2:
            raise Exception(Restriccion.NOMBRE_CLASE + '.Y()'
                            + ': Se deben pasar al menos 2 instancias'
                            + ' de Restriccion!'
                            )

        else:
            #validamos cada elemento de la lista
            for r in lRestricciones:
                if type(r) is not Restriccion:
                    raise Exception(Restriccion.NOMBRE_CLASE + '.Y()'
                            + ': Se deben ser instancias de Restriccion!'
                            )

        return Restriccion(None, lRestricciones, Restriccion.__Y)


    @staticmethod
    def O(lRestricciones):
        '''
        Devuelve una instancia de Restriccion de tipo de logico
        con operador O (or)
        
        lRestricciones = lista de instancias de Restriccion
        
        Ej.
            (Restriccion.Ig(..), Restriccion.Entre(..), ...)
        
        '''

        if type(lRestricciones) not in (list, tuple) \
            or len(lRestricciones) < 2:

            raise Exception(Restriccion.NOMBRE_CLASE + '.O()'
                            + ': Se deben pasar al menos 2 instancias'
                            + ' de Restriccion!'
                            )

        else:
            #validamos cada elemento de la lista/tupla
            for r in lRestricciones:
                if type(r) is not Restriccion:
                    raise Exception(Restriccion.NOMBRE_CLASE + '.O()'
                            + ': Se deben ser instancias de Restriccion!'
                            )

        return Restriccion(None, lRestricciones, Restriccion.__O)


    def __formatoValor(self, oValor):
        '''
        Devuelve el parametro de valor formateado de acuerdo a su tipo
        
        oValor = instancia del valor a formatear
        
        '''

        #si no se debe formatear, lo devolvemos tal cual
        if not self.__bFormatear: return oValor

        if type(oValor) in (str, unicode): return "'" + oValor + "'"

        if type(oValor) in (float, int, long): return oValor

        if type(oValor) is datetime.datetime:
            return oValor.strftime("'%Y-%m-%d %H:%M:%S'")

        return oValor