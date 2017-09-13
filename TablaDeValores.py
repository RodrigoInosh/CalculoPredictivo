# -*- coding: iso-8859-15 -*-
'''
Created on 12-02-2014

@author: CRodriguez
'''
import math
import OtrosCalculos as Calculos
import arcpy

class TablaValores():
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

           
    def Calcula_ListaDistanciasKM(self):
        self.tablaCotas_DistanciasKM = [d*0.5*(self.params.resolucionCalculo/500) for d in range(0,201)]  # validar que siempre son 500 mts

    def Calcula_him(self, radiales):
        # Validado: 12 feb 2014
        self.tablaCotas_him = []
        #radiales1 = int(radiales)
        for radial in range(0,radiales): 
            valores = []
            
            rango = 1 + int(30/(self.params.resolucionCalculo/500))
            
            for dist in range(0,rango):
                suma = 0
                for pos in range(0,dist+1):
                    suma = suma + self.Matriz_Cotas(radial, pos)
                promedio = float(suma)/float(dist+1)
                valores.append(promedio)
                
            self.tablaCotas_him.append(valores)
        
    # radial, distancia    
    def Matriz_Cotas(self, r, d):
        radiales = self.params.radiales
        if r>=0 and r<=(radiales-1):
            if d>=0 and d<=200:
                return self.tablaCotas[int(d)][int(r)] 
            else:
                #arcpy.AddMessage("El valor de distancia esta fuera de rango {}".format(d))
                return self.tablaCotas[int(200)][int(r)] 
        else:
            arcpy.AddMessage("El valor de radial esta fuera de rango {}".format(r));
        return 0
    
    def Matriz_Cotas_GrKm(self,radialGrados, distanciaKilometros):
        saltoangular = 360 / self.params.radiales
        return self.Matriz_Cotas(radialGrados/saltoangular, distanciaKilometros * 2)

    def Calcula_ADT(self, radiales):
        #self.TablaCotas_ADT = []
        self.tablaCotas_ADT_Maximos = []
        cota_antena = self.Matriz_Cotas(0,0) + self.params.alturaAntenaTransmisora
        #radiales1 = int(radiales)
        for r in range(0,radiales):
            valores = []
            #KCS: este rango deberia modificarse para rcc?
            for d in range(0,31):
                cota = self.Matriz_Cotas(r,d)
                if ( (cota - cota_antena) < 0):
                    h = 0
                else:
                    if (self.tablaCotas_DistanciasKM[d] == 0):
                        arcpy.AddMessage("Distancia 0 para d:{}, r:{} cota:{}, cota antena:{}".format(d, r, cota, cota_antena))
                        h = 0
                    else:
                        h = ((cota - cota_antena)/1000) / self.tablaCotas_DistanciasKM[d]
                v = Calculos.grados(math.atan(h))
                valores.append(v)
            self.tablaCotas_ADT_Maximos.append(max(valores))
            #self.tablaCotas_ADT.append(valores)
        
    """
    calculos hecho en la hoja de excel, esta abajo de donde 
    se encuentran los valores de cotas
    """
    def Calcula_Valores(self, radiales):
        # Validado: 13 feb 2014 
        him = []
        B4 = round( self.params.resolucionCalculo/500, 2)
        #radiales1 = int(radiales)
        if (B4 == 1):  #promedio de filas 11 a la 35 (3km a 15km)(posiciones de la 6 a la 30)
            for r in range(0,radiales):
                suma = 0
                for t in range(6,31):  #validar los rangos
                    suma = suma + self.Matriz_Cotas(r, t)
                him.append(suma / 25)
        elif (B4 == 0.2):
            for r in range(0,radiales):
                suma = 0
                for t in range(30,151):   #15km a 75km
                    suma = suma + self.Matriz_Cotas(r, t)
                him.append(suma / 120)
        elif (B4 == 0.5):
            for r in range(0,radiales):
                suma = 0
                for t in range(12,61):   #calculo370
                    suma = suma + self.Matriz_Cotas(r, t)
                him.append(suma / 48)
        else:
            for r in range(0,radiales):
                suma = 0
                for t in range(40 + 20*(0.1/B4)**2, 201):   #30km a 100km
                    suma = suma + self.Matriz_Cotas(r, t)
                him.append(suma / (160-20*(0.1/B4)**2))
        
        ho = self.Matriz_Cotas(0,0)   #valor de la cota 0
        hot = self.params.alturaAntenaTransmisora
        h1 = []
        for r in range(0,radiales):
            suma = ho + hot - him[r]
            if (suma >= 1200):
                h1.append(1200)
            else:
                h1.append(suma)
            
        self.tablaCotas_Valores = {'ho': ho, 'hot': hot, 'him': him, 'h1': h1}
        
    """
    reproduce los calculos de la hoja 100land50 del excel
    C4 es un valor de distancia
    """
    def Calcula_100land50(self, C4):
        # Validado: 13 feb 2014 
        A4 = Calculos.Log10(C4)
        #1,51*A4^6-17,895*A4^5+70,131*A4^4-114,66*A4^3+72,259*A4^2-48,766*A4+90,18
        D4 = (1.51*A4**6)-(17.895*A4**5)+(70.131*A4**4)-(114.66*A4**3)+(72.259*A4**2)-(48.766*A4)+(90.18)
        #0,3299*A4^6-7,4813*A4^5+37,064*A4^4-69,438*A4^3+45,626*A4^2-40,535*A4+92,294
        E4 = (0.3299*A4**6)-(7.4813*A4**5)+(37.064*A4**4)-(69.438*A4**3)+(45.626*A4**2)-(40.535*A4)+(92.294)
        #-1,0026*A4^6+4,3377*A4^5-0,7297*A4^4-17,47*A4^3+15,834*A4^2-32,691*A4+94,681
        F4 = (-1.0026*A4**6)+(4.3377*A4**5)-(0.7297*A4**4)-(17.47*A4**3)+(15.834*A4**2)-(32.691*A4)+(94.681)
        #-2,4965*A4^6+17,774*A4^5-44,59*A4^4+44,793*A4^3-21,335*A4^2-23,307*A4+97,362
        G4 = (-2.4965*A4**6)+(17.774*A4**5)-(44.59*A4**4)+(44.793*A4**3)-(21.335*A4**2)-(23.307*A4)+(97.362)
        #-4,14*A4^6+32,866*A4^5-95,275*A4^4+119,82*A4^3-68,885*A4^2-10,992*A4+100,19
        H4 = (-4.14*A4**6)+(32.866*A4**5)-(95.275*A4**4)+(119.82*A4**3)-(68.885*A4**2)-(10.992*A4)+(100.19)
        #-5,8737*A4^6+49,309*A4^5-152,69*A4^4+209,14*A4^3-129,15*A4^2+5,4035*A4+102,83
        I4 = (-5.8737*A4**6)+(49.309*A4**5)-(152.69*A4**4)+(209.14*A4**3)-(129.15*A4**2)+(5.4035*A4)+(102.83)
        #-7,5306*A4^6+66,172*A4^5-216,05*A4^4+315,63*A4^3-206,65*A4^2+27,275*A4+104,65
        J4 = (-7.5306*A4**6)+(66.172*A4**5)-(216.05*A4**4)+(315.63*A4**3)-(206.65*A4**2)+(27.275*A4)+(104.65)
        #-7,7186*A4^6+72,01*A4^5-251,81*A4^4+397,66*A4^3-280,68*A4^2+50,735*A4+105,27
        K4 = (-7.7186*A4**6)+(72.01*A4**5)-(251.81*A4**4)+(397.66*A4**3)-(280.68*A4**2)+(50.735*A4)+(105.27)
        #-0,00000004*A4^6+0,0000003*A4^5-0,0000007*A4^4+0,0000007*A4^3-0,00000008*A4^2-20*A4+106,9
        L4 = (-0.00000004*A4**6)+(0.0000003*A4**5)-(0.0000007*A4**4)+(0.0000007*A4**3)-(0.00000008*A4**2)-(20*A4)+(106.9)
        lista1 = [10,20,37.5,75,150,300,600,1200,0]
        lista2 = [D4,E4,F4,G4,H4,I4,J4,K4,L4]
        return [lista1, lista2]
 
    """
    reproduce los calculos de la hoja 600land50 del excel
    C4 es un valor de distancia
    """
    def Calcula_600land50(self, C4):
        # Validado: 13 feb 2014 
        A4 = Calculos.Log10(C4)
        #1,1579*A4^6-11,398*A4^5+35,332*A4^4-39,51*A4^3+7,9826*A4^2-37,976*A4+92,639
        D4 = (1.1579*A4**6)-(11.398*A4**5)+(35.332*A4**4)-(39.51*A4**3)+(7.9826*A4**2)-(37.976*A4)+(92.639)
        #0,6738*A4^6-8,2119*A4^5+30,312*A4^4-43,496*A4^3+17,846*A4^2-37,313*A4+94,852
        E4 = (0.6738*A4**6)-(8.2119*A4**5)+(30.312*A4**4)-(43.496*A4**3)+(17.846*A4**2)-(37.313*A4)+(94.852)
        #0,0527*A4^6-3,7463*A4^5+21,03*A4^4-42,033*A4^3+27,113*A4^2-39,157*A4+97,138
        F4 = (0.0527*A4**6)-(3.7463*A4**5)+(21.03*A4**4)-(42.033*A4**3)+(27.113*A4**2)-(39.157*A4)+(97.138)
        #-1,0787*A4^6+5,4862*A4^5-4,7487*A4^4-15,076*A4^3+19,961*A4^2-37,869*A4+99,864
        G4 = (-1.0787*A4**6)+(5.4862*A4**5)-(4.7487*A4**4)-(15.076*A4**3)+(19.961*A4**2)-(37.869*A4)+(99.864)
        #-2,7405*A4^6+20,1*A4^5-51,134*A4^4+48,252*A4^3-15,711*A4^2-28,785*A4+102,53
        H4 = (-2.7405*A4**6)+(20.1*A4**5)-(51.134*A4**4)+(48.252*A4**3)-(15.711*A4**2)-(28.785*A4)+(102.53)
        #-4,8978*A4^6+40,059*A4^5-119,13*A4^4+151,6*A4^3-84,357*A4^2-9,6264*A4+104,62
        I4 = (-4.8978*A4**6)+(40.059*A4**5)-(119.13*A4**4)+(151.6*A4**3)-(84.357*A4**2)-(9.6264*A4)+(104.62)
        #-7,4655*A4^6+65,193*A4^5-210,43*A4^4+301,06*A4^3-191,65*A4^2+20,828*A4+105,63
        J4 = (-7.4655*A4**6)+(65.193*A4**5)-(210.43*A4**4)+(301.06*A4**3)-(191.65*A4**2)+(20.828*A4)+(105.63)
        #-9,0872*A4^6+84,796*A4^5-295,62*A4^4+464,18*A4^3-324,81*A4^2+60,405*A4+105,49
        K4 = (-9.0872*A4**6)+(84.796*A4**5)-(295.62*A4**4)+(464.18*A4**3)-(324.81*A4**2)+(60.405*A4)+(105.49)
        #-0,00000004*A4^6+0,0000003*A4^5-0,0000007*A4^4+0,0000007*A4^3-0,00000008*A4^2-20*A4+106,9
        L4 = (-0.00000004*A4**6)+(0.0000003*A4**5)-(0.0000007*A4**4)+(0.0000007*A4**3)-(0.00000008*A4**2)-(20*A4)+(106.9)
        lista1 = [10,20,37.5,75,150,300,600,1200,0]
        lista2 = [D4,E4,F4,G4,H4,I4,J4,K4,L4]
        return [lista1, lista2]
    
    """
    reproduce los calculos de la hoja 2000land50 del excel
    C4 es un valor de distancia
    """
    def Calcula_2000land50(self, C4):
        # Validado: 13 feb 2014 
        A4 = Calculos.Log10(C4)
        D4 = (2.7625*A4**6)-(27.277*A4**5)+(93.259*A4**4)-(133.51*A4**3)+(72.312*A4**2)-(54.74*A4)+(94.434)
        E4 = (1.9611*A4**6)-(21.366*A4**5)+(79.701*A4**4)-(125.59*A4**3)+(74.607*A4**2)-(51.745*A4)+(96.733)
        F4 = (1.1181*A4**6)-(15.104*A4**5)+(65.367*A4**4)-(118.46*A4**3)+(81.535*A4**2)-(52.746*A4)+(98.957)
        G4 = (-0.3133*A4**6)-(3.423*A4**5)+(32.685*A4**4)-(84.003*A4**3)+(72.087*A4**2)-(51.079*A4)+(101.55)
        H4 = (-2.4831*A4**6)+(15.642*A4**5)-(27.791*A4**4)-(1.5331*A4**3)+(26.077*A4**2)-(39.829*A4)+(103.93)
        I4 = (-5.3998*A4**6)+(42.629*A4**5)-(119.79*A4**4)+(138.37*A4**3)-(66.228*A4**2)-(15.158*A4)+(105.53)
        J4 = (-8.9098*A4**6)+(77*A4**5)-(244.86*A4**4)+(343.75*A4**3)-(213.56*A4**2)+(24.992*A4)+(105.99)
        K4 = (-11.043*A4**6)+(102.59*A4**5)-(355.75*A4**4)+(556.35*A4**3)-(388.01*A4**2)+(76.047*A4)+(105.38)
        L4 = (-0.00000004*A4**6)+(0.0000003*A4**5)-(0.0000007*A4**4)+(0.0000007*A4**3)-(0.00000008*A4**2)-(20*A4)+(106.9)
        lista1 = [10,20,37.5,75,150,300,600,1200,0]
        lista2 = [D4,E4,F4,G4,H4,I4,J4,K4,L4]
        return [lista1, lista2]
