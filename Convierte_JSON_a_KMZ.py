# -*- encoding: utf-8 -*-
'''
Created on 16-04-2014
@author: CristianRodriguez
'''
import arcpy
import json
import zipfile
import os
import uuid

def GeneraPoligono(anillo_json):
    fcPoli = arcpy.CreateFeatureclass_management("in_memory","area","POLYGON","","DISABLED","ENABLED",srWebMercator)
    curPoli = arcpy.da.InsertCursor(fcPoli,["SHAPE@"])
    vertices = [ arcpy.Point(par[0],par[1]) for par in anillo_json ]
    poli = arcpy.Polygon(arcpy.Array(vertices))
    curPoli.insertRow(tuple([poli]))
    return fcPoli

def GeneraPunto(punto_json):
    fcPunto = arcpy.CreateFeatureclass_management("in_memory","punto","POINT","","DISABLED","ENABLED",srWebMercator)
    curPunto = arcpy.da.InsertCursor(fcPunto,["SHAPE@"])
    p = arcpy.Point(punto_json['x'], punto_json['y'])
    curPunto.insertRow((p,))
    return fcPunto

def GeneraListaParesCoordenados(fcPoli):
    for row in arcpy.da.SearchCursor(fcPoli, ["SHAPE@"]):
        wkt = row[0].WKT
    ini = wkt.find('(((') + 3
    fin = wkt.find(')))')
    coords = wkt[ini:fin]
    coords = coords.replace(', ', ';')
    coords = coords.replace(' ', ',')
    coords = coords.replace(';', ' ')
    return coords

def GeneraParCoordenado(fcPunto):
    for row in arcpy.da.SearchCursor(fcPunto, ["SHAPE@"]):
        wkt = row[0].WKT
    ini = wkt.find('(') + 1
    fin = wkt.find(')')
    coords = wkt[ini:fin]
    coords = coords.replace(' ', ',')
    return coords
        
def GeneraXMLLayerOperacional(oLayer, folder_id, folder_name, placemark_id, placemark_name, styleUrl):
    arcpy.AddMessage('Se procesa capa {}'.format(oLayer['id']))
    kml = ''
    #por defecto se usa '0' para el primer layer
    featureSet = oLayer['featureCollection']['layers'][0]['featureSet']
    tipoGeometrico = featureSet['geometryType']
    if tipoGeometrico == u'esriGeometryPolygon':
        #se usa solo el primer anillo de la primera feature del featureset
        anillo = featureSet['features'][0]['geometry']['rings'][0]
        
        fcPoli = GeneraPoligono(anillo)
        pProy = arcpy.env.scratchGDB + "\\poliProj"
        fcPoli_proj = arcpy.Project_management(fcPoli, pProy, srWGS84)
        coords = GeneraListaParesCoordenados(fcPoli_proj)
        
        kml += '    <Folder id="' + folder_id + '">\n'
        kml += '      <name>' + folder_name + '</name>\n'
        kml += '      <Snippet></Snippet>\n'
        kml += '      <Placemark id="' + placemark_id + '">\n'
        kml += '        <name>' + placemark_name + '</name>\n'
        kml += '        <Snippet></Snippet>\n'
        kml += '        <description></description>\n'
        kml += '        <styleUrl>' + styleUrl + '</styleUrl>\n'
        
        kml += '        <MultiGeometry>\n'
        kml += '          <Polygon>\n'
        kml += '            <extrude>0</extrude>\n'
        kml += '            <altitudeMode>clampToGround</altitudeMode>\n'
        kml += '            <outerBoundaryIs>\n'
        kml += '              <LinearRing>\n'
        kml += '                <coordinates> ' + coords + '</coordinates>\n'
        kml += '              </LinearRing>\n'
        kml += '            </outerBoundaryIs>\n'
        kml += '          </Polygon>\n'
        kml += '        </MultiGeometry>\n'
        
        kml += '      </Placemark>\n'
        kml += '    </Folder>\n'
        
    if tipoGeometrico == u'esriGeometryPoint':
        punto = featureSet['features'][0]['geometry']
        
        fcPunto = GeneraPunto(punto)
        pProy = arcpy.env.scratchGDB + "\\puntoProj"
        fcPunto_proj = arcpy.Project_management(fcPunto, pProy, srWGS84)
        coords = GeneraParCoordenado(fcPunto_proj)
            
        kml += '    <Folder id="' + folder_id + '">\n'
        kml += '      <name>' + folder_name + '</name>\n'
        kml += '      <Snippet></Snippet>\n'
        kml += '      <Placemark id="' + placemark_id + '">\n'
        kml += '        <name>' + placemark_name + '</name>\n'
        kml += '        <Snippet></Snippet>\n'
        kml += '        <description></description>\n'
        kml += '        <styleUrl>' + styleUrl + '</styleUrl>\n'
        
        kml += '        <Point>\n'
        kml += '          <altitudeMode>clampToGround</altitudeMode>\n'
        kml += '          <coordinates> ' + coords + '</coordinates>\n'
        kml += '        </Point>\n'
        
        kml += '      </Placemark>\n'
        kml += '    </Folder>\n'
        
    return kml

def GeneraKML(groupLayers,estilos):
    arcpy.AddMessage('Se compone KML')
    kml =  '<?kml version="1.0" encoding="UTF-8"?>\n'
    kml += '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
    kml += 'xsi:schemaLocation="http://www.opengis.net/kml/2.2 http://schemas.opengis.net/kml/2.2.0/ogckml22.xsd http://www.google.com/kml/ext/2.2 http://code.google.com/apis/kml/schema/kml22gx.xsd">\n'
    kml += '<Document id="CalculoAreaServicio">\n'
    kml += '  <name>CalculoAreaServicio</name>\n'
    kml += '  <Snippet></Snippet>\n'
    kml += groupLayers
    kml += estilos
    kml += '</Document>'
    kml += '</kml>'
    return kml

def GeneraKMLGroupLayer(id_, nombre, contenido):
    kml =  '  <Folder id="' + id_ + '">\n'
    kml += '    <name>' + nombre + '</name>\n'
    kml += '    <Snippet></Snippet>\n'
    kml += contenido
    kml += '    </Folder>\n'
    return kml

def GeneraKMLEstilo():
    kml =  '  <Style id="EstiloAreaServicio">\n'
    kml += '    <LabelStyle>\n'
    kml += '      <color>00000000</color>\n'
    kml += '      <scale>0.000000</scale>\n'
    kml += '    </LabelStyle>\n'
    kml += '    <LineStyle>\n'
    kml += '      <color>ffff00c5</color>\n'
    kml += '      <width>1.500000</width>\n'
    kml += '    </LineStyle>\n'
    kml += '    <PolyStyle>\n'
    kml += '      <color>1aff00c5</color>\n'
    kml += '      <outline>1</outline>\n'
    kml += '    </PolyStyle>\n'
    kml += '  </Style>\n'
    
    kml += '  <Style id="EstiloAreaMaxima">\n'
    kml += '    <LabelStyle>\n'
    kml += '      <color>00000000</color>\n'
    kml += '      <scale>0.000000</scale>\n'
    kml += '    </LabelStyle>\n'
    kml += '    <LineStyle>\n'
    kml += '      <color>ff000000</color>\n'
    kml += '      <width>1.500000</width>\n'
    kml += '    </LineStyle>\n'
    kml += '    <PolyStyle>\n'
    kml += '      <color>1a000000</color>\n'
    kml += '      <outline>1</outline>\n'
    kml += '    </PolyStyle>\n'
    kml += '  </Style>\n'
    
    kml += '  <Style id="CruzLila">\n'
    kml += '    <IconStyle>\n'
    kml += '      <Icon><href>CruzLila.png</href></Icon>\n'
    kml += '      <scale>1.250000</scale>\n'
    kml += '    </IconStyle>\n'
    kml += '  <LabelStyle>\n'
    kml += '    <color>00000000</color>\n'
    kml += '    <scale>0.000000</scale>\n'
    kml += '  </LabelStyle>\n'
    kml += '  <PolyStyle>\n'
    kml += '    <color>ff000000</color>\n'
    kml += '    <outline>0</outline>\n'
    kml += '  </PolyStyle>\n'
    kml += '</Style>\n'
    
    kml += '  <Style id="CruzNegra">\n'
    kml += '    <IconStyle>\n'
    kml += '      <Icon><href>CruzNegra.png</href></Icon>\n'
    kml += '      <scale>1.250000</scale>\n'
    kml += '    </IconStyle>\n'
    kml += '  <LabelStyle>\n'
    kml += '    <color>00000000</color>\n'
    kml += '    <scale>0.000000</scale>\n'
    kml += '  </LabelStyle>\n'
    kml += '  <PolyStyle>\n'
    kml += '    <color>ff000000</color>\n'
    kml += '    <outline>0</outline>\n'
    kml += '  </PolyStyle>\n'
    kml += '</Style>\n'
    
    return kml

srWGS84 = arcpy.SpatialReference(4326)   #GCS_WGS_84
srWebMercator = arcpy.SpatialReference(3857)  #WGS_1984_Web_Mercator_Auxiliary_Sphere
arcpy.env.overwriteOutput = True

Web_Map_as_JSON = arcpy.GetParameterAsText(0)
if Web_Map_as_JSON == '#' or not Web_Map_as_JSON:
    Web_Map_as_JSON = '{"operationalLayers":[]}' 

arcpy.AddMessage('Se carga JSON')
datos = json.loads(Web_Map_as_JSON)

kml_layers_Zs = ''
kml_layers_Zm = ''
kml_layers_Zm_p = ''
kml_layers_Zs_p = ''
for oLayer in datos['operationalLayers']:
    if oLayer['id'] == u'capaPuntos':
        kml_layers_Zm_p += GeneraXMLLayerOperacional(oLayer, 'Featurelayer0', 'Punto', 'ID_10000', 'Override 1', '#CruzNegra')
    if oLayer['id'] == u'capaCalculoPuntos':
        kml_layers_Zs_p += GeneraXMLLayerOperacional(oLayer, 'Featurelayer1', 'Punto', 'ID_20000', 'Override 1', '#CruzLila')
    if oLayer['id'] == u'capaCalculoPoligonos':
        kml_layers_Zs += GeneraXMLLayerOperacional(oLayer, 'Featurelayer2', 'Area', 'ID_30000', 'Override 1', '#EstiloAreaServicio')
    if oLayer['id'] == u'capaPoligonos':
        kml_layers_Zm += GeneraXMLLayerOperacional(oLayer, 'Featurelayer3', 'Area', 'ID_40000', 'Override 1', '#EstiloAreaMaxima')

groupLayerZs = GeneraKMLGroupLayer('GroupLayer0','AreaServicio', kml_layers_Zs+kml_layers_Zs_p)
groupLayerZm = GeneraKMLGroupLayer('GroupLayer1','AreaMaxima', kml_layers_Zm+kml_layers_Zm_p)

xKML = GeneraKML(groupLayerZs+groupLayerZm, GeneraKMLEstilo())

#guardar archivo KML
archivo_kml = 'Calculo_{}.kml'.format(str(uuid.uuid1()))
Output_File_KML = os.path.join(arcpy.env.scratchFolder, archivo_kml)
arcpy.AddMessage('Se genera KML: {}'.format(Output_File_KML))
with open(Output_File_KML, 'w') as f:
    f.write(xKML)

#genera archivo KMZ
archivo_zip = 'Calculo_{}.kmz'.format(str(uuid.uuid1()))
Output_File_KMZ = os.path.join(arcpy.env.scratchFolder, archivo_zip)
Archivo_Imagen_CruzLila = r'C:\arcgisserver\imagenesKMLSUBTEL\CruzLila.png'
Archivo_Imagen_CruzNegra = r'C:\arcgisserver\imagenesKMLSUBTEL\CruzNegra.png'
with zipfile.ZipFile(Output_File_KMZ, 'a') as myzip:
    myzip.write(Output_File_KML, 'doc.kml')
    myzip.write(Archivo_Imagen_CruzLila, 'CruzLila.png')
    myzip.write(Archivo_Imagen_CruzNegra, 'CruzNegra.png')
    
arcpy.AddMessage('Archivo KMZ:{}'.format(Output_File_KMZ))
arcpy.SetParameterAsText(1, Output_File_KMZ)

os.remove(Output_File_KML)
