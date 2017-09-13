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
import os
import arcpy

''' Inicio del proceso '''
#arcpy.env.overwriteOutput = True
params = ParametrosFormulario.ParametrosFormulario()

params.radiales = int(arcpy.GetParameter(0))
params.potencia = arcpy.GetParameter(1)
params.latitud = arcpy.GetParameter(2)
params.longitud = arcpy.GetParameter(3)
#DEBEN SER RESOLICION = 250#
params.resolucionCalculo = arcpy.GetParameter(4)
sde_connection_file = arcpy.GetParameter(5)
arcpy.AddMessage(sde_connection_file)
params.revalidaParametros()

arcpy.env.workspace = sde_connection_file
''' Pasar de watts a kilowatts '''
params.potencia = float(params.potencia)/1000
tareasGeo = TareasGeometricas.TareasGeometricas()
nubePuntos = tareasGeo.GeneraNubeDePuntos(params.latitud, params.longitud, params.imagen, params.resolucionCalculo, params.radiales)
shp = ('Nube_{}_{}.shp'.format(3,2))
#salida = os.path.join(arcpy.env.scratchFolder, shp)
salida = os.path.join("c:\env", shp)
arcpy.AddMessage('Se genera {}'.format(salida))
arcpy.CopyFeatures_management(nubePuntos, salida)
# matrizCotas = tareasGeo.GeneraMatrizDeCotas(nubePuntos, params.resolucionCalculo)
# arcpy.AddMessage(matrizCotas)
# var = str(matrizCotas)
# arcpy.AddMessage(var)
arcpy.SetParameter(6, salida)