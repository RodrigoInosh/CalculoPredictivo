# -*- coding: iso-8859-15 -*-
'''
Created on 17-02-2014

@author: CRodriguez
'''
import arcpy

srWGS84 = arcpy.SpatialReference(4326)   #GCS_WGS_84
stWebMercator = arcpy.SpatialReference(3857)  #WGS_1984_Web_Mercator_Auxiliary_Sphere

fcPunto = arcpy.GetParameter(0)

fcPunto_proj = arcpy.Project_management(fcPunto,"puntoProj",srWGS84)

for row in arcpy.da.SearchCursor(fcPunto_proj, ["SHAPE@"]):
    punto = row[0].firstPoint

arcpy.AddMessage("Coordenadas lon:{}, lat:{}".format(punto.X, punto.Y))

arcpy.SetParameter(1, punto.X)
arcpy.SetParameter(2, punto.Y)