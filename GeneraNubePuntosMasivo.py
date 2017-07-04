# -*- coding: iso-8859-15 -*-
'''
Created on 08/03/2014

@author: cristian
'''
import os
import arcpy
import TareasGeometricas

def calculaGrados(valor):
    t = str(int(valor))
    l = len(t)
    return float(t[0:l-4]) + (float(t[l-4:l-2])/60) + (float(t[l-2:l])/3600)

arcpy.env.overwriteOutput = True

tabla = arcpy.GetParameter(0)
imagen = arcpy.GetParameter(1)
carpeta = arcpy.GetParameterAsText(2)
resolucionCalculo = arcpy.GetParameter(3)
if resolucionCalculo == '#' or not resolucionCalculo:
    resolucionCalculo = 500
radiales = int(arcpy.GetParameter(4))
if radiales == '#' or not radiales:
    radiales = 72 
#arcpy.AddMessage("Carpeta: " + carpeta )

# Se crea un dicionario con los nombres de los campos y sus posiciones dentro de la tabla
dict = {}
campos = []
pos = 0
for f in arcpy.ListFields(tabla):
    dict[f.name] = pos
    campos.append(f.name)
    pos = pos + 1

tareasGeo = TareasGeometricas.TareasGeometricas()

cursor = arcpy.da.SearchCursor(tabla, campos)
for row in cursor:
    nubePuntos = tareasGeo.GeneraNubeDePuntos(-calculaGrados(row[dict['LAT_PTX']]), \
                                              -calculaGrados(row[dict['LONG_PTX']]), imagen, resolucionCalculo, radiales)
    #shp = ('Nube_{}.shp'.format( row[dict['identificador']] )).replace('-', '_')
    shp = ('Nube_{}_{}.shp'.format(int(row[dict['LAT_PTX']]), int(row[dict['LONG_PTX']])))
    #salida = os.path.join(arcpy.env.scratchFolder, shp)
    salida = os.path.join(carpeta, shp)
    arcpy.AddMessage('Se genera {}'.format(salida))
    
    arcpy.CopyFeatures_management(nubePuntos, salida)
    
arcpy.AddMessage("FIN")

