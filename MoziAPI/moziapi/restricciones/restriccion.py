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

    _Y_ = ' AND '
    _O_ = ' OR '

    _COMO_ = " @%s@ LIKE %s "

    _IGUAL_ = ' @%s@ = %s '
    _NO_IGUAL_ = ' @%s@ <> %s '

    _MAYOR_QUE_ = ' @%s@ > %s '
    _MENOR_QUE_ = ' @%s@ < %s '

    _MAYOR_O_IGUAL_QUE_ = ' @%s@ >= %s '
    _MENOR_O_IGUAL_QUE_ = ' @%s@ <= %s '

    _ENTRE_ = ' @%s@ BETWEEN %s AND %s '


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

        if cOperador in (Restriccion._IGUAL_
                         , Restriccion._NO_IGUAL_
                         , Restriccion._MENOR_QUE_
                         , Restriccion._MENOR_O_IGUAL_QUE_
                         , Restriccion._MAYOR_QUE_
                         , Restriccion._MAYOR_O_IGUAL_QUE_
                         , Restriccion._COMO_
                         ):
            self.__cSql = cOperador % (cAtributo
                                        , self.__formatoValor(oValor)
                                        )

        elif cOperador in (Restriccion._Y_, Restriccion._O_):
            self.__cSql = cOperador

        elif cOperador is Restriccion._ENTRE_:
            self.__cSql = cOperador % (cAtributo
                                        , self.__formatoValor(oValor[0])
                                        , self.__formatoValor(oValor[-1])
                                        )


    def __getAtributo(self): return self.__cAtributo
    def __getValor(self): return self.__oValor
    def __str__(self): return self.__cSql


    atributo = property(fget=__getAtributo, doc='Devuelve el nombre del atributo')
    valor = property(fget=__getValor, doc='Devuelve el valor del atributo')


    def getCondiciones(self, oOTD):
        '''
        Devuelve la clausula de condiciones en formato SQL con
        los nombres de campos y sus valores
        
        oOTD = instancia de OTDBase de la cual tomar los atributos
        
        '''

        # reemplazamos en la cadena SQL los valores de atributos por sus nombres
        # de campos de tabla
        if self.__cOperador in (Restriccion._COMO_
                                , Restriccion._IGUAL_
                                , Restriccion._NO_IGUAL_
                                , Restriccion._MENOR_QUE_
                                , Restriccion._MENOR_O_IGUAL_QUE_
                                , Restriccion._MAYOR_QUE_
                                , Restriccion._MAYOR_O_IGUAL_QUE_
                                , Restriccion._ENTRE_
                                ):

            if self.__bModoAtributos:
                self.__cSql = self.__cSql.replace('@' + self.__cAtributo + '@'
                                            , oOTD.alias + '.' + oOTD._dicAtributos[self.__cAtributo]
                                            )

            else:
                #self.__cSql = ' (' + self.__cOperador % (self.__cAtributo, self.__oValor) + ') '
                self.__cSql = self.__cOperador % (self.__cAtributo, self.__oValor)
                self.__cSql = self.__cSql.replace('@' + self.__cAtributo + '@'
                                                , self.__cAtributo
                                                )

        elif self.__cOperador in [Restriccion._Y_, Restriccion._O_]:

            if self.__bModoAtributos:
                self.__cSql = self.__cOperador.join([' (' + r.getCondiciones(oOTD) + ') ' for r in self.__oValor])

            else:
                #self.__cSql = ' (' + self.__cOperador % (self.__cAtributo, self.__oValor) + ') '
                self.__cSql = self.__cOperador % (self.__cAtributo, self.__oValor)
                self.__cSql = self.__cSql.replace('@' + self.__cAtributo + '@'
                                                , self.__cAtributo
                                                )

        #devolvemos la condicion pero como sentencia SQL
        return self.__cSql


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
                           , Restriccion._IGUAL_
                           )

        #si es una tupla con al menos dos elementos
        if type(atributos) is tuple and len(atributos) > 1:
            return Restriccion(atributos[0]
                           , atributos[1]
                           , Restriccion._IGUAL_
                           , False
                           , False
                           )

        #sino
        raise Exception(Restriccion.NOMBRE_CLASE + '.Ig()'
                            + ': Se debe especificar el atributo y el valor a comparar!'
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
                           , Restriccion._COMO_
                           )

        #si es una tupla con al menos dos elementos
        if type(atributos) is tuple and len(atributos) > 1:
            return Restriccion(atributos[0]
                           , atributos[1]
                           , Restriccion._COMO_
                           , False
                           , False
                           )

        #sino
        raise Exception(Restriccion.NOMBRE_CLASE + '.Como()'
                            + ': Se debe especificar el atributo y el valor a comparar!'
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
                           , Restriccion._NO_IGUAL_
                           )

        #si es una tupla con al menos dos elementos
        if type(atributos) is tuple and len(atributos) > 1:
            return Restriccion(atributos[0]
                           , atributos[1]
                           , Restriccion._NO_IGUAL_
                           , False
                           , False
                           )

        #sino
        raise Exception(Restriccion.NOMBRE_CLASE + '.Dif()'
                            + ': Se debe especificar el atributo y el valor a comparar!'
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
                           , Restriccion._MAYOR_QUE_
                           )

        #si es una tupla con al menos dos elementos
        if type(atributos) is tuple and len(atributos) > 1:
            return Restriccion(atributos[0]
                           , atributos[1]
                           , Restriccion._MAYOR_QUE_
                           , False
                           , False
                           )

        #sino
        raise Exception(Restriccion.NOMBRE_CLASE + '.May()'
                            + ': Se debe especificar el atributo y el valor a comparar!'
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
                           , Restriccion._MENOR_QUE_
                           )

        #si es una tupla con al menos dos elementos
        if type(atributos) is tuple and len(atributos) > 1:
            return Restriccion(atributos[0]
                           , atributos[1]
                           , Restriccion._MENOR_QUE_
                           , False
                           , False
                           )

        #sino
        raise Exception(Restriccion.NOMBRE_CLASE + '.Men()'
                            + ': Se debe especificar el atributo y el valor a comparar!'
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
                           , Restriccion._MAYOR_O_IGUAL_QUE_
                           )

        #si es una tupla con al menos dos elementos
        if type(atributos) is tuple and len(atributos) > 1:
            return Restriccion(atributos[0]
                           , atributos[1]
                           , Restriccion._MAYOR_O_IGUAL_QUE_
                           , False
                           , False
                           )

        #sino
        raise Exception(Restriccion.NOMBRE_CLASE + '.MayIg()'
                            + ': Se debe especificar el atributo y el valor a comparar!'
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
                           , Restriccion._MENOR_O_IGUAL_QUE_
                           )

        #si es una tupla con al menos dos elementos
        if type(atributos) is tuple and len(atributos) > 1:
            return Restriccion(atributos[0]
                           , atributos[1]
                           , Restriccion._MENOR_O_IGUAL_QUE_
                           , False
                           , False
                           )

        #sino
        raise Exception(Restriccion.NOMBRE_CLASE + '.MenIg()'
                            + ': Se debe especificar el atributo y el valor a comparar!'
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
                            + ': Se debe especificar el atributo y los valores limites!'
                            )

        return Restriccion(comparacion.keys().pop()
                           , comparacion.values().pop()
                           , Restriccion._ENTRE_
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
                            + ': Se deben pasar al menos 2 instancias de Restriccion!'
                            )

        else:
            #validamos cada elemento de la lista
            for r in lRestricciones:
                if type(r) is not Restriccion:
                    raise Exception(Restriccion.NOMBRE_CLASE + '.Y()'
                            + ': Se deben ser instancias de Restriccion!'
                            )

        return Restriccion(None, lRestricciones, Restriccion._Y_)


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
                            + ': Se deben pasar al menos 2 instancias de Restriccion!'
                            )

        else:
            #validamos cada elemento de la lista/tupla
            for r in lRestricciones:
                if type(r) is not Restriccion:
                    raise Exception(Restriccion.NOMBRE_CLASE + '.O()'
                            + ': Se deben ser instancias de Restriccion!'
                            )

        return Restriccion(None, lRestricciones, Restriccion._O_)


    def __formatoValor(self, oValor):
        '''
        Devuelve el parametro de valor formateado de acuerdo a su tipo
        
        oValor = instancia del valor a formatear
        
        '''

        #si no se debe formatear, lo devolvemos tal cual
        if not self.__bFormatear: return oValor

        if type(oValor) is str:
            return "'" + oValor + "'"

        if type(oValor) in [float, int, long]:
            return oValor

        if type(oValor) is datetime.datetime:
            return oValor.strftime("'%Y-%m-%d %H:%M:%S'")

        return oValor