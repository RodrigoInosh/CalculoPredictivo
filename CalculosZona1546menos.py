# -*- coding: iso-8859-15 -*-
'''
Created on 12-02-2014

@author: CRodriguez
'''
import math
import OtrosCalculos as Calculos

class CalculosZona1546menos():

    params = 0   # Objeto: ParametrosFormulario
    tablas = 0   # Objeto: TablaValores

    def __init__(self, params, tablas):
        self.params = params
        self.tablas = tablas
        
    def Inicio_1546menos(self, radiales):
        arrayZSRec1546menos = []
        for k in range(0,radiales):
            extension = self.Calcula_Distancia_1546menos(k*360/radiales)
            #Se agrega restriccion solo para tv
            if (extension > 1):
                arrayZSRec1546menos.append( extension )
            else:
                arrayZSRec1546menos.append( 1 )
            #print "{}:{}".format(k*20,extension)
        
        print "listo"
        return arrayZSRec1546menos
        
    #revisar: degRadial hay multiplicacion y division por 20
    def Calcula_Distancia_1546menos(self, degRadial):
        E = self.params.intensidadCampoReferencia
        F = self.params.frecuencia
        if (F < 600):
            Finf = 100
            Fsup = 600
        else:
            Finf = 600
            Fsup = 2000
            
        #Pi = 3.14159265358979
        d0 = 0
        d = 0
        Ec = 106.9
        salto = round(self.params.resolucionCalculo/500, 2)
        sombra = round(self.params.toleranciaZonasSombra, 2)
        key = 0
        cotaLim = 100 * salto
        theta1 = 0
        saltoangular = 360 / self.params.radiales
        #pt = param.porcentajeTiempo
        pl = self.params.porcentajeUbicacion
        
        while (key <= 2*sombra):
            Ec0 = Ec
            d = d + (0.5 * salto)           
            #Calculo de altura efectiva en funcion del trayecto
            h1 = self.tablas.tablaCotas_Valores['h1'][degRadial/saltoangular]
            him = self.tablas.tablaCotas_Valores['him'][degRadial/saltoangular]
            
            if (d <= 15):
                himd = self.tablas.tablaCotas_him[degRadial/saltoangular][int((d/salto)*2)] #validar conmutabilidad
            else:
                himd = him
            
            h1d = h1 + him - himd
            
            if (h1d >= 10):
                Eh1inf = self.Campo_1546(d, h1d, Finf)
                Eh1sup = self.Campo_1546(d, h1d, Fsup)
            else:
                E10inf = self.Campo_1546(d, 10, Finf)
                E20inf = self.Campo_1546(d, 20, Finf)
                E10sup = self.Campo_1546(d, 10, Fsup)
                E20sup = self.Campo_1546(d, 20, Fsup)
                v1 = ((1.35 * math.atan(1/900))-0.1)
                Ezeroa = Calculos.Log10(math.sqrt(v1**2 + 1) + v1)
                Ezeroinf = E10inf + 0.5 * (E10inf - E20inf + (6.03 - (6.9 + 20 * Ezeroa)))
                Ezerosup = E10sup + 0.5 * (E10sup - E20sup + (6.03 - (6.9 + 20 * Ezeroa)))
                
                if (h1d >= 0):
                    Eh1inf = Ezeroinf + 0.1 * h1d * (E10inf - Ezeroinf)
                    Eh1sup = Ezerosup + 0.1 * h1d * (E10sup - Ezerosup)
                else:
                    theta1 = self.tablas.tablaCotas_ADT_Maximos[degRadial/saltoangular]
                    v1 = ((0.036 * math.sqrt(Finf)) - 0.1)
                    Eh1ainf = Calculos.Log10(math.sqrt((v1**2) + 1) + v1)
                    #Eh1ainf = Log10(Sqr((((0.036 * Sqr(Finf)) - 0.1) ^ 2) + 1) + (0.036 * Sqr(Finf)) - 0.1)
                    
                    v2 = ((0.065 * theta1 * math.sqrt(Finf)) - 0.1)
                    Eh1binf =Calculos.Log10(math.sqrt((v2**2) + 1) + v2)
                    #Eh1binf = Log10(Sqr((((0.065 * theta1 * Sqr(Finf)) - 0.1) ^ 2) + 1) + (0.065 * theta1 * Sqr(Finf)) - 0.1)
                    
                    v3 = ((0.036 * math.sqrt(Fsup)) - 0.1)
                    Eh1asup = Calculos.Log10(math.sqrt((v3 ** 2) + 1) + v3)
                    #Eh1asup = Log10(Sqr((((0.036 * Sqr(Fsup)) - 0.1) ^ 2) + 1) + (0.036 * Sqr(Fsup)) - 0.1)
                    
                    v4 = (0.065 * theta1 * math.sqrt(Fsup)) - 0.1
                    Eh1bsup = Calculos.Log10(math.sqrt((v4**2) + 1) + v4)
                    #Eh1bsup = Log10(Sqr((((0.065 * theta1 * Sqr(Fsup)) - 0.1) ^ 2) + 1) + (0.065 * theta1 * Sqr(Fsup)) - 0.1)
            
                    Eh1inf = Ezeroinf + (6.9 + 20 * Eh1ainf) - (6.9 + 20 * Eh1binf)
                    Eh1sup = Ezerosup + (6.9 + 20 * Eh1asup) - (6.9 + 20 * Eh1bsup)
            
            #Interpolacion por Frecuencia
            Eh1 = Eh1inf + (Eh1sup - Eh1inf) * Calculos.Log10(F / Finf) / Calculos.Log10(Fsup / Finf)
            Emax = 106.9 - 20 * Calculos.Log10(d)
            if (Eh1 > Emax):
                Eh1 = Emax
              
            #Factor de correccion de potencia
            P = self.params.potencia
            G = self.params.ganancia
            PC = self.params.perdidaCablesConectores + self.params.perdidaDivisorPotencia + self.params.otrasPerdidas
            #Plob = Sheets("Inicio").Cells(55, 3 + ((degRadial / 10) / 2)).Value
            Plob = self.params.perdidasLobulo[degRadial/saltoangular]
            
            Fcp = 10 * Calculos.Log10(P) + G - (PC + Plob)
            
            # limite de potencia radiada RESTRICCION OJO
            if Fcp < -45:
                Fcp = -45
            
            #Factor de correccion altura antena receptora
            R = self.params.obstaculosCircundantesRx
            if (h1d > 6.5 * d + R):
                Rcd = (1000 * d * R - 15 * h1d) / (1000 * d - 15)
            else:
                Rcd = R
            
            h2 = self.params.alturaAntenaReceptora
            if (h2 >= Rcd):
                FcR = (3.2 + 6.2 * Calculos.Log10(F)) * Calculos.Log10(h2 / Rcd)
            else:
                va1 = math.atan(float(20 - h2) / 27)
                va2 = math.atan(float(Rcd - h2) / 27)
                vv1 = (0.0108 * math.sqrt(F) * math.sqrt((Rcd - h2) * va1))
                vv2 = (0.0108 * math.sqrt(F) * math.sqrt((Rcd - h2) * va2))
                FcR = (6.03 - (6.9 + 20 * Calculos.Log10(math.sqrt(((vv1 - 0.1)**2) + 1) + vv2 - 0.1)))
                #FcR = (6.03 - (6.9 + 20 * Calculos.Log10(math.sqrt((((0.0108 * math.sqrt(F) * math.sqrt((Rcd - h2) * math.atan((20 - h2) / 27))) - 0.1) ** 2) + 1) + (0.0108 * math.sqrt(F) * math.sqrt((Rcd - h2) * math.atan((Rcd - h2) / 27))) - 0.1)))
            
            #Factor de correccion trayectos urbanos
            h1s = self.params.alturaAntenaTransmisora
            if (d <= 15):
                if ((h1d > 10) and ((h1d - Rcd) < 150)):
                    if ((1 + h1s - Rcd) < 0):
                        FcU = 0
                    else:
                        FcU = -3.3 * Calculos.Log10(F) * (1 - 0.85 * Calculos.Log10(d)) * (1 - 0.46 * Calculos.Log10(1 + h1s - Rcd))
                else:
                    FcU = 0
            else:
                FcU = 0
    
            #Factor de correccion angulo antena receptora
            if (d <= cotaLim):     #Limite de cotas
                #h2s = Sheets("RD41").Cells(5 + d / salto * 2, 23 + ((degRadial / 10) / 2)).Value + h2
                h2s = self.tablas.Matriz_Cotas(degRadial/saltoangular, d/salto*2) + h2
                theta2 = self.Angulo_Receptor(d, degRadial, h2)
            else:
                #h2s = Sheets("RD41").Cells(5 + cotaLim / salto * 2, 23 + ((degRadial / 10) / 2)).Value + h2
                h2s = self.tablas.Matriz_Cotas(degRadial/saltoangular, cotaLim/salto*2) + h2
                theta2 = self.Angulo_Receptor(cotaLim, degRadial, h2)
            
            thetar = math.atan((self.tablas.Matriz_Cotas(0,0) + h1s - h2s) / (1000*d))
            
            if ((theta2 - thetar) < 40):
                if ((theta2 - thetar) <= 0.55):
                    tca = 0
                else:
                    tca = (theta2 - thetar)
            else:
                tca = 40
            
            if (tca == 0):
                FcAR = 0
            else:
                if (h1d < 0):
                    tca = theta1
                v5 = ((0.036 * math.sqrt(F)) - 0.1)
                FcARa = Calculos.Log10(math.sqrt((v5 ** 2) + 1) + v5)
                v6 = ((0.065 * tca * math.sqrt(F)) - 0.1)
                FcARb = Calculos.Log10(math.sqrt((v6 ** 2) + 1) + v6)
                FcAR = (6.9 + 20 * FcARa) - (6.9 + 20 * FcARb)
    
            Ec = Eh1 + Fcp + FcR + FcU + FcAR
    
            #Variabilidad segun las predicciones de cobertura terrestre zonal
            if (pl > 50):
                #sigmaloc = 1.2 + 1.3 * Calculos.Log10(F)
                #1.2 antenas Rx urbanas por debajo del obstaculo
                #1.0 antenas Rx urbanas cerca del obstaculo
                #0.5 antenas Rx rural
                #Ec = Ec + Calculos.Log_Normal(pl/100) * sigmaloc
                #Correcion -7 solo para calculos tv digitales
                if (F > 300): #Rango digital entre 512 MHz al 698 Mhz
                    Ec = Ec - 7 #7.0 digital/ 10.6 analogo<300/ 12.2 analogo>300
                else: #Rango analogo entre 54 MHz y 216 MHz
                    #if (F <= 300):
                    Ec = Ec - 10.6
                    #else:
                    #    Ec = Ec - 12.2
                    
            if (Ec > E):
                key = 0
            else:
                if (key == 0):
                    if (d < 1 * salto):
                        #dnf = (10 ^ (0.1 * (G - 2.15))) / (10 * F)
                        #d0 = (10 ^ ((110.9 + Fcp) / 40)) / 100
                        E01 = 106.9 - 20 * Calculos.Log10(0.1)
                        E1 = self.Campo_1546(1, h1d, Finf)
                        d0 = (0.1 * 10 ** ((Ec - E01) / (E1 - E01))) / 100
                    else:
                        d0 = (d - 0.5 * salto) * 10 ** ((Calculos.Log10(d / (d - 0.5 * salto))) * (E - Ec) / (Ec0 - Ec))
                #arcpy.AddMessage(Ec) #prueba
                key = key + 1
            if (d >= (200*salto)):
                d0 = d
                key = 2*sombra + 1
        return d0

       
    # Calcula la intensidad de campo que se obtiene a la distancia d de la estacion
    def Campo_1546(self, distancia, altura, frecuencia):
        #Esup = Land50[1][0] #Cells(4, 4).Value
        #Einf = Land50[1][0] #Cells(4, 4).Value
        #hsup = Land50[0][0] #Cells(3, 4).Value
        #hinf = Land50[0][0] #Cells(3, 4).Value
        
        #Calcula indice sup e inf segun h1d
        if (altura < 10): 
            sup = 2
            inf = 1
        elif ((altura >= 10) and (altura < 20)):
            sup = 2
            inf = 1
        elif ((altura >= 20) and (altura < 37.5)):
            sup = 3
            inf = 2
        elif ((altura >= 37.5) and (altura < 75)):
            sup = 4
            inf = 3
        elif ((altura >= 75) and (altura < 150)):
            sup = 5
            inf = 4
        elif ((altura >= 150) and (altura < 300)):
            sup = 6
            inf = 5
        elif ((altura >= 300) and (altura < 600)):
            sup = 7
            inf = 6
        elif ((altura >= 600) and (altura <= 1200)):
            sup = 8
            inf = 7
        elif (altura > 1200):
            sup = 9
            inf = 8
        
        #se puede mejorar usando diccionarios
        if (frecuencia==100):
            Land50 = self.tablas.Calcula_100land50(1)
        elif (frecuencia == 600):
            Land50 = self.tablas.Calcula_600land50(1)
        elif (frecuencia==2000):
            Land50 = self.tablas.Calcula_2000land50(1)
            
        Esup1 = Land50[1][sup-1] # Cells(4, 3 + sup).Value
        Einf1 = Land50[1][inf-1] # Cells(4, 3 + inf).Value
        
        #se puede mejorar usando diccionarios
        if (frecuencia==100):
            Land50 = self.tablas.Calcula_100land50(distancia)
        elif (frecuencia==600):
            Land50 = self.tablas.Calcula_600land50(distancia)
        elif frecuencia==2000:
            Land50 = self.tablas.Calcula_2000land50(distancia)
            
        Esup = Land50[1][sup-1] #Cells(4, 3 + sup).Value
        Einf = Land50[1][inf-1] #Cells(4, 3 + inf).Value
        hsup = Land50[0][sup-1] #Cells(3, 3 + sup).Value
        hinf = Land50[0][inf-1] #Cells(3, 3 + inf).Value
        
        Es = Einf + (Esup-Einf) * Calculos.Log10(altura/hinf) / Calculos.Log10(hsup/hinf)
        Ed = 106.9 - 20 * Calculos.Log10(distancia)
        Ednf = 106.9 - 20 * Calculos.Log10(0.01)
        Emin = 106.9 - 20 * Calculos.Log10(0.1)
        Emax = Einf1 + (Esup1-Einf1) * Calculos.Log10(altura/hinf) / Calculos.Log10(hsup/hinf)
        
        if (distancia <= 0.01):
            resultado = Ednf
        elif ((distancia > 0.01) and (distancia <= 0.1)):
            resultado = Ed
        elif ((distancia > 0.1) and (distancia < 1)):
            resultado = Emin + (Emax - Emin) * Calculos.Log10(distancia / 0.1)
        elif ((distancia >= 1) and (Es >= Ed)):
            resultado = Ed
        elif ((distancia >= 1) and (Es < Ed)):
            resultado = Es
        
        return resultado
  

    def Angulo_Receptor(self, distancia, radial, altura):
        ARmax = -180
        Pi = 3.14159265358979
        salto = round(self.params.resolucionCalculo/500, 2)
        saltoangular = 360 / self.params.radiales
        if(distancia>=16):
            dx = 16
        else:
            dx = distancia
            
        s = distancia - dx
        while (s <= distancia):
            ha = self.tablas.Matriz_Cotas(radial/saltoangular, (distancia/salto*2))
            hb = self.tablas.Matriz_Cotas(radial/saltoangular, (s/salto*2))
            
            AR = (180/Pi) * Calculos.ArcTan((hb-ha-altura)/1000, distancia-s)
            
            if ((AR > ARmax) and (dx != 0)):
                ARmax = AR
            
            s = s + (salto * 0.5)
            
        return ARmax
