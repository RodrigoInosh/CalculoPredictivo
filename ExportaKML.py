# -*- encoding: utf-8 -*-
import arcpy
import os
import uuid

Web_Map_as_JSON = arcpy.GetParameterAsText(0)

result = arcpy.mapping.ConvertWebMapToMapDocument(Web_Map_as_JSON)
mxd = result.mapDocument

output = 'Zmax_{}.kmz'.format(str(uuid.uuid1()))
Output_File = os.path.join(arcpy.env.scratchFolder, output)

''' Esta arreglado para correr desde desktop y poder publicar el geoproceso '''
lyrs = arcpy.mapping.ListLayers(mxd,"CapaPoligonos")
if len(lyrs) > 0:
    lyr = lyrs[0] 
    arcpy.LayerToKML_conversion(lyr, Output_File)

arcpy.SetParameterAsText(1, Output_File)



output = 'Zs_{}.kmz'.format(str(uuid.uuid1()))
Output_File2 = os.path.join(arcpy.env.scratchFolder, output)

''' Esta arreglado para correr desde desktop y poder publicar el geoproceso '''
lyrs = arcpy.mapping.ListLayers(mxd,"CapaCalculoPoligonos")
if len(lyrs) > 0:
    lyr = lyrs[0] 
    arcpy.LayerToKML_conversion(lyr, Output_File2)

arcpy.SetParameterAsText(2, Output_File2)




''' Limpieza final '''
filePath = mxd.filePath
del mxd, result
os.remove(filePath)
arcpy.AddMessage("***FIN***")