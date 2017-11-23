# -*- coding: utf-8 -*-
'''
Created on 14-02-2014
Modificated on 26-01-2015

@author: CRodriguez
'''
import arcpy
#import math
#import csv
import os

class TareasGeometricas(): 
    srWGS84 = arcpy.SpatialReference(4326)   #GCS_WGS_84
    srWebMercator = arcpy.SpatialReference(3857)  #WGS_1984_Web_Mercator_Auxiliary_Sphere
    poligono_servicio = ""
    
    # EPSG 3854 = wkid 102100
    # EPSG 3854 para esri
    # wkid 102100 para google earth
    
    def __init__(self): 
        arcpy.env.overwriteOutput = True

    ''' 
    **************************************************************************************************************
     MODIFICACION INICIO 26 enero 2015
    **************************************************************************************************************
    ''' 
    def GeneraNubeDePuntos(self, latitud, longitud, imagen, resolucionCalculo, radiales):
        
        # se crea una tabla para contener valores y ser utilizada por la siguiente herramienta
        tb = arcpy.CreateTable_management("in_memory", "tabla")
        arcpy.AddField_management(tb,"x","DOUBLE")
        arcpy.AddField_management(tb,"y","DOUBLE")
        arcpy.AddField_management(tb,"a","LONG")
        arcpy.AddField_management(tb,"d","LONG")
        cursor = arcpy.da.InsertCursor(tb, ["x","y","a","d"])
        #radiales1 = int(radiales)
        #radiales = self.params.radiales
        #for d in range(0,201):
        # Se omite el punto centrar, provoca errores en BearingDistanceToLine
            
        for d in range(1,201):   
            for a in range(0,radiales):
                ang = a * (360 / radiales)
                dist = d*resolucionCalculo
                cursor.insertRow((longitud,latitud,ang,dist,))
        del cursor
        arcpy.AddMessage("Se creo tabla temporal para calculo de ubicacion de puntos")
        
        tabla = os.path.join(arcpy.env.scratchGDB, 'tabla_distancias1')
        ra = arcpy.BearingDistanceToLine_management(tb,tabla,"x","y","d","METERS","a","DEGREES","GEODESIC","",self.srWGS84)
        arcpy.AddMessage("Se calculan distancias")
        
        # fcNube = arcpy.CreateFeatureclass_management("c:\env", "punto", "POINT", "", "DISABLED", "DISABLED",self.srWGS84, "")
        fcNube = arcpy.CreateFeatureclass_management("in_memory","punto","POINT","","DISABLED","ENABLED",self.srWGS84)
        arcpy.AddField_management(fcNube,"angulo","LONG")
        arcpy.AddField_management(fcNube,"distancia","LONG")
        arcpy.AddMessage("Se creo feature class para los puntos")
    
        inCur = arcpy.da.InsertCursor(fcNube, ["SHAPE@","angulo","distancia"])
        seCur = arcpy.da.SearchCursor(ra, ["SHAPE@","a","d"])
        
        # se agrega el punto central
        p = arcpy.Point(longitud,latitud)
        arcpy.AddMessage(p)
        #print "Se genera punto central"
        #print p
        for a in range(0,radiales):
            angulo = a * (360 / radiales)
            inCur.insertRow((p,angulo,0,))
        # se gregan el resto de los puntos
        for row in seCur:
            p = row[0].lastPoint   # Solo se recupera el punto final de la linea
            inCur.insertRow((p,row[1],row[2],))
        
        arcpy.AddMessage("Se genero la nube de puntos")
        arcpy.AddMessage("Advertencia: Se obtendran las alturas para los puntos. Este proceso puede demorar un poco.")
        
        for a in range(0,radiales):
            arcpy.AddMessage("    Obteniendo alturas para puntos {:.2%}".format(float(a)/radiales))
            lyr = arcpy.MakeFeatureLayer_management(fcNube,"lyr")
            angulo = a * (360 / radiales)
            arcpy.SelectLayerByAttribute_management(lyr,"NEW_SELECTION","angulo={}".format(angulo))
            arcpy.AddSurfaceInformation_3d(lyr,imagen,"Z","BILINEAR")

        arcpy.AddMessage("Se obtuvieron las alturas para los puntos")

        del inCur
        del seCur

        return fcNube

    def CapaCensal(self, x, y, poligono, capa_censal):
        arcpy.AddMessage("---Capa censal---")

        suma_censal = 0
        intersectOutput = arcpy.CreateFeatureclass_management("in_memory", "FC", "POLYGON")
        arcpy.env.outputZFlag = "Disabled"
        arcpy.env.outputMFlag = "Disabled"
        inFeatures = [poligono, capa_censal]
        arcpy.Intersect_analysis(inFeatures, intersectOutput, "ALL")
        cursor = arcpy.SearchCursor(intersectOutput)
        count_rows = 0

        for row in cursor:
            suma_censal += float(row.getValue("TOT_VIV"))
            count_rows+=1

        return suma_censal
    
    # Input: posicion central(longitud,latitud), lista de distancias
    # Output: poligono
    def GeneraPoligono2(self, longitud, latitud, distancias, radiales):
        # se crea una tabla para contener valores y ser utilizada por la siguiente herramienta
        tb = arcpy.CreateTable_management("in_memory", "tabla")
        arcpy.AddField_management(tb,"x","DOUBLE")
        arcpy.AddField_management(tb,"y","DOUBLE")
        arcpy.AddField_management(tb,"a","LONG")
        arcpy.AddField_management(tb,"d","LONG")
        cursor = arcpy.da.InsertCursor(tb, ["x","y","a","d"])
        #radiales1 = int(radiales)
        #radiales = self.params.radiales
        # Se omite el punto centrar, provoca errores en BearingDistanceToLine
        if len(distancias) == 1: # si hay solo un valor se asume que es el radio
            for a in range(0,360):
                cursor.insertRow((longitud,latitud,a,distancias[0],))
        else:  
            for a in range(0,radiales):
                cursor.insertRow((longitud,latitud,a*(360/radiales),distancias[a],))
        del cursor
        arcpy.AddMessage("Se creo tabla temporal para calculo de ubicacion de puntos")
        
        tabla = os.path.join(arcpy.env.scratchGDB, 'tabla_distancias2')
        ra = arcpy.BearingDistanceToLine_management(tb,tabla,"x","y","d","METERS","a","DEGREES","GEODESIC","",self.srWGS84)
        arcpy.AddMessage("Se calculan distancias")
        
        vertices = []
        cursor = arcpy.da.SearchCursor(ra, ["SHAPE@","a","d"])
        for row in cursor:
            v = row[0].lastPoint   # Solo se recupera el punto final de la linea
            vertices.append(v)
        del cursor
        
        poligono = arcpy.Polygon(arcpy.Array(vertices))
        return poligono
    
    # Input: centro(longitud,latitud) y lista de distancias
    # Output: Capa con dos poligonos
    def GeneraCapaPoligonos(self, x, y, distancias, radiales):
        fcPoli = arcpy.CreateFeatureclass_management("in_memory","area","POLYGON","","DISABLED","DISABLED",self.srWGS84)
        arcpy.AddField_management(fcPoli, 'area', 'DOUBLE')
        cursor = arcpy.da.InsertCursor(fcPoli,["SHAPE@"])
        #radiales = self.params.radiales
        poli = self.GeneraPoligono2(x, y, [distancias[r]*1000 for r in range(0,radiales)], radiales)    
        poli2 = self.GeneraPoligono2(x, y, [distancias[r]*1300 for r in range(0,radiales)], radiales)

        cursor.insertRow(tuple([poli]))
        cursor.insertRow(tuple([poli2]))
        del cursor
        
        arcpy.CalculateField_management(fcPoli,'area','!shape.area@squarekilometers!','PYTHON')

        return fcPoli
    '''
    **************************************************************************************************************
     MODIFICACION FIN 26 enero 2015
    **************************************************************************************************************
    '''

    def GeneraPoligonoInterseccion(self, x, y, distancias, radiales):
        poligonoZonaServicio = arcpy.CreateFeatureclass_management("in_memory","area","POLYGON","","DISABLED","DISABLED",self.srWGS84)
        arcpy.AddField_management(poligonoZonaServicio, 'area', 'DOUBLE')
        cursor = arcpy.da.InsertCursor(poligonoZonaServicio,["SHAPE@"])
        poli = self.GeneraPoligono2(x, y, [distancias[r]*1000 for r in range(0,radiales)], radiales)

        cursor.insertRow(tuple([poli]))
        del cursor
        
        arcpy.CalculateField_management(poligonoZonaServicio,'area','!shape.area@squarekilometers!','PYTHON')

        return poligonoZonaServicio

    def GeneraMatrizDeCotas(self, fcNube, resolucionCalculo):
        arcpy.AddMessage("Generando Matriz de Cotas");
        tabla = []
        for d in range(0,201):
            reg = []
            w = "distancia=" + str(d*resolucionCalculo)
            cursor = arcpy.da.SearchCursor(fcNube, ["angulo", "distancia", "Z"],w,"","",("None","ORDER BY angulo")) 
            for row in cursor: 
                # arcpy.AddMessage("angulo: {}".format(row[0]))
                # arcpy.AddMessage("distancia: {}".format(row[1]))
                # arcpy.AddMessage("Z: {}".format(row[2]))
                # se controla en caso de que no se pueda recuperar cota desde imagen
                try:
                    z = round(row[2],3)
                except:
                    reg.append(0)
                    #arcpy.AddMessage("SE DIO UN ERROR PARA EL VALOR:{}, ANGULO:{}, DISTANCIA:{}".format( row[2], row[0], row[1] ))
                else:
                    reg.append(z)
                    #arcpy.AddMessage("angulo:{}, distancia:{}, altura:{}".format(row[0], row[1], row[2]) )
            tabla.append(reg)    
        return tabla
    
    def ImprimeMatrizCotas(self, m):
        for d in range(0,201):
            #for r in range(0,18):
            reg = m[d]
            #arcpy.AddMessage("d:{}, r:{}, v:{}".format(d, r, v) ) 
            arcpy.AddMessage(reg)
    
    def CentroDeNube(self, fcNube):
        cursor = arcpy.da.SearchCursor(fcNube, ["SHAPE@X","SHAPE@Y"], "distancia=0 and angulo=0") 
        for row in cursor:
            x = row[0]
            y = row[1]
        return [x,y]
    
    '''
    def generaCSV(self, m):
        tablaCSV = r"d:\matrizcotas.csv"
        writer = csv.writer(open(tablaCSV, "wb"), delimiter=",")
        for d in range(0,201):
            writer.writerow(m[d]) 
        del writer
    '''   
    def ListaAString(self, lista):
        t = ""
        for v in lista:
            t = t + str(v) + ","
        return t
      
      
    #def __CreaPunto(self, punto, angulo, distancia):
    #    p = arcpy.Point(0.0,0.0)
    #    p.X += punto.X + (distancia * math.cos(angulo * math.pi / 180.0))
    #    p.Y += punto.Y + (distancia * math.sin(angulo * math.pi / 180.0))
    #    return p
            
    #def ___GeneraNubeDePuntos(self, latitud, longitud, imagen, resolucionCalculo):
    #    fcPunto = arcpy.CreateFeatureclass_management("in_memory","punto","POINT","","DISABLED","ENABLED",self.srWGS84)
    #    cursor = arcpy.da.InsertCursor(fcPunto, ["SHAPE@"])
    #    #da.InsertCursor(fcPunto, ["SHAPE@"])
    #    p = arcpy.Point(longitud, latitud)
    #    cursor.insertRow((p,))
        #arcpy.AddMessage("Se agrego punto")
    #    arcpy.AddMessage("Coordenadas: lat:{}, lon:{}".format(p.Y, p.X))
    #    
    #    #arcpy.env.overwriteOutput = True
    #    pProy = arcpy.env.scratchGDB + "\\puntoProj"
        #pProy = arcpy.env.scratchFolder + "\\puntoProj.shp"
    #    fcPunto_proj = arcpy.Project_management(fcPunto, pProy, self.srWebMercator)
        #fcPunto_proj = arcpy.Project_management(fcPunto,"puntoProj",self.srWebMercator)
        #arcpy.AddMessage("Se proyecto a Web Mercator")
    #    for row in arcpy.da.SearchCursor(fcPunto_proj, ["SHAPE@"]):
    #        punto = row[0].firstPoint
    #    arcpy.AddMessage("Nuevas coordenadas: x:{}, y:{}".format(punto.X, punto.Y))
    #    
    #    fcNube = arcpy.CreateFeatureclass_management("in_memory","nube","POINT","","DISABLED","ENABLED",self.srWebMercator)
    #    arcpy.AddField_management(fcNube,"angulo","LONG")
    #    arcpy.AddField_management(fcNube,"distancia","LONG")
    #    cursor = arcpy.da.InsertCursor(fcNube,["SHAPE@","angulo","distancia"])
        #arcpy.AddMessage("Se creo feature para nube de puntos")
    #    
    #    ajuste = 90   #ajuste para el valor del angulo
    #    for d in range(0,201):
    #        for a in range(0,18):
    #            angulo = a*20
    #            p = self.__CreaPunto(punto, ajuste-angulo, d*resolucionCalculo)
    #            cursor.insertRow((p,angulo,d*resolucionCalculo,))
    #    arcpy.AddMessage("Se genero la nube de puntos")
    #    arcpy.AddMessage("Advertencia: Se obtendran las alturas para los puntos. Este proceso puede demorar un poco.")
    #    
    #    for a in range(0,18):
    #        arcpy.AddMessage("    Obteniendo alturas para puntos {:.2%}".format(float(a)/18))
    #        lyr = arcpy.MakeFeatureLayer_management(fcNube,"lyr")
    #        angulo = a*20
    #        arcpy.SelectLayerByAttribute_management(lyr,"NEW_SELECTION","angulo={}".format(angulo))
    #        arcpy.AddSurfaceInformation_3d(lyr,imagen,"Z","BILINEAR")
        #arcpy.SelectLayerByLocation_management(fcNube, "CLEAR_SELECTION")
        #arcpy.AddSurfaceInformation_3d(fcNube,imagen,"Z","BILINEAR")
    #    arcpy.AddMessage("Se obtuvieron las alturas para los puntos")
    #    return fcNube  