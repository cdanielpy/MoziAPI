# -*- coding: utf-8 -*-
'''
Created on 10/04/2014

@author: cgaray
@contact: cdaniel.py@gmail.com
@summary: Clase base para modelo de tablas de bases de datos 
'''


#importamos los modulos y clases necesarias
from org.moziapi.restricciones import Restriccion



class OTDBase(object):
    '''
    Clase base para modelo de tablas de bases de datos
    '''


    def __init__(self, cNombreTabla):
        '''
        Inicializador de la clase
        
        cNombreTabla = Nombre de la tabla fisica
        
        '''

        self.cNombreTabla = cNombreTabla

        self._nId = 0
        self._cDescripcion = ''

        self._dicAtributos = {v:k for k, v in self._dicCampos.iteritems()}

        self._cSelect = None


    def __str__(self):
        return '<%s - %s>' % (self._nId, self._cDescripcion)


    def _getSelect(self):
        '''
        Devuelve la sentencia SELECT para la tabla administrada
        '''


        #si el atributo aun no fue establecido
        if self._cSelect is None:
            #le asignamos su valor
            self._cSelect = 'SELECT %(campos)s FROM %(tabla)s'
            self._cSelect = self._cSelect % {'campos': ', '.join(self._dicCampos.keys())
                                               , 'tabla':self.cNombreTabla
                                               }


        #devolvemos la cadena de sentencia
        return self._cSelect


    def filtrar(self, oRestriccion):
        '''
        Devuelve la sentencia SELECT para la tabla administrada
        agregando las restrincciones de filtrado de registros
        
        oRestriccion = instancia de Restriccion o condicion SQL
            Ej. Restriccion.Ig(nombreAtributo = 15) o 'CAMPO = 15'
        '''

        #si se recibe el diccionario parametro
        if type(oRestriccion) is Restriccion:
            #le agregamos los parametros de filtrado
            return self._getSelect() + (' WHERE %s' % oRestriccion.getCondiciones(self))

        elif type(oRestriccion) is str:
            #le agregamos los parametros de filtrado
            return self._getSelect() + (' WHERE %s' % oRestriccion)
        
        else:
            #resultado por defecto
            return self._getSelect()


    select = property(fget = _getSelect
                      , doc = 'Devuelve el comando SELECT campos FROM tabla'
                      )