# -*- encoding: utf-8 -*-
'''
Created on 27-02-2014

@author: CRodriguez
'''
import arcpy
import os
#import uuid
import datetime

def Actualiza_Texto(nombre, valor):
    elementos = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")
    for elem in elementos:
        if elem.name == nombre:
            if type(valor) == str:
                elem.text = unicode(valor, "utf-8", errors="ignore")
            else:
                elem.text = unicode(valor)

def Texto_A_Matriz(texto, radiales):
    matriz = []
    if texto:
        l = str(texto).split(",")
        p = 0
        for n in l:
            if p < radiales:
                matriz.append(n)
            p = p + 1
    return matriz
                            
Web_Map_as_JSON = arcpy.GetParameterAsText(0) #{"paramName":"Web_Map_as_JSON","dataType":"GPString","value":{"layoutOptions":{"titleText":"Simple WebMap JSON example"},"operationalLayers":[{"url":"http://maps1.arcgisonline.com/ArcGIS/rest/services/USA_Federal_Lands/MapServer","visibility":true}],"exportOptions":{"outputSize":[1500,1500]},"mapOptions":{"extent":{"xmin":-13077000,"ymin":4031000,"xmax":-13023000,"ymax":4053000}},"version":"1.4"}}

Format = arcpy.GetParameterAsText(2)
if Format == '#' or not Format:
    Format = "PDF" 

Layout_Template = arcpy.GetParameterAsText(3) #AQUI PARECE QUE HABRIA QUE CREAR UN LAYOUT_TEMPLATE PARA 8, 18 y 72 Y CAMBIAR NÚMERO DE GETPARAMETER
if Layout_Template == '#' or not Layout_Template:
    Layout_Template = "Carta Vertical" 

''' Se cargan los valores para el formulario '''
pRazonSocial = arcpy.GetParameterAsText(4)
if pRazonSocial == '#' or not pRazonSocial:
    pRazonSocial = "-"

pRut = arcpy.GetParameterAsText(5)
if pRut == '#' or not pRut:
    pRut = "-"
    
pLocalidad = arcpy.GetParameterAsText(6)
if pLocalidad == '#' or not pLocalidad:
    pLocalidad = "-"
    
pPotencia = arcpy.GetParameterAsText(7)
if pPotencia == '#' or not pPotencia:
    pPotencia = "-"
    
pFrecuencia = arcpy.GetParameterAsText(8)
if pFrecuencia == '#' or not pFrecuencia:
    pFrecuencia = "-"

pIntensidadCampo = arcpy.GetParameterAsText(9)
if pIntensidadCampo == '#' or not pIntensidadCampo:
    pIntensidadCampo = "-"

pAlturaAntenaTx = arcpy.GetParameterAsText(10)
if pAlturaAntenaTx == '#' or not pAlturaAntenaTx:
    pAlturaAntenaTx = "-"
    
pGanancia = arcpy.GetParameterAsText(11)
if pGanancia == '#' or not pGanancia:
    pGanancia = "-"
    
pDivisorPotencia = arcpy.GetParameterAsText(12)
if pDivisorPotencia == '#' or not pDivisorPotencia:
    pDivisorPotencia = "-"    
    
pPerdidaCablesConectores = arcpy.GetParameterAsText(13)
if pPerdidaCablesConectores == '#' or not pPerdidaCablesConectores:
    pPerdidaCablesConectores = "-"   
    
pOtrasPerdidas = arcpy.GetParameterAsText(14)
if pOtrasPerdidas == '#' or not pOtrasPerdidas:
    pOtrasPerdidas = "-"
    
pRadiales = int(arcpy.GetParameter(15)) #DESDE AQUI AGREGO NUEVO PARAMETRO DE ENTRADA PARA OCUPAR NUMERO DE RADIALES
if pRadiales == '#' or not pRadiales:
    pRadiales = "-"   
    
pLatitud = arcpy.GetParameterAsText(16)
if pLatitud == '#' or not pLatitud:
    pLatitud = "-"   
    
pLongitud = arcpy.GetParameterAsText(17)
if pLongitud == '#' or not pLongitud:
    pLongitud = "-"

if pRadiales == 8: 
    pLobulos = arcpy.GetParameterAsText(18)
        if pLobulos == '#' or not pLobulos:
            pLobulos = "0,0,0,0,0,0,0,0"
            #arcpy.AddMessage("lob:" + pLobulos)
    pDistancias = arcpy.GetParameterAsText(19)
        if pDistancias == '#' or not pDistancias:
            pDistancias = "0,0,0,0,0,0,0,0"
             
else if pRadiales == 18: 
    pLobulos = arcpy.GetParameterAsText(18)
        if pLobulos == '#' or not pLobulos:
            pLobulos = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
            #arcpy.AddMessage("lob:" + pLobulos)
    pDistancias = arcpy.GetParameterAsText(19)
        if pDistancias == '#' or not pDistancias:
            pDistancias = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
            
else if pRadiales == 72: 
    pLobulos = arcpy.GetParameterAsText(18)
        if pLobulos == '#' or not pLobulos:
            pLobulos = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
            #arcpy.AddMessage("lob:" + pLobulos)
    pDistancias = arcpy.GetParameterAsText(19)
        if pDistancias == '#' or not pDistancias:
            pDistancias = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"  

arcpy.AddMessage("Se leyeron los parametros")

''' Fin de la carga de valores para formulario '''    

''' Se genera el documento de mapa (mxd) de salida '''
templatePath = 'c:/arcgisserver/layoutsSUBTEL/'
arcpy.AddMessage("templatePath:" + templatePath + Layout_Template + '.mxd')
    
templateMxd = os.path.join(templatePath, Layout_Template + '.mxd')
result = arcpy.mapping.ConvertWebMapToMapDocument(Web_Map_as_JSON, templateMxd)
mxd = result.mapDocument

''' Se actualizan los valores de textos del mxd '''
Actualiza_Texto('tRazonSocial', pRazonSocial)
Actualiza_Texto('tRut', pRut)
Actualiza_Texto('tLocalidad', pLocalidad)
Actualiza_Texto('tPotencia', pPotencia)
Actualiza_Texto('tFrecuencia', pFrecuencia)
Actualiza_Texto('tIntensidadCampo', pIntensidadCampo)
Actualiza_Texto('tAlturaAntenaTx', pAlturaAntenaTx)
Actualiza_Texto('tGanancia', pGanancia)
Actualiza_Texto('tDivisorPotencia', pDivisorPotencia)
Actualiza_Texto('tPerdidaCablesConectores', pPerdidaCablesConectores)
Actualiza_Texto('tOtrasPerdidas', pOtrasPerdidas)
Actualiza_Texto('tLatitud', pLatitud)
Actualiza_Texto('tLongitud', pLongitud)

if pRadiales == 8: 
                
    lobulos = Texto_A_Matriz(pLobulos, pRadiales)
    Actualiza_Texto('pLob0', lobulos[0])
    Actualiza_Texto('pLob45', lobulos[1])
    Actualiza_Texto('pLob90', lobulos[2])
    Actualiza_Texto('pLob135', lobulos[3])
    Actualiza_Texto('pLob180', lobulos[4])
    Actualiza_Texto('pLob225', lobulos[5])
    Actualiza_Texto('pLob270', lobulos[6])
    Actualiza_Texto('pLob315', lobulos[7])
    distancias = Texto_A_Matriz(pDistancias, pRadiales)
    Actualiza_Texto('pDist0', distancias[0])
    Actualiza_Texto('pDist45', distancias[1])
    Actualiza_Texto('pDist90', distancias[2])
    Actualiza_Texto('pDist135', distancias[3])
    Actualiza_Texto('pDist180', distancias[4])
    Actualiza_Texto('pDist225', distancias[5])
    Actualiza_Texto('pDist270', distancias[6])
    Actualiza_Texto('pDist315', distancias[7])

else if pRadiales == 18: 

    lobulos = Texto_A_Matriz(pLobulos, pRadiales)
    Actualiza_Texto('pLob0', lobulos[0])
    Actualiza_Texto('pLob20', lobulos[1])
    Actualiza_Texto('pLob40', lobulos[2])
    Actualiza_Texto('pLob60', lobulos[3])
    Actualiza_Texto('pLob80', lobulos[4])
    Actualiza_Texto('pLob100', lobulos[5])
    Actualiza_Texto('pLob120', lobulos[6])
    Actualiza_Texto('pLob140', lobulos[7])
    Actualiza_Texto('pLob160', lobulos[8])
    Actualiza_Texto('pLob180', lobulos[9])
    Actualiza_Texto('pLob200', lobulos[10])
    Actualiza_Texto('pLob220', lobulos[11])
    Actualiza_Texto('pLob240', lobulos[12])
    Actualiza_Texto('pLob260', lobulos[13])
    Actualiza_Texto('pLob280', lobulos[14])
    Actualiza_Texto('pLob300', lobulos[15])
    Actualiza_Texto('pLob320', lobulos[16])
    Actualiza_Texto('pLob340', lobulos[17])
    distancias = Texto_A_Matriz(pDistancias, pRadiales)
    Actualiza_Texto('pDist0', distancias[0])
    Actualiza_Texto('pDist20', distancias[1])
    Actualiza_Texto('pDist40', distancias[2])
    Actualiza_Texto('pDist60', distancias[3])
    Actualiza_Texto('pDist80', distancias[4])
    Actualiza_Texto('pDist100', distancias[5])
    Actualiza_Texto('pDist120', distancias[6])
    Actualiza_Texto('pDist140', distancias[7])
    Actualiza_Texto('pDist160', distancias[8])
    Actualiza_Texto('pDist180', distancias[9])
    Actualiza_Texto('pDist200', distancias[10])
    Actualiza_Texto('pDist220', distancias[11])
    Actualiza_Texto('pDist240', distancias[12])
    Actualiza_Texto('pDist260', distancias[13])
    Actualiza_Texto('pDist280', distancias[14])
    Actualiza_Texto('pDist300', distancias[15])
    Actualiza_Texto('pDist320', distancias[16])
    Actualiza_Texto('pDist340', distancias[17])

else if pRadiales == 72: 

    lobulos = Texto_A_Matriz(pLobulos, pRadiales)
    Actualiza_Texto('pLob0', lobulos[0])
    Actualiza_Texto('pLob5', lobulos[1])
    Actualiza_Texto('pLob10', lobulos[2])
    Actualiza_Texto('pLob15', lobulos[3])
    Actualiza_Texto('pLob20', lobulos[4])
    Actualiza_Texto('pLob25', lobulos[5])
    Actualiza_Texto('pLob30', lobulos[6])
    Actualiza_Texto('pLob35', lobulos[7])
    Actualiza_Texto('pLob40', lobulos[8])
    Actualiza_Texto('pLob45', lobulos[9])
    Actualiza_Texto('pLob50', lobulos[10])
    Actualiza_Texto('pLob55', lobulos[11])
    Actualiza_Texto('pLob60', lobulos[12])
    Actualiza_Texto('pLob65', lobulos[13])
    Actualiza_Texto('pLob70', lobulos[14])
    Actualiza_Texto('pLob75', lobulos[15])
    Actualiza_Texto('pLob80', lobulos[16])
    Actualiza_Texto('pLob85', lobulos[17])
    Actualiza_Texto('pLob90', lobulos[18])
    Actualiza_Texto('pLob95', lobulos[19])
    Actualiza_Texto('pLob100', lobulos[20])
    Actualiza_Texto('pLob105', lobulos[21])
    Actualiza_Texto('pLob110', lobulos[22])
    Actualiza_Texto('pLob115', lobulos[23])
    Actualiza_Texto('pLob120', lobulos[24])
    Actualiza_Texto('pLob125', lobulos[25])
    Actualiza_Texto('pLob130', lobulos[26])
    Actualiza_Texto('pLob135', lobulos[27])
    Actualiza_Texto('pLob140', lobulos[28])
    Actualiza_Texto('pLob145', lobulos[29])
    Actualiza_Texto('pLob150', lobulos[30])
    Actualiza_Texto('pLob155', lobulos[31])
    Actualiza_Texto('pLob160', lobulos[32])
    Actualiza_Texto('pLob165', lobulos[33])
    Actualiza_Texto('pLob170', lobulos[34])
    Actualiza_Texto('pLob175', lobulos[35])
    Actualiza_Texto('pLob180', lobulos[36])
    Actualiza_Texto('pLob185', lobulos[37])
    Actualiza_Texto('pLob190', lobulos[38])
    Actualiza_Texto('pLob195', lobulos[39])
    Actualiza_Texto('pLob200', lobulos[40])
    Actualiza_Texto('pLob205', lobulos[41])
    Actualiza_Texto('pLob210', lobulos[42])
    Actualiza_Texto('pLob215', lobulos[43])
    Actualiza_Texto('pLob220', lobulos[44])
    Actualiza_Texto('pLob225', lobulos[45])
    Actualiza_Texto('pLob230', lobulos[46])
    Actualiza_Texto('pLob235', lobulos[47])
    Actualiza_Texto('pLob240', lobulos[48])
    Actualiza_Texto('pLob245', lobulos[49])
    Actualiza_Texto('pLob250', lobulos[50])
    Actualiza_Texto('pLob255', lobulos[51])
    Actualiza_Texto('pLob260', lobulos[52])
    Actualiza_Texto('pLob265', lobulos[53])
    Actualiza_Texto('pLob270', lobulos[54])
    Actualiza_Texto('pLob275', lobulos[55])
    Actualiza_Texto('pLob280', lobulos[56])
    Actualiza_Texto('pLob285', lobulos[57])
    Actualiza_Texto('pLob290', lobulos[58])
    Actualiza_Texto('pLob295', lobulos[59])
    Actualiza_Texto('pLob300', lobulos[60])
    Actualiza_Texto('pLob305', lobulos[61])
    Actualiza_Texto('pLob310', lobulos[62])
    Actualiza_Texto('pLob315', lobulos[63])
    Actualiza_Texto('pLob320', lobulos[64])
    Actualiza_Texto('pLob325', lobulos[65])
    Actualiza_Texto('pLob330', lobulos[66])
    Actualiza_Texto('pLob335', lobulos[67])
    Actualiza_Texto('pLob340', lobulos[68])
    Actualiza_Texto('pLob345', lobulos[69])
    Actualiza_Texto('pLob350', lobulos[70])
    Actualiza_Texto('pLob355', lobulos[71])
    distancias = Texto_A_Matriz(pDistancias, pRadiales)
    Actualiza_Texto('pDist0', distancias[0])
    Actualiza_Texto('pDist20', distancias[1])
    Actualiza_Texto('pDist40', distancias[2])
    Actualiza_Texto('pDist60', distancias[3])
    Actualiza_Texto('pDist80', distancias[4])
    Actualiza_Texto('pDist100', distancias[5])
    Actualiza_Texto('pDist120', distancias[6])
    Actualiza_Texto('pDist140', distancias[7])
    Actualiza_Texto('pDist160', distancias[8])
    Actualiza_Texto('pDist180', distancias[9])
    Actualiza_Texto('pDist200', distancias[10])
    Actualiza_Texto('pDist220', distancias[11])
    Actualiza_Texto('pDist240', distancias[12])
    Actualiza_Texto('pDist260', distancias[13])
    Actualiza_Texto('pDist280', distancias[14])
    Actualiza_Texto('pDist300', distancias[15])
    Actualiza_Texto('pDist320', distancias[16])
    Actualiza_Texto('pDist340', distancias[17])
    Actualiza_Texto('pDist0', distancias[0])
    Actualiza_Texto('pDist5', distancias[1])
    Actualiza_Texto('pDist10', distancias[2])
    Actualiza_Texto('pDist15', distancias[3])
    Actualiza_Texto('pDist20', distancias[4])
    Actualiza_Texto('pDist25', distancias[5])
    Actualiza_Texto('pDist30', distancias[6])
    Actualiza_Texto('pDist35', distancias[7])
    Actualiza_Texto('pDist40', distancias[8])
    Actualiza_Texto('pDist45', distancias[9])
    Actualiza_Texto('pDist50', distancias[10])
    Actualiza_Texto('pDist55', distancias[11])
    Actualiza_Texto('pDist60', distancias[12])
    Actualiza_Texto('pDist65', distancias[13])
    Actualiza_Texto('pDist70', distancias[14])
    Actualiza_Texto('pDist75', distancias[15])
    Actualiza_Texto('pDist80', distancias[16])
    Actualiza_Texto('pDist85', distancias[17])
    Actualiza_Texto('pDist90', distancias[18])
    Actualiza_Texto('pDist95', distancias[19])
    Actualiza_Texto('pDist100', distancias[20])
    Actualiza_Texto('pDist105', distancias[21])
    Actualiza_Texto('pDist110', distancias[22])
    Actualiza_Texto('pDist115', distancias[23])
    Actualiza_Texto('pDist120', distancias[24])
    Actualiza_Texto('pDist125', distancias[25])
    Actualiza_Texto('pDist130', distancias[26])
    Actualiza_Texto('pDist135', distancias[27])
    Actualiza_Texto('pDist140', distancias[28])
    Actualiza_Texto('pDist145', distancias[29])
    Actualiza_Texto('pDist150', distancias[30])
    Actualiza_Texto('pDist155', distancias[31])
    Actualiza_Texto('pDist160', distancias[32])
    Actualiza_Texto('pDist165', distancias[33])
    Actualiza_Texto('pDist170', distancias[34])
    Actualiza_Texto('pDist175', distancias[35])
    Actualiza_Texto('pDist180', distancias[36])
    Actualiza_Texto('pDist185', distancias[37])
    Actualiza_Texto('pDist190', distancias[38])
    Actualiza_Texto('pDist195', distancias[39])
    Actualiza_Texto('pDist200', distancias[40])
    Actualiza_Texto('pDist205', distancias[41])
    Actualiza_Texto('pDist210', distancias[42])
    Actualiza_Texto('pDist215', distancias[43])
    Actualiza_Texto('pDist220', distancias[44])
    Actualiza_Texto('pDist225', distancias[45])
    Actualiza_Texto('pDist230', distancias[46])
    Actualiza_Texto('pDist235', distancias[47])
    Actualiza_Texto('pDist240', distancias[48])
    Actualiza_Texto('pDist245', distancias[49])
    Actualiza_Texto('pDist250', distancias[50])
    Actualiza_Texto('pDist255', distancias[51])
    Actualiza_Texto('pDist260', distancias[52])
    Actualiza_Texto('pDist265', distancias[53])
    Actualiza_Texto('pDist270', distancias[54])
    Actualiza_Texto('pDist275', distancias[55])
    Actualiza_Texto('pDist280', distancias[56])
    Actualiza_Texto('pDist285', distancias[57])
    Actualiza_Texto('pDist290', distancias[58])
    Actualiza_Texto('pDist295', distancias[59])
    Actualiza_Texto('pDist300', distancias[60])
    Actualiza_Texto('pDist305', distancias[61])
    Actualiza_Texto('pDist310', distancias[62])
    Actualiza_Texto('pDist315', distancias[63])
    Actualiza_Texto('pDist320', distancias[64])
    Actualiza_Texto('pDist325', distancias[65])
    Actualiza_Texto('pDist330', distancias[66])
    Actualiza_Texto('pDist335', distancias[67])
    Actualiza_Texto('pDist340', distancias[68])
    Actualiza_Texto('pDist345', distancias[69])
    Actualiza_Texto('pDist350', distancias[70])
    Actualiza_Texto('pDist355', distancias[71])


''' Se ajusta el extent del mapa '''
dfs = arcpy.mapping.ListDataFrames(mxd, 'Webmap')
if (len(dfs) > 0):
    df = dfs[0]
    
    lyrs = arcpy.mapping.ListLayers(mxd,"CapaPoligonos")
    if (len(lyrs) > 0):
        glyr = lyrs[0]
    
        for lyr in glyr:
            ext = lyr.getExtent()

        df.panToExtent(ext)
   
''' Se configura la leyenda '''
#styleItem = arcpy.mapping.ListStyleItems("ESRI.ServerStyle", "Legend Items", "Horizontal Single Symbol Label Only")[0]
'''
legends = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")
if len(legends)>0:
    legend = legends[0]
'''
#    for lyr in legend.listLegendItemLayers():
#        legend.updateItem(lyr, styleItem)

#df.name = Layout_Template

''' Se configura el nombre de archivo de salida '''
arcpy.AddMessage("Se configura el nombre de archivo de salida")
ahora = datetime.datetime.now()
output = 'Calculo_{}_{}_{}_{}_{}_{}.{}'.format(ahora.year,ahora.month,ahora.day, ahora.hour,ahora.minute,ahora.second, Format)
#output = 'WebMap_{}{}{}{}{}{}.{}'.format(str(uuid.uuid1()), Format)
# C:\arcgisserver\directories\arcgisjobs\subtel2\imprimir_gpserver\j0f754de513dd47e5ac41eb3acc5cb595\scratch
Output_File = os.path.join(arcpy.env.scratchFolder, output)
Actualiza_Texto('tDocumento', Output_File)

''' Se exporta, por defecto a PDF'''
if Format.lower() == 'pdf':
    arcpy.AddMessage("Se exporta, por defecto a PDF")
    arcpy.mapping.ExportToPDF(mxd, Output_File) 
elif Format.lower() == 'png':
    arcpy.mapping.ExportToPNG(mxd, Output_File)

''' Se entrega el resultado como parametro '''
arcpy.AddMessage("Se entrega el resultado como parametro {}".format(Output_File))
arcpy.SetParameterAsText(1, Output_File)

''' Limpieza final '''
filePath = mxd.filePath
del mxd, result
os.remove(filePath)
arcpy.AddMessage("***FIN***")