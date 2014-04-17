# -*- coding: utf-8 -*-
'''
Created on 09/04/2014

@author: cgaray
@contact: cdaniel.py@gmail.com
@summary: Clase base para utilerias de conexion a motores de bases de datos
'''

class ConectorBase(object):
    '''
    Clase base para utilerias de conexion a motores de bases de datos
    '''


    def __init__(self):
        '''
        Inicializador de la clase
        '''

        self.__oConexion = None

        self._cServidor = ''
        self._nPuerto = 0
        self._cServicio = ''
        self._cCatalogo = ''

        self._cUsuario = ''
        self._cContrasena = ''
        self._nTiempoEspera = 300

        self._bMostrarSql = False
        self._bConectado = False


    def lConectar(self):
        raise NotImplementedError


    def lDesconectar(self):
        raise NotImplementedError


    def lConfirmar(self):
        raise NotImplementedError


    def lRevertir(self):
        raise NotImplementedError


    def lEjecutarConsulta(self, cConsultaSQL, tParametros):
        raise NotImplementedError

    def lEjecutarSentencia(self, cSentenciaSQL, tParametros):
        raise NotImplementedError


    def lEjecutarProcedimiento(self, cConsultaSQL, tParametros):
        raise NotImplementedError

    def bConectado(self):
        raise NotImplementedError

    def mostrarSQL(self):
        raise NotImplementedError

    def __str__(self):
        '''
        Devuelve la representacion de cadena de la instancia
        
        '''

        return '<%s %s %s>' % (self.NOMBRE_CLASE
                               , self._cServidor
                               , self._cServicio
                               )


    def _mostrarComando(self, cComando):
        '''
        Imprime en pantalla el comando parametro
        
        cComando = comando sql
        
        '''

        if self._bMostrarSql: print cComando