# -*- coding: iso-8859-15 -*-
'''
Created on 06-03-2014

@author: CRodriguez
'''
import math
import OtrosCalculos as Calculos

class CalculosZona370():
    
    params = 0   # Objeto: ParametrosFormulario
    tablas = 0   # Objeto: TablaValores
    deltaH = []
    
    def __init__(self, params, tablas):
        self.params = params
        self.tablas = tablas
        
    def Inicio_370(self, radiales):
        self.calcularDeltaH()
        arrayZSRec370 = []

        for r in range(0,radiales):
            h = self.tablas.tablaCotas_Valores['h1'][r]

            if (h < 0):
                h = self.params.alturaAntenaTransmisora

            dh = self.deltaH[r]
            perdidas = self.params.perdidaCablesConectores + self.params.perdidaDivisorPotencia + self.params.otrasPerdidas
            P = 10 * Calculos.Log10(self.params.potencia) + self.params.ganancia - perdidas - self.params.perdidasLobulo[r]
            arrayZSRec370.append( self.Calcula_Distancia_370(self.params.intensidadCampoReferencia, h, dh, P) )

        return arrayZSRec370

    # tomar valores de cotas, ordenar y tomar las posiciones 9 y 74 restar (9-74)
    def calcularDeltaH(self):
        self.deltaH = []
        radiales = self.params.radiales
        for r in range(0,radiales):
            l = []
            for d in range(41,201):  # valores de cotas desde 10 a 50 kms, 10kms = posicion 20, 50kms = posicion 100 de tabla de cotas
                if (d % 2 == 0):
                    l.append( self.tablas.Matriz_Cotas(r,d) )
            l.sort(reverse=True)
            self.deltaH.append( l[8] - l[73] )

    def Calcula_Distancia_370(self, E, h, dh, P):
        Fca = 0 # Asignacion de valor por defecto
        #'Calcula la distancia a la que se produce una intensidad de campo E
        if (h > 1200):    #'MsgBox "Altura sobre el limite, se asumira hi = 1200 m", vbExclamation
            h = 1199.99
        if (h < 37.5):    #'MsgBox "Altura bajo el limite, se asumira hi = 37,5 m", vbExclamation
            h = 37.51
        if (dh > 1000):   #'MsgBox "Delta-H sobre el limite, se asumira Dh = 1000 m", vbExclamation
            dh = 999.99
        if (dh < 10):     #'MsgBox "Delta-H bajo el limite, se asumira Dh = 10 m", vbExclamation
            dh = 10.01

        a0 = -16.36932424214
        a1 = 0.044802696567377
        a2 = -4.932965993005E-05
        a3 = 1.9371835269792E-08
        a4 = 3.6643359351263

        infl = a0 + a1 * dh + a2 * dh * dh + a3 * dh * dh * dh + a4 * math.log(dh)

        if (h < 75):
            C0 = 0.1114876543408 * h + 106.94768420836
            C1 = -0.000534259586939 * h - 0.10642244576921
            C2 = -1.30880140177E-05 * h + 1.5004266224724E-03
            c3 = 4.678300131517E-08 * h - 4.23836612412E-06
            c4 = 0.0287902859644 * h - 20.739626447348
        if ((h >= 75) and (h < 150)):
            C0 = 0.106430847979867 * h + 107.32694468543
            C1 = -3.778072852863E-04 * h - 0.11815636839314
            C2 = -1.1220890386627E-06 * h + 6.0298224904173E-04
            c3 = 3.8266936972787E-09 * h - 1.0166430527762E-06
            c4 = 1.5776342509467E-03 * h - 18.698677568839
        if ((h >= 150) and (h < 300)):
            C0 = -0.0207665087734 * h + 126.40654819842
            C1 = -1.3125464659513E-03 * h + 0.02205450870661
            C2 = 4.3728601258665E-06 * h - 2.2126012563764E-04
            c3 = -5.3335964079973E-09 * h + 3.574004630152E-07
            c4 = 0.032048801628973 * h - 23.269352675543
        if ((h >= 300) and (h < 600)):
            C0 = -0.0406181022365 * h + 132.36202623735
            C1 = -4.127444887297E-04 * h - 0.24788608445986
            C2 = 3.3251945296467E-07 * h + 9.908420762329E-04
            c3 = 4.6618381272333E-10 * h - 1.382533603201E-06
            c4 = 0.022819539559086 * h - 20.500574054577
        if (h >= 600):
            C0 = -0.041055307372173 * h + 132.62434931871
            C1 = -1.8873893521345E-04 * h - 0.38216941656961
            C2 = 6.0466463402E-08 * h + 1.1540738699705E-03
            c3 = 1.97043439896E-10 * h - 1.2210493795046E-06
            c4 = 0.016756922176087 * h - 16.863003624777
        try:
            d = 10
            d0 = 50
            j = 0
            if ((C0 + C1 * 50 + C2 * 2500 + c3 * 125000 + c4 * math.log(50) + P - infl) > E):
                while (True):
                    d0 = d
                    F = C0 + C1 * d + C2 * d * d + c3 * d * d * d + c4 * math.log(d) - infl + P - E
                    F1 = C1 + 2 * C2 * d + 3 * c3 * d * d + c4 / d
                    d = d - F / F1
                    j = j + 1
                    if not( (j<45) and ( abs(d-d0)>0.000000000000001) ):
                        break
                j = 1
            
            if ((C0 + C1 * 10 + C2 * 100 + c3 * 1000 + c4 * math.log(10) + P) < E):
                while (True):
                    d0 = d
                    F = C0 + C1 * d + C2 * d * d + c3 * d * d * d + c4 * math.log(d) + P - E
                    F1 = C1 + 2 * C2 * d + 3 * c3 * d * d + c4 / d
                    d = d - F / F1
                    j = j + 1
                    if not((j<45) and (abs(d-d0) > 0.000000000000001)):
                        break
                j = 2
                
            if ((C0 + C1 * 50 + C2 * 2500 + c3 * 125000 + c4 * math.log(50) + P - infl) <= E) and ((C0 + C1 * 10 + C2 * 100 + c3 * 1000 + c4 * math.log(10) + P) >= E):
                while (True):
                    d0 = d
                    F = C0 + C1 * d + C2 * d * d + c3 * d * d * d + c4 * math.log(d) + P - E - infl / 40 * d + infl / 4
                    F1 = C1 + 2 * C2 * d + 3 * c3 * d * d + c4 / d - infl / 40
                    d = d - F / F1
                    j = j + 1
                    if not((j<45) and (abs(d-d0) > 0.000000000000001)):
                        break
                j = 0
                
        except:
            d = 10
            campo = self.Campo_VHF(d, h, dh, P, 0) - Fca
            
            while ((abs(campo - E) > 0.5) and (d >= 1)):
                d = d - 0.05
                campo = self.Campo_VHF(d, h, dh, P, 0) - Fca
            
            if (d < 1):
                d = 1


        dlim = self.Distancia_Limite_VHF(E, dh, P) #'Calcula el valor para un hi = 600 m
        if (h <= 599 and d > dlim) or (h >= 601 and d < dlim):
            d = dlim
        
        return d
    

    def Distancia_Limite_VHF(self, E, dh, P):
        #'Calcula la distancia a la que se produce una intensidad de campo E con un hi=600
        h = 600
        if (dh > 1000):
            dh = 999.99
        elif (dh < 10):
            dh = 10.01
        
        a0 = -16.36932424214
        a1 = 0.044802696567377
        a2 = -4.932965993005E-05
        a3 = 1.9371835269792E-08
        a4 = 3.6643359351263
        infl = a0 + a1 * dh + a2 * dh * dh + a3 * dh * dh * dh + a4 * math.log(dh)

        C0 = -0.041055307372173 * h + 132.62434931871
        C1 = -1.8873893521345E-04 * h - 0.38216941656961
        C2 = 6.0466463402E-08 * h + 1.1540738699705E-03
        c3 = 1.97043439896E-10 * h - 1.2210493795046E-06
        c4 = 0.016756922176087 * h - 16.863003624777
        #On Error Resume Next    ' Inicializa el controlador de error.
        
        d = 10
        d0 = 50
        j = 0
        if ((C0 + C1 * 50 + C2 * 2500 + c3 * 125000 + c4 * math.log(50) + P - infl) > E):
            while (True):
                d0 = d
                F = C0 + C1 * d + C2 * d * d + c3 * d * d * d + c4 * math.log(d) - infl + P - E
                F1 = C1 + 2 * C2 * d + 3 * c3 * d * d + c4 / d
                d = d - F / F1
                j = j + 1
                if not((j < 45) and (abs(d - d0) > 0.000000000000001)):
                    break
            j = 1
            
        if ((C0 + C1 * 10 + C2 * 100 + c3 * 1000 + c4 * math.log(10) + P) < E):
            while (True):
                d0 = d
                F = C0 + C1 * d + C2 * d * d + c3 * d * d * d + c4 * math.log(d) + P - E
                F1 = C1 + 2 * C2 * d + 3 * c3 * d * d + c4 / d
                d = d - F / F1
                j = j + 1
                if not((j < 45) and (abs(d - d0) > 0.000000000000001)):
                    break
            j = 2
            
        if ((C0 + C1 * 50 + C2 * 2500 + c3 * 125000 + c4 * math.log(50) + P - infl) <= E) and ((C0 + C1 * 10 + C2 * 100 + c3 * 1000 + c4 * math.log(10) + P) >= E):
            while (True):
                d0 = d
                F = C0 + C1 * d + C2 * d * d + c3 * d * d * d + c4 * math.log(d) + P - E - infl / 40 * d + infl / 4
                F1 = C1 + 2 * C2 * d + 3 * c3 * d * d + c4 / d - infl / 40
                d = d - F / F1
                j = j + 1
                if not ((j < 45) and (abs(d - d0) > 0.000000000000001)):
                    break
            j = 0

        return d


    def Campo_VHF(self, d, h, dh, P, Fca):
        #'Calcula la intensidad de campo que se produce a la distancia d de la estacion
        if (d <= 0):     #' MsgBox "Imposible calcular campo", vbCritical, "Error de distancia"
            return
        if (h > 1200):   #'MsgBox "Altura sobre el limite, se asumira hi = 1200 m", vbExclamation
            h = 1200
        elif (h < 37.5): #'MsgBox "Altura bajo el limite, se asumira hi = 37,5 m", vbExclamation
            h = 37.5
        if (dh > 1000):  #'MsgBox "Delta-H sobre el limite, se asumira Dh = 1000 m", vbExclamation
            dh = 1000
        elif (dh < 10):   #'MsgBox "Delta-H bajo el limite, se asumira Dh = 10 m", vbExclamation
            dh = 10
        
        P = P - Fca   #'Considera factor de correccion por altura

        if (dh >= 500): #'Delta H minimo es 10
            infl = 0.0104 * (dh - 500) + 18.5
        else:
            infl = -2.95532103321E-14 * dh ** 6 + 5.00156359416E-11 * dh ** 5 - 3.33307086953E-08 * dh ** 4 + 1.12398772368E-05 * dh ** 3 - 0.00211598154822 * dh ** 2 + 0.267017851123 * dh - 9.07022390067
        
        if (h < 75):
            C0 = 0.1114876543408 * h + 106.94768420836
            C1 = -0.000534259586939 * h - 0.10642244576921
            C2 = -1.30880140177E-05 * h + 1.5004266224724E-03
            c3 = 4.678300131517E-08 * h - 4.23836612412E-06
            c4 = 0.0287902859644 * h - 20.739626447348
        elif ((h >= 75) and (h < 150)):
            C0 = 0.106430847979867 * h + 107.32694468543
            C1 = -3.778072852863E-04 * h - 0.11815636839314
            C2 = -1.1220890386627E-06 * h + 6.0298224904173E-04
            c3 = 3.8266936972787E-09 * h - 1.0166430527762E-06
            c4 = 1.5776342509467E-03 * h - 18.698677568839
        elif ((h >= 150) and (h < 300)):
            C0 = -0.0207665087734 * h + 126.40654819842
            C1 = -1.3125464659513E-03 * h + 0.02205450870661
            C2 = 4.3728601258665E-06 * h - 2.2126012563764E-04
            c3 = -5.3335964079973E-09 * h + 3.574004630152E-07
            c4 = 0.032048801628973 * h - 23.269352675543
        elif ((h >= 300) and (h < 600)):
            C0 = -0.0406181022365 * h + 132.36202623735
            C1 = -4.127444887297E-04 * h - 0.24788608445986
            C2 = 3.3251945296467E-07 * h + 9.908420762329E-04
            c3 = 4.6618381272333E-10 * h - 1.382533603201E-06
            c4 = 0.022819539559086 * h - 20.500574054577
        else:       #'hi mayor a 600
            C0 = -0.041055307372173 * h + 132.62434931871
            C1 = -1.8873893521345E-04 * h - 0.38216941656961
            C2 = 6.0466463402E-08 * h + 1.1540738699705E-03
            c3 = 1.97043439896E-10 * h - 1.2210493795046E-06
            c4 = 0.016756922176087 * h - 16.863003624777
        
        if (d > 50):
            E = C0 + C1 * d + C2 * d * d + c3 * d * d * d + c4 * math.log(d) - infl + P
        elif (d < 10):
            E = C0 + C1 * d + C2 * d * d + c3 * d * d * d + c4 * math.log(d) + P
        else:
            E = C0 + C1 * d + C2 * d * d + c3 * d * d * d + c4 * math.log(d) + P - infl / 40 * d + infl / 4
            
        return E   #'Muestra el campo
