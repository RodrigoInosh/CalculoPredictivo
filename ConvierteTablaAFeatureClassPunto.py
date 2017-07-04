'''
Created on 21-02-2014

@author: CRodriguez
'''
import arcpy
arcpy.env.overwriteOutput = True

def agregarCamposDeTabla(tabla,fc):
    nombres = []
    for f in arcpy.ListFields(tabla):
        # se deberian excluir los campos de latitud y longitud, son redundantes
        arcpy.AddField_management(fc,f.name,f.type)
        nombres.append(f.name)
    return nombres

def calculaGrados(valor):
    t = str(int(valor))
    l = len(t)
    return float(t[0:l-4]) + (float(t[l-4:l-2])/60) + (float(t[l-2:l])/3600)

def generaPunto(lat,lon):
    return arcpy.Point(-calculaGrados(lon),-calculaGrados(lat))
    
def posicionCampoCoordenadas(lista):
    pLat = -1
    pLon = -1
    for p in range(0,len(lista)):
        if lista[p] == "LAT_PTX":
            pLat = p
        if lista[p] == "LONG_PTX":
            pLon = p
    return [pLat,pLon]
        
tabla = arcpy.GetParameter(0)
sr = arcpy.SpatialReference(4326)   #GCS_WGS_84

arcpy.AddMessage("Creando feature class")
fcPunto = arcpy.CreateFeatureclass_management("in_memory","puntos","POINT","","DISABLED","DISABLED",sr)

listaCamposTabla = agregarCamposDeTabla(tabla,fcPunto)
listaCamposFC = ["SHAPE@"]
listaCamposFC.extend(listaCamposTabla)

curFC = arcpy.da.InsertCursor(fcPunto,listaCamposFC)
curTabla = arcpy.da.SearchCursor(tabla,listaCamposTabla)

arcpy.AddMessage("Copiando datos")
pLat,pLon = posicionCampoCoordenadas(listaCamposTabla)

for row in curTabla:
    punto = generaPunto(row[pLat],row[pLon])
    valores = [punto]
    for x in range(0,len(listaCamposTabla)):
        valores.append(row[x])
    tupla = tuple(valores)
    curFC.insertRow(tupla)

arcpy.AddMessage("FIN")
arcpy.SetParameter(1, fcPunto)
