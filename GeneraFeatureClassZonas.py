# -*- coding: iso-8859-15 -*-
'''
Created on 22-02-2014
Modificated on 19-01-2015
@author: CRodriguez
'''
import arcpy
import TareasGeometricas

arcpy.env.overwriteOutput = True

def agregaCampos(fc,pref,radiales):
    campos = []
    #radiales = 72
    for x in range(0,radiales):
        campo = (pref + str(x * (360/radiales)))
        arcpy.AddField_management(fc,campo,"DOUBLE")
        campos.append(campo)
    return campos

tareasGeo = TareasGeometricas.TareasGeometricas()
    
fcPunto = arcpy.GetParameter(0)  # feature class de puntos
prefijo = arcpy.GetParameter(1)  # prefijo de campos, posibles: Zs, Z400_, Z200_, Z0_
multiplicador = arcpy.GetParameter(2) # multiplicador para las distancias calculadas: 1 , 1.3
radiales = int(arcpy.GetParameter(3))
srWGS84 = arcpy.SpatialReference(4326)   #GCS_WGS_84
#srWebMercator = arcpy.SpatialReference(3857)  #WGS_1984_Web_Mercator_Auxiliary_Sphere

fcPoli = arcpy.CreateFeatureclass_management("in_memory","FC"+prefijo,"POLYGON","","DISABLED","DISABLED",srWGS84)
arcpy.AddField_management(fcPoli,"IDENTIFICADOR","TEXT",0,0,30,"IDENTIFICADOR","NULLABLE","NON_REQUIRED")
arcpy.AddField_management(fcPoli,"RADIO_MAXIMO","LONG")
arcpy.AddField_management(fcPoli,"FRECUENCIA","DOUBLE")
#arcpy.AddField_management(fcPoli,"Z","TEXT",0,0,5,"Zona","NULLABLE","NON_REQUIRED")

campos = ["SHAPE@","IDENTIFICADOR","RADIO_MAXIMO","FRECUENCIA"]
# Se agregan los 18 campos de distancias
campos.extend(agregaCampos(fcPoli,prefijo,radiales))

curPunto = arcpy.da.SearchCursor(fcPunto,campos)
curPoli = arcpy.da.InsertCursor(fcPoli,campos)
#radiales = 72

for row in curPunto:
    # siempre debe venir el campo radio maximo
    radio = row[2]
    if ( radio > 0 ):
        distancias = [0]*radiales  # Se dejan todas las distancias en cero
        centro = row[0]
        radio = row[2] * multiplicador
        poli = tareasGeo.GeneraPoligono2(centro.firstPoint.X, centro.firstPoint.Y, [radio*1000], radiales)
    else:
        distancias = []
        centro = row[0]
        radios = []
        vertices = []
        for x in range(0,radiales):
            distancia = row[x+4] * multiplicador
            distancias.append(distancia)
            radios.append(distancia*1000)
        poli = tareasGeo.GeneraPoligono2(centro.firstPoint.X, centro.firstPoint.Y, radios, radiales)
        
    valores = [poli,row[1],row[2],row[3]]
    valores.extend(distancias)
    
    arcpy.AddMessage( "Identificador: {}".format( row[1].encode('utf-8') ) )
    
    tupla = tuple(valores)
    curPoli.insertRow(tupla)

del curPunto
del curPoli

ruta = arcpy.GetParameter(3)
#fcPoli_proj = arcpy.Project_management(fcPoli,"poliProj",sr)
#fcPoli_proj = arcpy.Project_management(fcPoli,ruta,sr)
#arcpy.MinimumBoundingGeometry_management("Zs_m30p","Zs_m30p_convex","CONVEX_HULL")
arcpy.AddMessage("FIN")
arcpy.SetParameter(4, fcPoli)
