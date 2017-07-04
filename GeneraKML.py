# -*- coding: iso-8859-15 -*-
'''
Created on 22-02-2017
@author: kcortes ESTA ES UNA PRUEBA
'''
import math
import arcpy
#import TareasGeometricas
import ParametrosFormulario
import OtrosCalculos as Calculos

import os
from lxml import etree

arcpy.env.overwriteOutput = True

class GeneraKML():
    params = 0
    tablaCotas = []
    tablaCotas_him = []
    tablaCotas_DistanciasKM = []
    #tablaCotas_ADT = []
    tablaCotas_ADT_Maximos = []
    tablaCotas_Valores = []
    
    def __init__(self, params, tabla_cotas):
        self.params = params
        self.tablaCotas = tabla_cotas
        self.Calcula_ListaDistanciasKM()
        self.Calcula_him(params.radiales)
        self.Calcula_ADT(params.radiales)
        self.Calcula_Valores(params.radiales)
        
    def calculaGrados(valor):
        t = str(int(valor))
        l = len(t)
        return float(t[0:l-4]) + (float(t[l-4:l-2])/60) + (float(t[l-2:l])/3600)

    def VerticesPoligono(fc,pref,radiales):
        Pi = 3.14159265358979
        #campos = []
        ##radiales = 72
        LatDeg = -calculaGrados(Lat)
        LongDeg = -calculaGrados(Long)
        LatRad = LatDeg * Pi/180
        LongRad = LongDeg * Pi/180
        Huso = LongDeg//6 + 31
        HusoMer = 6 * Huso - 183
        Dlambda = LongRad - ((HusoMer * Pi)/180)
        A = math.cos(LatRad) * math.sin(Dlambda)
        Xi = (1/2) * math.log((1+A)/(1-A)) #logaritmo natural
        Eta = math.atan((math.tan(LatRad))/math.cos(Dlambda)) - LatRad
        ejemayor = 6378137
        ejemenor = 6356752.31424518
        e2 = (math.raiz(ejemayor**2 - ejemenor**2)/ejemenor)**2
        rpolar = (ejemayor**2)/ejemenor
        Ni = (rpolar/(1 + e2*(math.cos(LatRad))**2)**(1/2))*0.9996
        Zeta = (e2/2) * Xi**2 *(math.cos(LatRad))**2
        A1 = math.sin(2*LatRad)
        A2 = A1 * (math.cos(LatRad))**2
        J2 = LatRad + (A1/2)
        J4 = ((3*J2) + A2)/4
        J6 = ((5*J4 + A2*math.cos(LatRad))**2)/3
        Alfa = (3/4) * e2
        Beta = (5/3) * Alfa**2
        Gamma = (35/27) * Alfa**3
        Bfi = 0.9996 * rpolar * (LatRad-(Alfa*J2) + (Beta*J4) - (Gamma*J6))
        UTMxEste
        UTMyNorte
        
        #for para crear y construir array lat,long de cada vertice y luego para generar cadena de caracteres texto + lat[i]+","+long[i]+",0"
        
        #for x in range(0,radiales):
        #    campo = (pref + str(x * (360/radiales)))
        #    arcpy.AddField_management(fc,campo,"DOUBLE")
        #    campos.append(campo)
        #    return campos

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
