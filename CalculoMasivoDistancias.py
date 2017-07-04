# -*- coding: iso-8859-15 -*-
'''
Created on 29/12/2015

@author: kimie
'''
import arcpy
import ParametrosFormulario
import TareasGeometricas
import TablaDeValores
import CalculosZona1546
import CalculosZona1812
import CalculosZona1546mas
import CalculosZona1546menos
import CalculosZona370

def calculaGrados(valor):
    t = str(int(valor))
    l = len(t)
    #arcpy.AddMessage(float(t[l-4:l-2])/60)
    #arcpy.AddMessage((float(t[l-2:l])/3600))
    return float("{0:.5f}".format(float(t[0:l-4]))) + float("{0:.5f}".format(float(t[l-4:l-2])/60)) + float("{0:.5f}".format((float(t[l-2:l])/3600)))    
    #return (float(t[0:l-4])) + (float(t[l-4:l-2])/60) + ((float(t[l-2:l])/3600))

def validaFloat(v):
    t = "{}".format(v)
    if t == "None":
        return 0.0
    else:
        return float(t)
        
def ObtieneParametros(row): #(self, row, radiales):
    params = ParametrosFormulario.ParametrosFormulario()
    params.recomendacion = recomendacion #'1546+'
    params.frecuencia = validaFloat(row[dict['FRECUENCIA']])
    params.potencia = validaFloat(row[dict['POTENCIA']])/1000   # Pasar de watts a kilowatts
    params.ganancia = validaFloat(row[dict['G_ANT_DBD']])
    params.alturaAntenaTransmisora = validaFloat(row[dict['ALTURA_TX']])
    #params.alturaAntenaReceptora = row[]
    params.latitud = -calculaGrados(row[dict['LAT_PTX']])
    params.longitud = -calculaGrados(row[dict['LONG_PTX']])
    params.perdidaCablesConectores= validaFloat(row[dict['PERDIDA_CABLE_CONECTOR']])
    #params.perdidaDivisorPotencia= row[]
    #params.otrasPerdidas= row[]
    params.radiales = 72
    if ('RADIALES' in dict.keys() ):
        params.radiales = int(row[dict['RADIALES']]) 
    params.perdidasLobulo = []
    for p in range(0,params.radiales):  
        params.perdidasLobulo.append( validaFloat(row[dict['PLOB0']+p]) )
    #params.obstaculosCircundantesTx= row[]
    #params.obstaculosCircundantesRx= row[]
    params.toleranciaZonasSombra = 1
    if ('TOLERANCIA_SOMBRA' in dict.keys() ):
        params.toleranciaZonasSombra = row[dict['TOLERANCIA_SOMBRA']]
    params.resolucionCalculo = 500 
    if ('RESOLUCION_CALCULO' in dict.keys() ):
        params.resolucionCalculo = row[dict['RESOLUCION_CALCULO']]
    params.porcentajeUbicacion = 90
    if ('PORCENTAJE_UBICACION' in dict.keys() ):
        params.porcentajeUbicacion = row[dict['PORCENTAJE_UBICACION']]   
    #params.porcentajeTiempo= row[]
    #params.porcentajeUbicacion = row[]
    params.intensidadCampoReferencia = row[dict['CAMPO_LIMITE']]
    #arcpy.AddMessage(params.frecuencia)
    #arcpy.AddMessage(params.potencia)
    #arcpy.AddMessage(params.ganancia)
    #arcpy.AddMessage(params.alturaAntenaTransmisora)
    #arcpy.AddMessage(params.latitud)
    #arcpy.AddMessage(params.longitud)
    #arcpy.AddMessage(params.perdidasLobulo)
    #arcpy.AddMessage(params.toleranciaZonasSombra)
    #arcpy.AddMessage(params.resolucionCalculo)
    #arcpy.AddMessage(params.intensidadCampoReferencia)
    params.imagen = imagen
    params.revalidaParametros()
    return params

arcpy.env.overwriteOutput = True
tareasGeo = TareasGeometricas.TareasGeometricas()

tabla = arcpy.GetParameter(0)
imagen = arcpy.GetParameter(1)
recomendacion = arcpy.GetParameter(2)

# Se crea un dicionario con los nombres de los campos y sus posiciones dentro de la tabla
dict = {}
campos = []
pos = 0
for f in arcpy.ListFields(tabla):
    dict[f.name] = pos
    campos.append(f.name)
    pos = pos + 1

# estos campos deben venir
'''
campos = ['frecuencia','potencia','campo_limite', \
          'lat_ptx','long_ptx','tipo_servicio','altura_tx', \
          'g_ant_dbd','perdida_cable_conector', \
          'plob0','plob20','plob40','plob60','plob80','plob100','plob120','plob140','plob160', \
          'plob180','plob200','plob220','plob240','plob260','plob280','plob300','plob320','plob340',  \
          'Zs0','Zs20','Zs40','Zs60','Zs80','Zs100','Zs120','Zs140','Zs160', \
          'Zs180','Zs200','Zs220','Zs240','Zs260','Zs280','Zs300','Zs320','Zs340' ]
            # 27 posicion de Zs
'''
# se crea una replica de la tabla conlos mismos campos      
arcpy.AddMessage("Generando nueva tabla")    
tablaSalida = arcpy.CreateTable_management(arcpy.env.scratchGDB, 'Tabla_Salida')
for f in arcpy.ListFields(tabla):
    if (f.name != 'OBJECTID'):  # menos el objetid que se crea solo
        arcpy.AddField_management(tablaSalida, f.name, f.type, f.precision, f.scale, f.length)
curSalida = arcpy.da.InsertCursor(tablaSalida, campos)

# se recorre la tabla
cursor = arcpy.da.SearchCursor(tabla, campos)
for row in cursor:
    
    arcpy.AddMessage("Procesando Identificador:{}".format(row[dict['IDENTIFICADOR']].encode(encoding='UTF-8',errors='strict')))
 
    # Se copian los valores de todos los campos directamente de la tabla original
    valores = []
    for x in range(0,len(campos)):
        valores.append( row[x] )
        
    rm = False
    if ('RADIO_MAXIMO' in dict.keys() ):
        radio = row[dict['RADIO_MAXIMO']]
        if ( radio > 0 ):
            rm = True

    if ( rm ):
        # Si existe el campo radio maximo y su valor es mayor a cero 
        # no se realiza el calculo y se dejan los radiales en cero
        arcpy.AddMessage("Se omite el calculo de distancias, esta definido un radio maximo")
        for x in range(0,params.radiales):
            valores[ dict['Zs{}'.format(x*(360/params.radiales))] ] = 0
            
    else:
        # se realiza el calculo
        params = ObtieneParametros(row)
        #params.imprimeParametros()
        nubePuntos = tareasGeo.GeneraNubeDePuntos(params.latitud, params.longitud, params.imagen, params.resolucionCalculo, params.radiales)
        matrizCotas = tareasGeo.GeneraMatrizDeCotas(nubePuntos, params.resolucionCalculo)
        tablaValores = TablaDeValores.TablaValores(params, matrizCotas)
        
        if ( params.recomendacion == "1546-" ):
            arcpy.AddMessage("Calculos para recomendacion 1546-")
            # Calculos para recomendacion 1546
            calculo1546 = CalculosZona1546.CalculosZona1546(params, tablaValores)
            a1546 = calculo1546.Inicio_1546(params.radiales)
            distancias = calculo1546.Inicio_1546(params.radiales)
        
        if ( params.recomendacion == "1812" ):
            arcpy.AddMessage("Calculos para recomendacion 1812")
            # Calculos para recomendacion 1546
            calculo1812 = CalculosZona1812.CalculosZona1812(params, tablaValores)
            a1812 = calculo1812.Inicio_1812(params.radiales)
            distancias = calculo1812.Inicio_1812(params.radiales)
                             
        if ( params.recomendacion == "1546+" ):
            arcpy.AddMessage("Calculos para recomendacion 1546+")
            # Calculos para recomendacion 1546
            calculo1546 = CalculosZona1546.CalculosZona1546(params, tablaValores)
            a1546 = calculo1546.Inicio_1546(params.radiales)
            # Calculos para recomendacion 1812
            if(params.radiales == 18):
                calculo1812 = CalculosZona1812.CalculosZona1812(params, tablaValores)
                a1812 = calculo1812.Inicio_1812(params.radiales)
                dlt = calculo1812.dlt
                # Calculos para recomendacion 1546+
                calculo1546mas = CalculosZona1546mas.CalculosZona1546mas(params, a1546, a1812, dlt)
                distancias = calculo1546mas.Inicio_1546mas(params.radiales)
            else:
                calculo1546menos = CalculosZona1546menos.CalculosZona1546menos(params, tablaValores)
                a1546 = calculo1546menos.Inicio_1546menos(params.radiales)
                distancias = calculo1546menos.Inicio_1546menos(params.radiales)

        if ( params.recomendacion == "1546" ):
            arcpy.AddMessage("Calculos para recomendacion 1546")
            # Calculos para recomendacion 1546
            calculo1546menos = CalculosZona1546menos.CalculosZona1546menos(params, tablaValores)
            a1546 = calculo1546menos.Inicio_1546menos(params.radiales)
            distancias = calculo1546menos.Inicio_1546menos(params.radiales)
                
        if ( params.recomendacion == "370" ):
            arcpy.AddMessage("Calculos para recomendacion 370")
            calculo370 = CalculosZona370.CalculosZona370(params, tablaValores)
            distancias = calculo370.Inicio_370(params.radiales)
        
        # Se actualizan solo los valores de los campos de distancias
        for x in range(0,params.radiales):
            valores[ dict['Zs{}'.format(x*(360/params.radiales))] ] = distancias[x]
            #valores[ dict['Zs0'] ] = distancias[0]
    
    # Se crea el registro en la tabla de salida
    tupla = tuple(valores)
    curSalida.insertRow(tupla)

arcpy.SetParameter(3, tablaSalida)
arcpy.AddMessage("FIN")       
        
