# -*- coding: utf-8 -*-
'''
Created on 12-02-2014

@author: CRodriguez
'''
import math

# se puede mejorar
def ArcTan(co,ca):
    if (co==0 and ca==0):
        at = 0
    else:
        if (ca==0):
            ca = 0.00000000001
        at = math.atan(co/ca)
    return at

# se puede mejorar, existe log10 en python
def Log10(valor):
    #l = 0
    if (valor > 0):
        l = math.log(valor) / math.log(10)
    else:
        l = 0.00000001
    return l
    
def grados(radian):
    Pi = 3.14159265358979
    return (radian * (180/Pi))

def Log_Normal(valor):
    #Calculo de la distribucion normal acumulativa inversa
    C0 = 2.515516698
    C1 = 0.802853
    C2 = 0.10328
    D1 = 1.432788
    D2 = 0.189269
    D3 = 0.1308

    if (valor >= 0.000001) and (valor <= 0.5):
        T = math.sqrt(-2 * math.log(valor))
        Z = (((C2 * T + C1) * T) + C0) / (((D3 * T + D2) * T + D1) * T + 1)
        I = T - Z
    else:
        T = math.sqrt(-2 * math.log(1 - valor))
        Z = (((C2 * T + C1) * T) + C0) / (((D3 * T + D2) * T + D1) * T + 1)
        I = Z - T

    return I

def Max(a,b):
    return (a+b+abs(a-b))/2

def Min(a, b):
    return (a+b-abs(a-b))/2

def Jota(parametro):
    #'Calcula el parametro de perdidas por difraccion
    return 6.9 + 20 * Log10(math.sqrt((parametro - 0.1) ** 2 + 1) + parametro - 0.1)

def TanH(valor):
    return (math.exp(valor) - math.exp(-valor)) / (math.exp(valor) + math.exp(-valor))

def MultiplicaLista(lista, multi, radiales):
    #return [lista[r]*multi for r in range(0,18)]
    l=[]
    for r in range(0,radiales):
        l.append( lista[r] * multi )
    return l    
