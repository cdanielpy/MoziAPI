# -*- coding: utf-8 -*-
'''
Created on 10/04/2014

@author: cgaray
@contact: cdaniel.py@gmail.com
@summary: Clase base para modelo de tablas de bases de datos 
'''


# importamos los modulos y clases necesarias
from org.moziapi.restricciones import Restriccion
from org.moziapi.uniones.union import Union


class OTDBase(object):
    '''
    Clase base para modelo de tablas de bases de datos
    '''


    def __init__(self, cNombreTabla, **kwargs):
        '''
        Inicializador de la clase
        
        cNombreTabla = Nombre de la tabla fisica
        
        '''

        self.cNombreTabla = cNombreTabla

        self._nId = 0
        self._cDescripcion = ''
        self._dicAtributos = {v:k for k, v in self._dicCampos.iteritems()}

        if kwargs.get('cAlias'):
            self.__cAlias = str(kwargs.get('cAlias'))
            kwargs.__delitem__('cAlias')

        else: self.__cAlias = '_this_'

        self._cListaCampos = None
        self._cSelect = None

        # lo recorremos
        for k in kwargs:
            # asignamos los valores a los atributos correspondientes
            self.__setattr__(self._dicCampos[k], kwargs[k])


    def __str__(self):
        '''
        Devuelve la representacion de cadena
        
        '''

        return '<%s - %s>' % (self._nId, self._cDescripcion)


    def _getListaCampos(self):
        '''
        Devuelve la lista de camos de la tabla administrada lista para ser
        utilizada en una consulta
        
        '''

        # si el atributo YA fue establecido, devolvemos la cadena de sentencia
        if self._cListaCampos is not None: return self._cListaCampos

        # le asignamos su valor
        __cTemp = (', ' + self.alias + '.').join(self._dicCampos.keys())
        __cTemp = self.__cAlias  + '.' + __cTemp 
        self._cListaCampos = '%(campos)s' % {'campos': __cTemp}

        #devolvemos la sentecia
        return self._cListaCampos



    def __getAlias(self): return self.__cAlias
    def __setAlias(self, cAlias): self.__cAlias = cAlias



    def _getSelect(self):
        '''
        Devuelve la sentencia SELECT para la tabla administrada
        
        '''

        # si el atributo YA fue establecido, devolvemos la cadena de sentencia
        if self._cSelect is not None: return self._cSelect

        # le asignamos su valor
        self._cSelect = 'SELECT %(campos)s FROM %(tabla)s AS %(alias)s '
        self._cSelect = self._cSelect % {'campos': self._getListaCampos()
                                       , 'tabla':self.cNombreTabla
                                       , 'alias':self.alias
                                       }

        #devolvemos la sentecia
        return self._cSelect


    def filtrar(self, oRestriccion):
        '''
        Devuelve la sentencia SELECT para la tabla administrada
        agregando las restrincciones de filtrado de registros
        
        oRestriccion = instancia de Restriccion o condicion SQL
            Ej. Restriccion.Ig(nombreAtributo = 15) o 'CAMPO = 15'
        
        '''

        # si se una instancia de Restriccion
        if type(oRestriccion) is Restriccion:
            # recuperamos las cadenas de condiciones
            return self._getSelect() + (' WHERE %s' % oRestriccion.getCondiciones(self))

        #si es una cadena
        elif type(oRestriccion) is str:
            # simplemente le anadimos la condicion
            return self._getSelect() + (' WHERE %s' % oRestriccion)

        # resultado por defecto
        else: return self._getSelect()


    def unir(self, oUnion):
        '''
        Devuelve la sentencia SELECT para la tabla administrada
        agregando las uniones con las instancias indicadas en el parametro
        
        oUnion = instancia de Union
            Ej. Union.Normal('aliasTabla'= ClaseOTD)
        
        '''

        # si se recibe el diccionario parametro
        if type(oUnion) is Union:
            oUnion.setUniones(self)
            self._cSelect = self.select + oUnion.union



    alias = property(fget=__getAlias, fset= __setAlias
                     , doc='Devuelve o establece el alias SQL asignado a la tabla'
                     )

    listaCampos = property(fget=_getListaCampos
                          , doc='Devuelve la lista de campos de tabla'
                          )

    select = property(fget=_getSelect
                      , doc='Devuelve el comando SELECT campos FROM tabla'
                      )
