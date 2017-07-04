# -*- coding: iso-8859-15 -*-
import arcpy
import os
import uuid
                
Web_Map_as_JSON = arcpy.GetParameterAsText(0)

output = 'WebMap_{}.txt'.format(str(uuid.uuid1()))
Output_File = os.path.join(arcpy.env.scratchFolder, output)

f = open(Output_File, 'w')
f.write(Web_Map_as_JSON)
f.close

arcpy.SetParameterAsText(1, Output_File)
arcpy.AddMessage("***FIN***")