#Prueba de conocimientos Talento B
#Juliana Lalinde Velásquez

import numpy as np
import pandas as pd
from pandas import DataFrame

#Lectura de las bases de datos
liquidacion = pd.read_excel('Liquidación.xlsx', sheet_name='Hoja1')
ordenes = pd.read_excel('Ordenes.xlsx', sheet_name='Lib Ordenes')
mercado = pd.read_excel('Mercado.xlsx', sheet_name='Mercado')

#Información general del mercado
empresas = []           #Lista vacía donde almacenamos la informacíon de las operaciones generales del mercado en la misma fecha
m = mercado.shape[0]    #Número de filas de datos
nombres = liquidacion.especie.unique()
for i in nombres:
    #Mercados de futuro: AFFX, AFEQ, AFIR
    #Mercado de contado: EQTY, REPO, TTV
    #Lista con el orden: [0] especie, [1] precio promedio mercados futuros, [2] precio promedio mercados contables, [3] # de acciones futuras,
    #[4] # de acciones contables
    empresa = [i,0,0,0,0]
    #indices = mercado.index[i in mercado['Nemotécnico']].tolist()
    indices = list(mercado.where(i in list(mercado['Nemotécnico'])))
print(indices)
print(nombres)

#Ordenes por cliente
n = ordenes.shape[0]    #Número de filas de datos
clientes = []           #Lista vacia donde se almacena la info de los clientes
for i in range(n):
    cliente = ordenes.iloc[i,4]
    #Revisar en que indice y cuantas ordenes ha realizado cada cliente
    indices = ordenes.index[ordenes['Nemotécnico'] == cliente].tolist()
    #Lista con el orden: [0] ID de cliente, [1] # de ordenes cerradas, [2] # de ordenes pendientes, [3] # de ordenes anuladas
    #[4] # de acciones compradas, [5] # de acciones vendidas, [6] ciudad de las liquidaciones, [7] canal de operación, [8] autentificación,
    #[9] # de ordenes mercado, [10] # de órdenes con límite, empresas de las que tiene acciones
    info = [cliente,0,0,0,0,0,'','','']
    acciones = []       #Lista de las empresas de las que tiene acciones
    for j in indices:
        orden = ordenes.iloc[j,11]
        if orden == 'Cerrada' or orden == 'Pendiente':
            liquidadas = liquidacion.index[liquidacion['orden'] == cliente].tolist() 
            if liquidadas != []:
                for x in liquidadas:
                    acciones.append(liquidacion.iloc[j])

            


    clientes[cliente].append(info)

print(clientes)