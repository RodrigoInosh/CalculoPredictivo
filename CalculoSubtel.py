# -*- coding: iso-8859-15 -*-
'''
Created on 12-02-2014

@author: CRodriguez
'''
import ParametrosFormulario
import TareasGeometricas
import TablaDeValores

import CalculosZona1546
import CalculosZona1812
import CalculosZona1546mas
import CalculosZona1546menos
import CalculosZona370
import OtrosCalculos as Calculos
import arcpy

''' Inicio del proceso '''
#arcpy.env.overwriteOutput = True
params = ParametrosFormulario.ParametrosFormulario()

params.radiales = int(arcpy.GetParameter(0)) 
params.recomendacion = arcpy.GetParameter(1)
params.potencia = arcpy.GetParameter(2)
params.ganancia = arcpy.GetParameter(3)
params.alturaAntenaTransmisora = arcpy.GetParameter(4)
params.alturaAntenaReceptora = arcpy.GetParameter(5)
params.latitud = arcpy.GetParameter(6)
params.longitud = arcpy.GetParameter(7)
params.perdidaCablesConectores = arcpy.GetParameter(8)
params.perdidaDivisorPotencia = arcpy.GetParameter(9)
params.otrasPerdidas = arcpy.GetParameter(10)
params.parsePerdidasLobulo(arcpy.GetParameter(11), params.radiales)
params.obstaculosCircundantesTx = arcpy.GetParameter(12)
params.obstaculosCircundantesRx = arcpy.GetParameter(13)
params.toleranciaZonasSombra = arcpy.GetParameter(14)
params.resolucionCalculo = arcpy.GetParameter(15)
params.porcentajeTiempo = arcpy.GetParameter(16)
params.porcentajeUbicacion = arcpy.GetParameter(17)
params.frecuencia = arcpy.GetParameter(18)
params.intensidadCampoReferencia = arcpy.GetParameter(19)
params.imagen = arcpy.GetParameter(20)
params.multiplo = arcpy.GetParameter(21)

params.revalidaParametros()

''' Pasar de watts a kilowatts '''
params.potencia = float(params.potencia)/1000

tareasGeo = TareasGeometricas.TareasGeometricas()
nubePuntos = tareasGeo.GeneraNubeDePuntos(params.latitud, params.longitud, params.imagen, params.resolucionCalculo, params.radiales)
matrizCotas = tareasGeo.GeneraMatrizDeCotas(nubePuntos, params.resolucionCalculo)
#import pruebas
#matrizCotas = pruebas.Genera_Tabla_Cotas_Prueba()# tareasGeo.GeneraMatrizDeCotas(nubePuntos)
#tareasGeo.ImprimeMatrizCotas(matrizCotas)

tablaValores = TablaDeValores.TablaValores(params, matrizCotas)
x, y = tareasGeo.CentroDeNube(nubePuntos)

if(params.recomendacion == "1546-"):
    # Calculos para recomendacion 1546
    arcpy.AddMessage("Calculos para recomendacion 1546-")
    calculo1546menos = CalculosZona1546menos.CalculosZona1546menos(params, tablaValores)
    a1546 = calculo1546menos.Inicio_1546menos(params.radiales)
    # se multiplica, normalmente por 1 o por 1.3
    a1546_m = Calculos.MultiplicaLista(a1546, params.multiplo, params.radiales)
    distancias = tareasGeo.ListaAString(a1546_m)
    poli = tareasGeo.GeneraCapaPoligonos(x, y, a1546_m, params.radiales)
    #arcpy.SetParameter(25, "Calculado con recomendacion 1546" )
    
if(params.recomendacion == "1812"):
    # Calculos para recomendacion 1812
    arcpy.AddMessage("Calculos para recomendacion 1812")
    calculo1812 = CalculosZona1812.CalculosZona1812(params, tablaValores)
    a1812 = calculo1812.Inicio_1812(params.radiales)
    # se multiplica, normalmente por 1 o por 1.3
    a1812_m = Calculos.MultiplicaLista(a1812, params.multiplo, params.radiales)
    dlt = calculo1812.dlt
    distancias = tareasGeo.ListaAString(a1812_m)
    poli = tareasGeo.GeneraCapaPoligonos(x, y, a1812_m, params.radiales)
    #arcpy.SetParameter(25, "Calculado con recomendacion 1812" )

if(params.recomendacion == "1546+"):
    arcpy.AddMessage("Calculos para recomendacion 1546+")
    # Calculos para recomendacion 1546
    calculo1546menos = CalculosZona1546menos.CalculosZona1546menos(params, tablaValores)
    a1546 = calculo1546menos.Inicio_1546menos(params.radiales)
    # Calculos para recomendacion 1812
    if(params.radiales == 18):
        calculo1812 = CalculosZona1812.CalculosZona1812(params, tablaValores)
        a1812 = calculo1812.Inicio_1812(params.radiales)
        dlt = calculo1812.dlt
        # Calculos para recomendacion 1546+
        calculo1546mas = CalculosZona1546mas.CalculosZona1546mas(params, a1546, a1812, dlt)
        a1546mas = calculo1546mas.Inicio_1546mas(params.radiales)
        # se multiplica, normalmente por 1 o por 1.3
        a1546mas_m = Calculos.MultiplicaLista(a1546mas, params.multiplo, params.radiales)
        distancias = tareasGeo.ListaAString(a1546mas_m)
        poli = tareasGeo.GeneraCapaPoligonos(x, y, a1546mas_m, params.radiales)
        #arcpy.SetParameter(25, "Calculado con recomendacion 1546+" )
    else:
        calculo1546 = CalculosZona1546.CalculosZona1546(params, tablaValores)
        a1546 = calculo1546.Inicio_1546(params.radiales)
        # se multiplica, normalmente por 1 o por 1.3
        a1546_m = Calculos.MultiplicaLista(a1546, params.multiplo, params.radiales)
        distancias = tareasGeo.ListaAString(a1546_m)
        poli = tareasGeo.GeneraCapaPoligonos(x, y, a1546_m, params.radiales)
        #arcpy.SetParameter(25, "Calculado con recomendacion 1546-" )

if(params.recomendacion == "1546"):
    # Calculos para recomendacion 1546 TVD
    arcpy.AddMessage("Calculos para recomendacion 1546")
    calculo1546 = CalculosZona1546.CalculosZona1546(params, tablaValores)
    a1546 = calculo1546.Inicio_1546(params.radiales)
    # se multiplica, normalmente por 1 o por 1.3
    a1546_m = Calculos.MultiplicaLista(a1546, params.multiplo, params.radiales)
    distancias = tareasGeo.ListaAString(a1546_m)
    poli = tareasGeo.GeneraCapaPoligonos(x, y, a1546_m, params.radiales)
    #arcpy.SetParameter(25, "Calculado con recomendacion 1546-" )
    
if(params.recomendacion == "370"):
    arcpy.AddMessage("Calculos para recomendacion 370")
    calculo370 = CalculosZona370.CalculosZona370(params, tablaValores)
    a370 = calculo370.Inicio_370(params.radiales)
    # se multiplica, normalmente por 1 o por 1.3
    a370_m = Calculos.MultiplicaLista(a370, params.multiplo, params.radiales)
    distancias = tareasGeo.ListaAString(a370)
    poli = tareasGeo.GeneraCapaPoligonos(x, y, a370, params.radiales)
    #arcpy.SetParameter(24, "Calculado con recomendacion 370" )

arcpy.AddMessage(params.latitud)
arcpy.AddMessage(params.latitud)
arcpy.AddMessage(distancias)
#BORRARarcpy.AddMessage(stop)#BORRAR  
arcpy.SetParameter(22, poli)
arcpy.SetParameter(23, nubePuntos)
arcpy.SetParameter(24, distancias)
#arcpy.SetParameter(25, params.resumenParametros() )
