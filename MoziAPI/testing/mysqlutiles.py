#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 13/04/2014

@author: daniel
@contact: cdaniel.py@gmail.com
@summary: Clase de administración de conexion a un motor MySQL

        Para este ejemplo se utiliza el modulo mysql/python connector
        descargable desde la pagina de la misma mysql
        en el siguiente enlace
        http://dev.mysql.com/downloads/connector/python/1.1.html
        
'''



# importamos los modulos y librerias necesarias
import mysql.connector
from moziapi.bases import ConectorBase



class MySqlUtiles(ConectorBase):
    '''
    Clase de administración de conexion a un motor MySQL
    
    '''

    NOMBRE_CLASE = 'MySqlUtiles'


    def __init__(self, cServidor
                , cServicio
                , cCatalogo
                , cUsuario
                , cContrasena
                , nPuerto=3306
                , nTiempoEspera=300
                , nMaxPool=10
                ):
        '''
        Inicializador de la clase
        
        cServidor
        cServicio
        cCatalogo
        cUsuario
        cContrasena
        nPuerto
        nTiempoEspera
        nMaxPool = cantidad de conexiones en pool
        
        '''

        # invocamos al inicializador de la clase base
        super(MySqlUtiles, self).__init__()

        self._cServidor = cServidor
        self._nPuerto = nPuerto
        self._cServicio = cServicio
        self._cCatalogo = cCatalogo

        self._cUsuario = cUsuario
        self._cContrasena = cContrasena
        self._nTiempoEspera = nTiempoEspera
        self._nMaxPool = nMaxPool


    def lConectar(self):
        '''
        Ejecuta un intento de conexion al motod de base de datos y devuelve
        una lista de resultados (int, string)
        
        '''

        NOMBRE_METODO = self.NOMBRE_CLASE + '.lConectar()'

        # resultado por defecto
        lResultado = (0, NOMBRE_METODO + ' No Ejecutado!')

        try:
            # intentamos iniciar la conexion
            self._oConexion = mysql.connector.connect(host=self._cServidor
                                              , user=self._cUsuario
                                              , password=self._cContrasena
                                              , database=self._cCatalogo
                                              , port=self._nPuerto
                                              , pool_size=self._nMaxPool
                                              , buffered = True
                                              )

            # establecemos el resultado del metodo
            lResultado = (1, 'Ok')

            # establecemos el marcador de conexion activa
            self._bConectado = True

        except BaseException, oError:
            # en caso de error, devolvemos el error como parte del resultado
            lResultado = (-1, NOMBRE_METODO + ' Error: ' + str(oError))

        # devolvemos el resultado del metodo
        return lResultado


    def lDesconectar(self):
        '''
        Ejecuta la llamada al metodo de finalizacion de la conexion existente
        y devuelve una lista de resultados (int, string)
        
        '''

        NOMBRE_METODO = self.NOMBRE_CLASE + '.lDesconectar()'

        # resultado por defecto
        lResultado = (0, NOMBRE_METODO + ' No Ejecutado!')

        try:
            # intentamos iniciar la conexion
            self._oConexion.close()

            # establecemos el resultado del metodo
            lResultado = (1, 'Ok')

            # establecemos el marcador de conexion cerrada
            self._bConectado = False

        except BaseException, oError:
            # en caso de error, devolvemos el error como parte del resultado
            lResultado = (-1, NOMBRE_METODO + ' Error: ' + str(oError))

        # devolvemos el resultado del metodo
        return lResultado


    def lConfirmar(self):
        '''
        Ejecuta la llamada al metodo de confirmacion de una transaccion
        exitentes y devuelve una lista de resultados (int, string)
        
        '''

        NOMBRE_METODO = self.NOMBRE_CLASE + '.lConfirmar()'

        # resultado por defecto
        lResultado = (0, NOMBRE_METODO + ' No Ejecutado!')

        try:
            # intentamos confirmar la transaccion
            self._oConexion.commit()

            # establecemos el resultado del metodo
            lResultado = (1, 'Ok')

        except BaseException, oError:
            # en caso de error, devolvemos el error como parte del resultado
            lResultado = (-1, NOMBRE_METODO + ' Error: ' + str(oError))

        # devolvemos el resultado del metodo
        return lResultado


    def lRevertir(self):
        '''
        Ejecuta la llamada al metodo de reversion de una transaccion
        exitentes y devuelve una lista de resultados (int, string)
        
        '''

        NOMBRE_METODO = self.NOMBRE_CLASE + '.lRevertir()'

        # resultado por defecto
        lResultado = (0, NOMBRE_METODO + ' No Ejecutado!')

        try:
            # intentamos revertir la transaccion
            self._oConexion.rollback()

            # establecemos el resultado del metodo
            lResultado = (1, 'Ok')

        except BaseException, oError:
            # en caso de error, devolvemos el error como parte del resultado
            lResultado = (-1, NOMBRE_METODO + ' Error: ' + str(oError))

        # devolvemos el resultado del metodo
        return lResultado


    def lEjecutarConsulta(self, cConsultaSQL, tParametros=None):
        '''
        Ejecuta la preparacion de ejecucion de una consulta
        mediante una instancia de Cursor y devuelve una lista
        de resultados (int, object)
        
        Si se ejecuto correctamente, el segundo elemento de la lista
        es la instancia de Cursor
        
        cConsultaSQL = Consulta SQL a ejecutar
        tParametros  = Valores de parametros de la Consulta
        
        '''

        NOMBRE_METODO = self.NOMBRE_CLASE + '.lEjecutarConsulta()'

        # resultado por defecto
        lResultado = (0, NOMBRE_METODO + ' No Ejecutado!')

        try:
            # intentamos instanciar un cursor
            oCursor = self._oConexion.cursor()

            # ejecutamos la consulta
            if tParametros is not None:
                self._mostrarComando(cConsultaSQL % tParametros)
                oCursor.execute(cConsultaSQL, tParametros)

            else:
                self._mostrarComando(cConsultaSQL)
                oCursor.execute(cConsultaSQL)

            # establecemos el resultado del metodo
            lResultado = (1, oCursor)

        except BaseException, oError:
            # en caso de error, devolvemos el error como parte del resultado
            lResultado = (-1, NOMBRE_METODO + ' Error: ' + str(oError))

        # devolvemos el resultado del metodo
        return lResultado


    def lEjecutarSentencia(self, cSentenciaSQL, tParametros=None):
        '''
        Ejecuta una sentencia sql y devuelve una lista
        de resultados (int, string)
        
        cConsultaSQL = Sentencia SQL a ejecutar
        tParametros  = Valores de parametros de la Sentencia
        
        '''
        
        NOMBRE_METODO = self.NOMBRE_CLASE + '.lEjecutarSentencia()'

        # resultado por defecto
        lResultado = (0, NOMBRE_METODO + ' No Ejecutado!')

        try:
            # intentamos instanciar un cursor
            oCursor = self._oConexion.cursor()

            # ejecutamos la consulta
            if tParametros is not None:
                self._mostrarComando(cSentenciaSQL % tParametros)
                oCursor.execute(cSentenciaSQL, tParametros)

            else:
                self._mostrarComando(cSentenciaSQL)
                oCursor.execute(cSentenciaSQL)

            # establecemos el resultado del metodo
            lResultado = (1, 'Ok')

            # cerramos el cursor
            oCursor.close()

        except BaseException, oError:
            # en caso de error, devolvemos el error como parte del resultado
            lResultado = (-1, NOMBRE_METODO + ' Error: ' + str(oError))

        # devolvemos el resultado del metodo
        return lResultado


