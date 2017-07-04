# -*- encoding: utf-8 -*-
'''
Created on 15-12-2016

@author: Octavio
'''
import arcpy
import os
import datetime

def Actualiza_Texto(nombre, valor):
    for elem in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
        if elem.text == nombre:
            if type(valor) == str:
                elem.text = unicode(valor, "utf-8", errors="ignore")
            else:
                elem.text = unicode(valor)
                
Web_Map_as_JSON = arcpy.GetParameterAsText(0)
tRazonSocial = arcpy.GetParameterAsText(1)
tDomicilio = arcpy.GetParameterAsText(2)
tRegion = arcpy.GetParameterAsText(3)
tRUT = arcpy.GetParameterAsText(4)
tEMail = arcpy.GetParameterAsText(5)
tComuna = arcpy.GetParameterAsText(6)
tTelefono = arcpy.GetParameterAsText(7)
tSenalDistintiva = arcpy.GetParameterAsText(8)
tLocalidadComuna = arcpy.GetParameterAsText(9)
tFrecuencia = arcpy.GetParameterAsText(10)
tLSur1 = arcpy.GetParameterAsText(11)
tLOet1 = arcpy.GetParameterAsText(12)
tDatum = arcpy.GetParameterAsText(13)
tPotencia = arcpy.GetParameterAsText(14)
tARadiacion = arcpy.GetParameterAsText(15)
tGanancia = arcpy.GetParameterAsText(16)
tPerdida = arcpy.GetParameterAsText(17)
tOtrasPerdidas = arcpy.GetParameterAsText(18)

ahora = datetime.datetime.now()
output = 'Calculo_{}_{}_{}_{}_{}_{}.{}'.format(ahora.year,ahora.month,ahora.day, ahora.hour,ahora.minute,ahora.second, "PDF")
templateMxd = os.path.join('c:/carta/', "Carta_Vertical_1.mxd")
result = arcpy.mapping.ConvertWebMapToMapDocument(Web_Map_as_JSON, templateMxd)
mxd = result.mapDocument

Actualiza_Texto('tRazonSocial', tRazonSocial)
Actualiza_Texto('tDomicilio', tDomicilio)
Actualiza_Texto('tRegion', tRegion)
Actualiza_Texto('tRUT', tRUT)
Actualiza_Texto('tEMail', tEMail)
Actualiza_Texto('tComuna', tComuna)
Actualiza_Texto('tTelefono', tTelefono)
Actualiza_Texto('tSenalDistintiva', tSenalDistintiva)
Actualiza_Texto('tLSur1', tLSur1)
Actualiza_Texto('tLOet1', tLOet1)
Actualiza_Texto('tDatum', tDatum)
Actualiza_Texto('tPotencia', tPotencia)
Actualiza_Texto('tARadiacion', tARadiacion)
Actualiza_Texto('tGanancia', tGanancia)
Actualiza_Texto('tPerdida', tPerdida)
Actualiza_Texto('tOtrasPerdidas', tOtrasPerdidas)

Output_File = os.path.join(arcpy.env.scratchFolder, output)
arcpy.mapping.ExportToPDF(mxd, Output_File)
arcpy.AddMessage("Se entrega el resultado como parametro {}".format(Output_File))
arcpy.SetParameterAsText(19, Output_File)

filePath = mxd.filePath
del mxd, result
os.remove(filePath)
arcpy.AddMessage("***FIN***")