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

        self._oConexion = None

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


    def gRecuperar(self, clsClaseOTD, oRestricciones):
        '''
        Ejecuta la consulta de datos aplicando las restricciones indicadas
        y devolviendo un generador de instancias de la clase especificada
        
        clsClaseOTD    = clase derivada de OTDBase
        oRestricciones = instancia de Restriccion
        
        '''

        #establecemos la conexion interna actual de la clase
        clsClaseOTD.conexion = self

        #generamos un cursor con los datos de peticiones
        lRes = self.lEjecutarConsulta(clsClaseOTD().filtrar(oRestricciones))

        #si no se pudo ejecutar
        if lRes[0] != 1: raise Exception(lRes[1])

        #tomamos los nombres de campos de la tabla
        tCampos = (clsClaseOTD()._dicCampos.keys())

        #devolvemos un generador
        return (clsClaseOTD(**dict(zip(tCampos, tFila))) for tFila in lRes[1])


    def lEjecutarConsulta(self, cConsultaSQL, tParametros):
        raise NotImplementedError

    def lEjecutarSentencia(self, cSentenciaSQL, tParametros):
        raise NotImplementedError

    def lEjecutarProcedimiento(self, cComandoSQL, tParametros):
        raise NotImplementedError

    def bConectado(self):
        raise NotImplementedError

    def mostrarSQL(self, bValor):
        '''
        Establece si se muestran o no las sentencias ejecutadas
        
        bValor = [True|False]
        
        '''

        self._bMostrarSql = bValor

    def __str__(self):
        '''
        Devuelve la representacion de cadena de la instancia
        
        '''

        return '<%s %s@%s/%s>' % (self.NOMBRE_CLASE
                                   , self._cUsuario
                                   , self._cServidor
                                   , self._cServicio
                                   )


    def _mostrarComando(self, cComando):
        '''
        Imprime en pantalla el comando parametro
        
        cComando = comando sql
        
        '''

        if self._bMostrarSql: print cComando