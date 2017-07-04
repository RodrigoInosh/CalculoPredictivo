# -*- coding: iso-8859-15 -*-
'''
Created on 12-02-2014

@author: CRodriguez
'''
import arcpy

class ParametrosFormulario:
    # PARAMETROS POR DEFECTO - CAMBIAR SEGUN TIPO DE SERVICIO AM,FM, RCC, ISDBT o UHF
    _recomendacion = "1546"
    _potencia = 250
    _ganancia = 3
    _alturaAntenaTransmisora = 25
    _alturaAntenaReceptora = 10
    _latitud = -32.4247222
    _longitud = -70.6325
    _perdidaCablesConectores = 1
    _perdidaDivisorPotencia = 0
    _otrasPerdidas = 0
    _radiales = 72        
    _perdidasLobulo = [0] * 72
    _obstaculosCircundantesTx = 10
    _obstaculosCircundantesRx = 10
    _toleranciaZonasSombra = 1
    _resolucionCalculo = 500
    _porcentajeTiempo = 50
    _porcentajeUbicacion = 90
    _frecuencia = 99.3
    _intensidadCampoReferencia = 48
    _imagen = "" #"c:\\arcgisserver\\Subtel2.sde\\Subtel2_prod.SUBTEL2.Imagen"
    _multiplo = 1
        
    def __init__(self):
        #cn = arcpy.CreateDatabaseConnection_management(arcpy.env.scratchFolder,"cn","SQL_SERVER","192.168.3.17","DATABASE_AUTH","subtel2","subtel2","SAVE_USERNAME","Subtel2_prod","subtel2")
        #self._imagen = arcpy.env.scratchFolder + "\\cn.sde\\Subtel2_prod.SUBTEL2.Imagen"
        self.recomendacion = self._recomendacion
        self.potencia = self._potencia
        self.ganancia = self._ganancia
        self.alturaAntenaTransmisora = self._alturaAntenaTransmisora
        self.alturaAntenaReceptora = self._alturaAntenaReceptora
        self.latitud = self._latitud
        self.longitud = self._longitud
        self.perdidaCablesConectores = self._perdidaCablesConectores
        self.perdidaDivisorPotencia = self._perdidaDivisorPotencia
        self.otrasPerdidas = self._otrasPerdidas
        self.radiales = self._radiales        
        self.perdidasLobulo = self._perdidasLobulo
        self.obstaculosCircundantesTx = self._obstaculosCircundantesTx
        self.obstaculosCircundantesRx = self._obstaculosCircundantesRx
        self.toleranciaZonasSombra = self._toleranciaZonasSombra
        self.resolucionCalculo = self._resolucionCalculo
        self.porcentajeTiempo = self._porcentajeTiempo
        self.porcentajeUbicacion = self._porcentajeUbicacion
        self.frecuencia = self._frecuencia
        self.intensidadCampoReferencia = self._intensidadCampoReferencia
        self.imagen = self._imagen
        self.multiplo = self._multiplo
    '''
        se convierte la cadena de texto separada por coma en una lista
        y se pasan los valores de la lista de perdidas por lobulo
        no se hacen validaciones de largo ni de tipo de dato, se asume
        que viene correcto desde el origen de los parametros
    '''
    def parsePerdidasLobulo(self, valor, radiales):
        self.perdidasLobulo = [0]*radiales
        if valor:
            l = str(valor).split(",")
            p = 0
            # no se valida la cantidad de elementos
            for n in l:
                self.perdidasLobulo[p] = float(n)
                p = p + 1

    '''
        En caso de un parametro faltante se asignan los por defecto
    '''    
    def revalidaParametros(self):
        if self.recomendacion == '#' or not self.recomendacion:
            self.recomendacion = self._recomendacion
            
        if self.potencia == '#' or not self.potencia:
            self.potencia = self._potencia
        
        if self.ganancia == '#' or not self.ganancia:
            self.ganancia = self._ganancia
            
        if self.alturaAntenaTransmisora == '#' or not self.alturaAntenaTransmisora:
            self.alturaAntenaTransmisora = self._alturaAntenaTransmisora
            
        if self.alturaAntenaReceptora == '#' or not self.alturaAntenaReceptora:
            self.alturaAntenaReceptora = self._alturaAntenaReceptora    
            
        if self.latitud == '#' or not self.latitud:
            self.latitud = self._latitud  
            
        if self.longitud == '#' or not self.longitud:
            self.longitud = self._longitud  
            
        if self.perdidaCablesConectores == '#' or not self.perdidaCablesConectores:
            self.perdidaCablesConectores = self._perdidaCablesConectores  
            
        if self.perdidaDivisorPotencia == '#' or not self.perdidaDivisorPotencia:
            self.perdidaDivisorPotencia = self._perdidaDivisorPotencia  
            
        if self.otrasPerdidas == '#' or not self.otrasPerdidas:
            self.otrasPerdidas = self._otrasPerdidas
                                
        if self.radiales == '#' or not self.radiales:
            self.radiales = self._radiales        
  
        if self.perdidasLobulo == '#' or not self.perdidasLobulo:
            self.perdidasLobulo = self._perdidasLobulo
            
        if self.obstaculosCircundantesTx == '#' or not self.obstaculosCircundantesTx:
            self.obstaculosCircundantesTx = self._obstaculosCircundantesTx
            
        if self.obstaculosCircundantesRx == '#' or not self.obstaculosCircundantesRx:
            self.obstaculosCircundantesRx = self._obstaculosCircundantesRx
            
        if self.toleranciaZonasSombra == '#' or not self.toleranciaZonasSombra:
            self.toleranciaZonasSombra = self._toleranciaZonasSombra

        if self.resolucionCalculo == '#' or not self.resolucionCalculo:
            self.resolucionCalculo = self._resolucionCalculo
            
        if self.porcentajeTiempo == '#' or not self.porcentajeTiempo:
            self.porcentajeTiempo = self._porcentajeTiempo
            
        if self.porcentajeUbicacion == '#' or not self.porcentajeUbicacion:
            self.porcentajeUbicacion = self._porcentajeUbicacion
            
        if self.frecuencia == '#' or not self.frecuencia:
            self.frecuencia = self._frecuencia
            
        if self.intensidadCampoReferencia == '#' or not self.intensidadCampoReferencia:
            self.intensidadCampoReferencia = self._intensidadCampoReferencia    
            
        if self.imagen == '#' or not self.imagen:
            self.imagen = self._imagen  
             
        if self.multiplo == '#' or not self.multiplo:
            self.multiplo = self._multiplo  
                        
    def imprimeParametros(self, radiales):
        arcpy.AddMessage("Recomendacion: {}".format(self.recomendacion))
        arcpy.AddMessage("Potencia: {}".format(self.potencia))
        arcpy.AddMessage("Ganancia: {}".format(self.ganancia))
        arcpy.AddMessage("Altura antena Tx: {}".format(self.alturaAntenaTransmisora))
        arcpy.AddMessage("Altura antena Rx: {}".format(self.alturaAntenaReceptora))
        arcpy.AddMessage("latitud: {}".format(self.latitud))
        arcpy.AddMessage("Longitud: {}".format(self.longitud))
        arcpy.AddMessage("Perd. Cables Conec.: {}".format(self.perdidaCablesConectores))
        arcpy.AddMessage(": {}".format(self.perdidaDivisorPotencia))
        arcpy.AddMessage(": {}".format(self.otrasPerdidas))    
        arcpy.AddMessage( self.radiales )
        t = ""
        for p in range(0,radiales):
            t+= "'{}'".format(self.perdidasLobulo[p])
        arcpy.AddMessage("Perdidas lobulo: " + t)      
        arcpy.AddMessage( self.obstaculosCircundantesTx )
        arcpy.AddMessage( self.obstaculosCircundantesRx )
        arcpy.AddMessage( self.toleranciaZonasSombra )
        arcpy.AddMessage( self.resolucionCalculo )
        arcpy.AddMessage( self.porcentajeTiempo )
        arcpy.AddMessage( self.porcentajeUbicacion )
        arcpy.AddMessage( self.frecuencia )
        arcpy.AddMessage( self.intensidadCampoReferencia )
        arcpy.AddMessage( self.multiplo )

    def resumenParametros(self):
        r = self.recomendacion + "\n"
        r+= str(self.potencia) + "\n"
        r+= str(self.ganancia) + "\n"
        r+= str(self.alturaAntenaTransmisora) + "\n"
        r+= str(self.alturaAntenaReceptora) + "\n"
        r+= str(self.latitud) + "\n"
        r+= str(self.longitud) + "\n"
        r+= str(self.perdidaCablesConectores) + "\n"
        r+= str(self.perdidaDivisorPotencia) + "\n"
        r+= str(self.otrasPerdidas) + "\n"
        r+= str(self.radiales) + "\n"
        #r+= self.perdidasLobulo + "\n"
        r+= str(self.obstaculosCircundantesTx) + "\n"
        r+= str(self.obstaculosCircundantesRx) + "\n"
        r+= str(self.toleranciaZonasSombra) + "\n"
        r+= str(self.resolucionCalculo) + "\n"
        r+= str(self.porcentajeTiempo) + "\n"
        r+= str(self.porcentajeUbicacion) + "\n"
        r+= str(self.frecuencia) + "\n"
        r+= str(self.intensidadCampoReferencia) + "\n"
        r+= str(self.multiplo) + "\n"
        return r
        
