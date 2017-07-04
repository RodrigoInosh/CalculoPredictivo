# -*- coding: iso-8859-15 -*-
'''
Created on 18-02-2014

@author: CRodriguez
'''
import OtrosCalculos as Calculos
#import arcpy

class CalculosZona1546mas():
    
    def __init__(self, params, a1546, a1812, dlt):
        self.a1546 = a1546
        self.a1812 = a1812
        self.dlt = dlt
        self.params = params
        
    def calculo1546mas(self, radiales):
        if (self.params.intensidadCampoReferencia <= 9):
            if ((self.dlt[radiales] > 15) and (self.dlt[radiales] < self.a1546[radiales]-16) and (self.a1546[radiales] > self.a1812[radiales])):
                V = self.a1812[radiales]
            else:
                V = self.a1546[radiales]
        else:
            if ((self.a1546[radiales] < 1) and (self.a1812[radiales] < 1)):
                if ( Calculos.Max(self.a1546[radiales], self.a1812[radiales]) > 0.25):
                    V = Calculos.Max(self.a1546[radiales], self.a1812[radiales])
                else:
                    V = 0.25
            else:
                if (self.a1546[radiales] > 1):
                    V = self.a1546[radiales]
                else:
                    V = 1    
        
        return V

    def Inicio_1546mas(self, radiales):
        # Calculos para recomendacion 1546+
        a1546mas = []
        for r in range(0,radiales):
            a1546mas.append(self.calculo1546mas(r))
            #arcpy.AddMessage("{}".format(a1546mas[r]))
            #print "{}".format(a1546mas[r])
        return a1546mas
    