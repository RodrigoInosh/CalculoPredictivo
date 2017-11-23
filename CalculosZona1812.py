# -*- coding: iso-8859-15 -*-
'''
Created on 16/10/2017

@author: Kimie Cortes
'''
import math
import OtrosCalculos as Calculos
#import arcpy

class CalculosZona1812():

    params = 0   # Objeto: ParametrosFormulario
    tablas = 0   # Objeto: TablaValores
    hsr = [0] * 18
    m = [0] * 18
    dlt = [0] * 18   #dlt es el unico que se esta utilizando fuera de la clase
    dlr = [0] * 18
    dim50 = [0] * 18
    
    def __init__(self, params, tablas):
        self.params = params
        self.tablas = tablas
           
    def Inicio_1812(self, radiales):
        #Calculo predictivo segun Rec 1812 para x radiales
        arrayZSRec1812 = []
        for k in range(0,radiales):
            extension = self.Calcula_Distancia_1812(k*360/radiales)
            arrayZSRec1812.append( extension )
            #print "{}:{}".format(k*20,extension)
        
        print "listo"
        return arrayZSRec1812


    def Calcula_Distancia_1812(self, degRadial):
        E = self.params.intensidadCampoReferencia
        F = self.params.frecuencia / 1000
        d0 = 0  # se asigna por defecto
        Pi = 3.14159265358979
        d = 0 #Distancia_1812(E, s, numCurva)
        Ec = 106.9 #Campo_1812(d, h1d, numCurva)
        salto = round(self.params.resolucionCalculo/500, 2)
        sombra = round(self.params.toleranciaZonasSombra, 2)
        key = 0
        cotaLim = 100 * salto
        saltoangular = 360 / self.params.radiales
        # estas variables se ocupan mas adelante pero no se les asigno un valor
        # por defecto al ser definidas en VB su valor es 0, se replica este comportamiento
        thetaprimat = 0  
        thetaprimar = 0
        
        Rt = self.params.obstaculosCircundantesTx #Rt = Sheets("Inicio").Cells(12, 19).Value
        Rr = self.params.obstaculosCircundantesRx #Rr = Sheets("Inicio").Cells(15, 19).Value
        pt = self.params.porcentajeTiempo         #pt = Sheets("Inicio").Cells(44, 19).Value
        pl = self.params.porcentajeUbicacion      #pl = Sheets("Inicio").Cells(45, 19).Value
        
        #Clasificacion del trayecto
        Nzero = 320   #refractividad a nivel del mar medida en el punto central del trayecto
        deltaN = 45   #gradiente refractividad radioelectrica
        k50 = float(157) / float(157 - deltaN)   #factor radio efectivo de la Tierra
        ae = 6371 * k50   #radio efectivo de la Tierra
        #kbeta = 3   #factor radio efectivo de la Tierra tiempo beta
        #abeta = 6371 * kbeta   #radio efectivo de la Tierra tiempo beta
        
        while (key <= 2*sombra):
            Ec0 = Ec
            d = d + (0.5 * salto)
          
            #Deduccion de parametros a partir del perfil del proyecto
            if (d <= cotaLim):     #Limite de cotas
                ha = self.Altura_Promedio(d, degRadial)    #promedio de alturas del trayecto
                m = self.Pendiente_Superficie(d, degRadial, ha)    #pendiente de la superficie
            else:
                ha = self.Altura_Promedio(cotaLim, degRadial)    #promedio de alturas del trayecto
                m = self.Pendiente_Superficie(cotaLim, degRadial, ha)    #pendiente de la superficie
            
            hst = ha - m * (d / 2)    #altura superficie tierra lisa antena Tx
            hsr = hst + m * d    #altura superficie tierra lisa antena Rx
            if (d <= cotaLim):     #Limite de cotas
                #hgr = Sheets("RD41").Cells(5 + d / salto * 2, 23 + ((degRadial / 10) / 2)).Value
                hgr = self.tablas.Matriz_Cotas(degRadial/5, (d/salto*2))
            else:
                hgr = hst + m * d
                #hgr = Sheets("RD41").Cells(5 + cotaLim * 2, 23 + ((degRadial / 10) / 2)).Value  'Mantiene la misma cota despues de 50 o 100 km?
                #Sheets("RD41").Cells(213, 23 + ((degRadial / 10) / 2)).FormulaR1C1 = hsr
                #Sheets("RD41").Cells(214, 23 + ((degRadial / 10) / 2)).FormulaR1C1 = m
        
            h1 = self.tablas.Matriz_Cotas(0,0)
            hn = hgr
            g1 = h1 + Rt
            gn = hn + Rr
            if (hst > h1):
                hst = h1
            
            if (hsr > hn):
                hsr = hn
            
            m = (hsr - hst) / d
            self.hsr[degRadial/saltoangular] = hsr
            self.m[degRadial/saltoangular] = m
            #Sheets("RD41").Cells(213, 23 + ((degRadial / 10) / 2)).FormulaR1C1 = hsr
            #Sheets("RD41").Cells(214, 23 + ((degRadial / 10) / 2)).FormulaR1C1 = m
            hgt = self.tablas.Matriz_Cotas(0,0)
            htg = self.params.alturaAntenaTransmisora
            #hgt = Sheets("RD41").Cells(206, 43 + ((degRadial / 10) / 2)).Value
            #htg = Sheets("RD41").Cells(207, 43 + ((degRadial / 10) / 2)).Value
            hts = hgt + htg    #altura antena Tx sobre el nivel del mar
            hrg = self.params.alturaAntenaReceptora
            #hrg = Sheets("Inicio").Cells(14, 19).Value
            hrs = hgr + hrg    #altura antena Rx sobre el nivel del mar
            
            thetatd = (hrs - hts) / d - (1000 * d) / (2 * ae)
            thetatmax = self.Angulo_Tx(d, degRadial, hts, ae, hsr, m)
            thetarmax = self.Angulo_Rx(d, degRadial, hrs, ae, hsr, m)
        
            if (thetatd >= thetatmax):
                thetat = thetatd
                if (thetatd == thetarmax):
                    thetar = (hts - hrs) / d - (1000 * d) / (2 * ae)
                else:
                    thetar = thetarmax
            else:
                thetat = thetatmax
                thetar = thetarmax
                    
            htc = Calculos.Max(hts, g1)   #altura antena Tx sobre el nivel del mar
            hrc = Calculos.Max(hrs, gn)   #altura antena Rx sobre el nivel del mar
            Ld50 = self.Arista_Principal(d, degRadial, htc, hrc, ae, hsr, m)  #perdidas de arista curvatura de la Tierra
            if (thetat == 0):
                dlt = self.dim50[degRadial/saltoangular]
                #dlt = Sheets("RD41").Cells(212, 23 + ((degRadial / 10) / 2)).Value
            else:
                dlt = self.dlt[degRadial/saltoangular]
                #dlt = Sheets("RD41").Cells(210, 23 + ((degRadial / 10) / 2)).Value   #distancia antena Tx a su horizonte
            
            if (thetat == thetatd):
                dlr = d - self.dim50[degRadial/saltoangular]
                #dlr = d - Sheets("RD41").Cells(212, 23 + ((degRadial / 10) / 2)).Value
            else:
                dlr = self.dlr[degRadial/saltoangular]
                #dlr = Sheets("RD41").Cells(211, 23 + ((degRadial / 10) / 2)).Value   #distancia antena Rx a su horizonte
            
            hte = h1 + htg - hst    #'altura efectiva de la antena Tx
            hre = hn + hrg - hsr    #altura efectiva de la antena Rx
            hm = self.Rugosidad_Terreno(degRadial, m, hst, dlt, d - dlr)   #rugosidad del terreno
                
            #Factor de correccion de potencia
            P = self.params.potencia
            G = self.params.ganancia
            PC = self.params.perdidaCablesConectores + self.params.perdidaDivisorPotencia + self.params.otrasPerdidas
            Plob = self.params.perdidasLobulo[degRadial/saltoangular]
            Fcp = 10 * Calculos.Log10(P) + G - (PC + Plob)
            
            # limite de potencia radiada
            if Fcp < -45:
                Fcp = -45
                  
            #Propagacion con visibilidad directa (incluido efectos a corto plazo)
            tau = 1 - math.exp(-(4.12 * 10**-4) * d**2.41)
            phi = round(self.params.latitud, 0)
            #phi = Sheets("Inicio").Cells(44, 14).Value
            u1 = (10 ** (-d / (16 - 6.6 * tau)) + 10 ** (-5 * (0.496 + 0.354 * tau))) ** 0.2
            if (phi <= 70):
                u4 = u1 ** (-0.935 + 0.0176 * abs(phi))
                betazero = u1 * u4 * 10 ** (-0.015 * abs(phi) + 1.67)   #porcentaje tiempo de propagacion
            else:
                u4 = u1 ** 0.3
                betazero = u1 * u4 * 4.17
            
            Lbfs = 92.44 + 20 * Calculos.Log10(F) + 20 * Calculos.Log10(d) #Perdidas basicas propagacion espacio libre
            Esp = 2.6 * (1 - math.exp(-(dlt+dlr) / 10)) * Calculos.Log10(pt/50)  #correccion multitrayecto para pt%
            Esbeta = 2.6 * (1 - math.exp(-(dlt+dlr) / 10)) * Calculos.Log10(betazero/50)  #correccion multitrayecto para betazero%
            Lb0p = Lbfs + Esp   #perdidas basicas propagacion para pt%
            Lb0beta = Lbfs + Esbeta  #perdidas basicas propagacion para betazero%
            
            #Propagacion por difraccion
            Ldbeta = 0  #Lmbeta + (1 - Exp(-Lmbeta / 6)) * (Ltbeta + Lrbeta + 10 + 0.04 * d) PENDIENTE pt<>50%
            if (pt <= 50):
                if (pt == 50):
                    Fi = 0    #factor de interpolacion i
                else:
                    if (betazero >= pt):
                        Fi = 1
                    else:
                        Fi = Calculos.Log_Normal(pt/100) / Calculos.Log_Normal(betazero/100)
            
            Ldp = Ld50 + (Ldbeta - Ld50) * Fi #perdidas difraccion pt% del tiempo
            Lbd = Lb0p + Ldp  #Perdidas de transmision basicas correspondientes a la difraccion no rebasadas durante el pt% del tiempo
        
            #Propagacion por dispersion troposferica
            theta = 1 * 10**3 * d / ae + thetat + thetar   #distancia angular del trayecto
            Lf = 25 * Calculos.Log10(F) - 2.5 * (Calculos.Log10(F / 2)) ** 2 #perdidas dependientes de la frecuencia
            Lbs = 190.1 + Lf + 20*Calculos.Log10(d) + 0.573 * theta - 0.15*Nzero - 10.125 * (Calculos.Log10(50/pt))**0.7 #Perdidas de transmision basicas debidas a la dispersion troposferica
        
            #'Propagacion por conductos y por reflexion en capas
            thetadobleprimat = thetat - 0.1 * dlt
            thetadobleprimar = thetar - 0.1 * dlr
            if (thetadobleprimat > 0):
                Ast = 20 * Calculos.Log10(1 + 0.361*thetadobleprimat*(F*dlt)**(float(1)/2)) + 0.264*thetaprimat*(F)**(1/3)  #perdidas difraccion apantallamiento Tx
            else:
                Ast = 0
            
            if (thetadobleprimar > 0):
                Asr = 20 * Calculos.Log10(1 + 0.361*thetadobleprimar*(F*dlr)**(float(1)/2)) + 0.264*thetaprimar*(F)**(1/3)  #perdidas difraccion apantallamiento Rx
            else:
                Asr = 0
            
            if (abs(dlt - dlr) > 0):
                # REVISAR: en formula original se ocupa Log en vez de Log10
                Af = 102.45 + 20*Calculos.Log10(F) + 20*math.log(dlt+dlr) + Ast + Asr #+ Act + Acr    'perdidas fijas de acoplamiento
                #Af = 102.45 + 20 * Log10(F) + 20 * Log(dlt + dlr) + Ast + Asr
            else:
                Af = 0
            
            if (thetat <= 0.1 * dlt):
                thetaprimat = thetat
            else:
                thetaprimat = 0.1 * dlt
            
            if (thetar <= 0.1 * dlr):
                thetaprimar = thetar
            else:
                thetaprimar = 0.1 * dlr
            
            thetaprima = (1 * 10**3 * d) / ae + thetaprimat + thetaprimar  #distancia angular corregida
            gammad = 5 * 10**-5 * ae * F**(float(1)/3) #atenuacion especifica
            duno = Calculos.Min(d-dlt-dlr, 40)
            epsilon = 3.5
            alpha = -0.6 - epsilon * (10**-9) * (d**3.1) * tau
            u2 = ((500 / ae) * ((d**2) / ((math.sqrt(hte/1000) + math.sqrt(hre/1000))**2)))**alpha    #correccion geometria del trayecto
            if (hm <= 10):
                u3 = 1
            else:
                u3 = math.exp(-4.6 * 10**-5 * (hm - 10) * (43 + 6 * duno))    #'correccion rugosidad del terreno
            
            beta = betazero * u2 * u3
            gammamay = (1.076 / abs(2.0058-Calculos.Log10(beta))**1.012) * math.exp(-(9.51 - 4.8*Calculos.Log10(beta) + 0.198 * (Calculos.Log10(beta))**2) * (10**-6) * (d**(1/3)))
            Ap = -12 + (1.2 + 3.7 * (10**-3) * d) * Calculos.Log10(pt/beta) + 12 * (pt/beta)**gammamay    #'variabilidad del porcentaje de tiempo
            #try:
            #    div0 = pt/beta
            #except:
            #    div0 = 0 # valor opcional para el resultado de la division
            #arcpy.AddMessage("d:{}; hte:{}; hre:{}; alpha:{}".format(d, hte, hre, alpha))
          
            #Ap = -12 + (1.2 + 3.7 * (10**-3) * d) * Calculos.Log10(div0) + 12 * (div0)**gammamay    #'variabilidad del porcentaje de tiempo

            Adp = gammad * thetaprima + Ap   #perdidas de la distancia angular
            Lba = Af + Adp    #Perdidas de transmision basicas debidas a la propagacion por conductos y por reflexion en capas no rebasadas durante el p% del tiempo
        
            #Perdidas de transmision basicas, no rebasadas durante el porcentaje de tiempo anual p%, para el 50% de las ubicaciones, ignorando los efectos de la ocupacion del suelo
            eta = 2.5
            #NOTA: se estaba usando Log en vez de Log10
            Lminbap = eta * math.log(math.exp(float(Lba)/eta) + math.exp(float(Lb0p)/eta))   #perdidas basicas minimas transhorizonte
            
            #pru1 = float(Lba)/eta
            #pru2 = float(Lb0p)/eta
            #pru3 = math.exp(pru1)
            #try:
            #    pru3 = math.exp(pru1)
            #except:
            #    arcpy.AddMessage("Lba: {}; eta: {}; pru1: {}".format(Lba, eta, pru1))
            #pru4 = math.exp(pru2)
            #pru5 = pru3 + pru4
            #Lminbap = eta * pru5

            xi = 0.8   #pendiente al final de la gama
            thetamay = 0.3   #gama de angulos
            Fj = 1 - 0.5 * (1 + math.atan(3 * xi * ((theta-thetamay) / thetamay)))   #factor de interpolacion j
            dsw = 20    #gama de distancias
            kappa = 0.5    #pendiente a los extremos gama
            Fk = 1 - 0.5 * (1 + Calculos.TanH(3 * kappa * (float(d-dsw)/dsw)))    #factor de interpolacion k
            if (Lminbap > Lbd):
                Lbda = Lbd
            else:
                Lbda = Lminbap + (Lbd - Lminbap) * Fk   #perdidas basicas minimas reflexion
            
            omega = 0    #para trayectos realizados totalmente sobre tierra
            Lbd50 = Lbfs + Ld50 #valor mediano perdidas de difraccion
            if (pt > betazero):
                Lminb0p = Lb0p + (1-omega) * Ldp   #perdidas basicas minimas difraccion
            else:
                Lminb0p = Lbd50 + (Lb0beta + (1-omega) * Ldp - Lbd50) * Fi
            
            Lbam = Lbda + (Lminb0p - Lbda) * Fj    #perdidas basicas minimas modificadas
            Lbu = -5 * Calculos.Log10(10**(-0.2*Lbs) + 10**(-0.2*Lbam))
            
            #Perdidas de transmision basicas, no rebasadas durante el porcentaje de tiempo anual p%, para el 50% de las ubicaciones, incluidos los efectos de la ocupacion del suelo
            Knu = 0.342 * math.sqrt(F)
            Kh2 = 21.8 + 6.2 * Calculos.Log10(F)
            
            hdift = Rt - htg
            thetaclut = (180 / Pi) * math.atan(float(hdift)/27) #cambio08
            vt = Knu * math.sqrt(abs(hdift*thetaclut))
            if (htg < Rt):
                if (Rt == 10):
                    Aht = -Kh2 * Calculos.Log10(htg / Rt)
                else:
                    Aht = Calculos.Jota(vt) - 6.03
            else:
                Aht = 0
            
            hdifr = Rr - hrg
            thetaclur = (180 / Pi) * math.atan(float(hdifr)/27) #cambio09
            vr = Knu * math.sqrt(abs(hdifr*thetaclur))
            if (hrg < Rr):
                if (Rr == 10):
                    Ahr = -Kh2 * Calculos.Log10(float(hrg)/Rr)
                else:
                    Ahr = Calculos.Jota(vr) - 6.03
            else:
                Ahr = 0
            
            Lbc = Lbu + Aht + Ahr
            
            #Perdidas de transmision basicas, no rebasadas durante el porcentaje de tiempo anual p%, para el pl% de las ubicaciones, incluidos los efectos de la ocupacion del suelo
            Lbe = 9
            sigmabe = 3
            sigmal = 8.3
            sigmai = math.sqrt((sigmal)**2 + (sigmabe)**2)   #variacion intensidad de campo recepcion interiores
            #If exteriores Then  'En principio se asume recepcion en interiores
            #    'Lloc = 0
            #Else
            Lloc = Lbe
            #End If
            #If exteriores Then
            #    'sigmaloc = sigmaluh
            #Else
            sigmaloc = sigmai
            #End If
            
            Lb = Calculos.Max(Lb0p, Lbc + Lloc - Calculos.Log_Normal(float(pl)/100) * sigmaloc)
             
            #Intensidad de campo normalizada a 1 kW de potencia radiada aparente rebasada durante el p% del tiempo en el 50% de las ubicaciones
            Ep = 199.36 + 20 * Calculos.Log10(F) - Lb
            Ec = Ep + Fcp #'+ FcR + FcU + FcAR  'Ep en vez de Eh1 y las otras correcciones ya estan consideradas
                
            #'Registra campo a distancia d
            #    'array_Ec1812((d / salto * 2) - 1, (degRadial / 10) / 2) = Ec
            #    'j = Sheets("RD43").Cells(6, 26).Value
            #    'If (j = 1) Then
            #        'Sheets("RD43").Activate
            #        'Range("AS9").Select
            #        'ActiveCell.Offset(d / salto * 2, (degRadial / 10) / 2).Select
            #        'ActiveCell.FormulaR1C1 = Ec
            #        'Sheets("RD41").Activate
            #    'End If
 
            if (Ec > E):
                key = 0
            else:
                if (key == 0) and (d > 0.5*salto):
                    d0 = (d - 0.5*salto) * 10 ** ((Calculos.Log10(d / (d - 0.5*salto))) * (E-Ec) / (Ec0-Ec))
                key = key + 1
            if (d >= (200*salto)):
                d0 = d
                key = 2*sombra + 1
        #Wend
        #arcpy.AddMessage("d0:{}; sombra:{}".format(d0, sombra))
        return d0
    
        
    def Altura_Promedio(self, distancia, radial):
        hsuma = self.tablas.Matriz_Cotas(0,0)
        salto = round(self.params.resolucionCalculo/500, 2)
        s = 0.5 * salto
        saltoangular = 360 / self.params.radiales
        while (s <= distancia):            
            hi = self.tablas.Matriz_Cotas(radial/saltoangular, (s/salto*2)) #hi = Sheets("RD41").Cells(5 + s / salto * 2, 23 + ((radial / 10) / 2)).Value
            hsuma = hsuma + hi
            s = s + (salto * 0.5)
        #for s = 0.5 * salto To distancia Step 0.5 * salto
        #    hi = Sheets("RD41").Cells(5 + s / salto * 2, 23 + ((radial / 10) / 2)).Value
        #    hsuma = hsuma + hi
        #Next
        return (1 / (distancia*2)) * hsuma  #promedio de alturas del trayecto        
        

    def Pendiente_Superficie(self, distancia, radial, promedio):
        h0 = self.tablas.Matriz_Cotas(0,0)
        mnum = (h0 - promedio) * (0 - distancia / 2)
        mden = (0 - distancia / 2) ** 2
        salto = round(self.params.resolucionCalculo/500, 2)
        s = 0.5 * salto
        saltoangular = 360 / self.params.radiales
        while (s <= distancia):
            hi = self.tablas.Matriz_Cotas(radial/saltoangular, (s/salto*2))
            mnum = mnum + (hi - promedio) * (s - distancia / 2)
            mden = mden + (s - distancia / 2) ** 2
            s = s + (salto * 0.5)
        #For s = 0.5 * salto To distancia Step 0.5 * salto
        #    hi = Sheets("RD41").Cells(5 + s / salto * 2, 23 + ((radial / 10) / 2)).Value
        #    mnum = mnum + (hi - promedio) * (s - distancia / 2)
        #    mden = mden + (s - distancia / 2) ^ 2
        #Next
        return mnum / mden  #pendiente de la superficie

    def Angulo_Tx(self, distancia, radial, alturats, radio, alturalisa, pendiente):
        #Pi = 3.14159265358979
        salto = round(self.params.resolucionCalculo/500, 2)
        cotaLim = 100 * salto
        dhorizonte = 0  # se define igual a 0, emula VB
        #delta = 0
        saltoangular = 360 / self.params.radiales
        #if (distancia > cotaLim):
        #    delta = (distancia - cotaLim)
    
        hi = self.tablas.Matriz_Cotas(radial/saltoangular, (0.5/salto*2) )
        #hi = Sheets("RD41").Cells(5 + 0.5 / salto * 2, 23 + ((radial / 10) / 2)).Value
        thetamax = (hi - alturats) / 0.5 * salto - (1000 * 0.5 * salto) / (2 * radio)
    
        if (distancia > 0.5 * salto): #'Define intervalo de despejamiento
            s = 0.5 * salto
            while (s <= (distancia-0.5*salto)):
                if (s > cotaLim):
                    hi = (alturalisa + pendiente * (s - cotaLim)) #* (distancia / cotaLim)      'altura perfil del punto a s
                else:
                    hi = self.tablas.Matriz_Cotas(radial/saltoangular, (s/salto*2))
                    #hi = Sheets("RD41").Cells(5 + s / salto * 2, 23 + ((radial / 10) / 2)).Value  #'hi = altura a distancia i
                #'hi = Sheets("RD41").Cells(5 + s/salto * 2, 23 + ((radial / 10) / 2)).Value    'hi = altura a distancia i
                ATx = (hi-alturats) / s - (1000*s) / (2*radio)
                if (ATx > thetamax):
                    thetamax = ATx
                    dhorizonte = s
           
                s = s + (salto * 0.5)
            #For s = (0.5 * salto) To (distancia - 0.5 * salto) Step 0.5 * salto
            #    If (s > cotaLim) Then
            #        hi = (alturalisa + pendiente * (s - cotaLim)) '* (distancia / cotaLim)      'altura perfil del punto a s
            #    Else
            #        hi = Sheets("RD41").Cells(5 + s / salto * 2, 23 + ((radial / 10) / 2)).Value  'hi = altura a distancia i
            #    End If
            #    'hi = Sheets("RD41").Cells(5 + s/salto * 2, 23 + ((radial / 10) / 2)).Value    'hi = altura a distancia i
            #    ATx = (hi - alturats) / s - (1000 * s) / (2 * radio)
            #    If (ATx > thetamax) Then
            #        thetamax = ATx
            #        dhorizonte = s
            #    End If
            #Next
        self.dlt[radial/saltoangular] = dhorizonte
        #Sheets("RD41").Cells(210, 23 + ((radial / 10) / 2)).FormulaR1C1 = dhorizonte
        return thetamax
            

    def Angulo_Rx(self, distancia, radial, alturars, radio, alturalisa, pendiente):
        #Pi = 3.14159265358979
        salto = round(self.params.resolucionCalculo/500, 2)
        cotaLim = 100 * salto
        dhorizonte = 0  # se define igual a 0, emula VB
        delta = 0
        saltoangular = 360 / self.params.radiales
        if (distancia > cotaLim):
            delta = (distancia - cotaLim)
        
        hj = self.tablas.Matriz_Cotas(radial/saltoangular,((distancia-delta-0.5*salto) / salto*2))
        #hj = Sheets("RD41").Cells(5 + (distancia - delta - 0.5 * salto) / salto * 2, 23 + ((radial / 10) / 2)).Value
        thetamax = (hj - alturars) / (0.5 * salto) - (1000 * (0.5 * salto)) / (2 * radio)
        
        if (distancia > 0.5 * salto): #'Define intervalo de despejamiento
            s = 0.5 * salto
            while (s <= (distancia-0.5*salto)):
                if (s > cotaLim):
                    hj = (alturalisa + pendiente * (s - cotaLim)) #'* (distancia / cotaLim)      'altura perfil del punto a s
                else:
                    hj = self.tablas.Matriz_Cotas(radial/saltoangular,(s/salto*2))
                    #hj = Sheets("RD41").Cells(5 + s / salto * 2, 23 + ((radial / 10) / 2)).Value  #'hj = altura a distancia j
                
                ARx = (hj - alturars) / (distancia - s) - (1000 * (distancia - s)) / (2 * radio)
                if (ARx >= thetamax):
                    thetamax = ARx
                    dhorizonte = s
                
                
                s = s + (salto * 0.5)
                   
        self.dlr[radial/saltoangular] = distancia - dhorizonte
        #Sheets("RD41").Cells(211, 23 + ((radial / 10) / 2)).FormulaR1C1 = distancia - dhorizonte
        
        return thetamax
            

    def Arista_Principal(self, distancia, radial, alturatc, alturarc, radio, alturalisa, pendiente):
        vm50 = -1
        vt50 = -1
        vr50 = -1
        dim50 = 0
        lambd = 0.3 / (self.params.frecuencia/1000)
        R = self.params.obstaculosCircundantesRx
        #Pi = 3.14159265358979
        salto = round(self.params.resolucionCalculo/500, 2)
        cotaLim = 100 * salto
        saltoangular = 360 / self.params.radiales
        #if (distancia >= cotaLim):
        #    delta = (distancia - cotaLim)
        
        if (distancia > 0.5*salto):
        
            zetam = math.cos(math.atan(10**-3 * (alturarc-alturatc) / distancia))  #'correccion pendiente global del trayecto
            
            s = 0.5 * salto
            while (s <= (distancia-0.5*salto)):
                if (s > cotaLim):
                    gs = (alturalisa + pendiente * (s-cotaLim)) + R #'* (distancia / cotaLim)      'altura perfil del punto a s
                else:
                    gs = self.tablas.Matriz_Cotas(radial/saltoangular, (s/salto*2)) + R
                    #gs = Sheets("RD41").Cells(5 + s / salto * 2, 23 + ((radial / 10) / 2)).Value + R
                hmi = gs + (10**3) * (s*(distancia-s) / (2*radio)) - ((alturatc * (distancia-s) + alturarc*s) / distancia)  #'altura despejada vertical
                vm = zetam * hmi * math.sqrt((2*10**-3 * distancia) / (lambd * s * (distancia-s)))
                if (vm > vm50):
                    vm50 = vm
                    dim50 = s
                    gim50 = gs
                s = s + (salto * 0.5)
            
            if (vm50 >= -0.78):
                Lm50 = Calculos.Jota(vm50)  #'perdidas difraccion arista principal
                
                zetat = math.cos(math.atan(10**-3 * (gim50-alturatc) / dim50))
                s = 0.5 * salto
                while (s <= (dim50 - 0.5 * salto)):   #'Arista secundaria transmisor
                    if (s > cotaLim):
                        gs = (alturalisa + pendiente * (s-cotaLim)) + R #'* (distancia / cotaLim)      'altura perfil del punto a s
                    else:
                        gs = self.tablas.Matriz_Cotas(radial/saltoangular, (s/salto*2)) + R 
                        #gs = Sheets("RD41").Cells(5 + s / salto * 2, 23 + ((radial / 10) / 2)).Value + R
                    hti = gs + (10**3) * (s * (dim50-s) / (2*radio)) - ((alturatc * (dim50-s) + gim50*s) / dim50)  #'altura despejada vertical
                    vt = zetat * hti * math.sqrt((2 * 10**-3 * dim50) / (lambd * s * (dim50 - s)))
                    if (vt > vt50):
                        vt50 = vt
                        #dit50 = s
                    s = s + (salto * 0.5)

                if (vt50 >= -0.78): 
                    Lt50 = Calculos.Jota(vt50)  #'perdidas difraccion arista secundaria Tx (im50 < n-1)
                else:
                    Lt50 = 0
                
                zetar = math.cos(math.atan(1 * 10**-3 * (alturarc-gim50) / (distancia-dim50)))
                s = dim50 + 0.5 * salto
                while (s <= (distancia - 0.5 * salto)):  #'Arista secundaria receptor
                    if (s > cotaLim):
                        gs = (alturalisa + pendiente * (s - cotaLim)) + R #'* (distancia / cotaLim)      'altura perfil del punto a s
                    else:
                        gs = self.tablas.Matriz_Cotas(radial/saltoangular, (s/salto*2)) + R 
                        #gs = Sheets("RD41").Cells(5 + s / salto * 2, 23 + ((radial / 10) / 2)).Value + R
                    hri = gs + (10**3) * ((distancia-s) * (distancia-dim50) / (2*radio)) - ((alturarc * (s-dim50) + gim50 * (distancia-s)) / (distancia-dim50))  #'altura despejada vertical
                    vr = zetar * hri * math.sqrt((2 * 10**-3 * (distancia-dim50)) / (lambd * (distancia-s) * (s-dim50)))
                    if (vr > vr50):
                        vr50 = vr
                        #dir50 = s
                    s = s + (salto * 0.5)
                if (vr50 >= -0.78):
                    Lr50 = Calculos.Jota(vr50)  #'perdidas difraccion arista secundaria Tx (im50 > 2)
                else:
                    Lr50 = 0
            else:
                Lm50 = 0
                Lt50 = 0
                Lr50 = 0
        else:
            Lm50 = 0
            Lt50 = 0
            Lr50 = 0
        self.dim50[radial/saltoangular] = dim50
        #Sheets("RD41").Cells(212, 23 + ((radial / 10) / 2)).FormulaR1C1 = dim50
        return Lm50 + (1 - math.exp(float(-Lm50)/6)) * (Lt50 + Lr50 + 10 + 0.04*distancia)  #'perdidas de arista curvatura de la Tierra
            

    def Rugosidad_Terreno(self, radial, pendiente, alturalisa, horizontet, horizonter):
        hmmax = 0
        salto = round(self.params.resolucionCalculo/500, 2)
        s = horizontet
        saltoangular = 360 / self.params.radiales
        while (s <= horizonter):
            hi = self.tablas.Matriz_Cotas(radial/saltoangular, (s/salto*2)) #hi = Sheets("RD41").Cells(5 + s / salto * 2, 23 + ((radial / 10) / 2)).Value            
            hm = hi - (alturalisa + pendiente * s)
            if (hm > hmmax):
                hmmax = hm
            s = s + 0.5 * salto
        return hmmax   #'rugosidad del terreno