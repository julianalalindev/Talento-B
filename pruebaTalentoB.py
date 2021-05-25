#Prueba de conocimientos Talento B
#Juliana Lalinde Velásquez
#Python 3.7.4

import numpy as np
import pandas as pd
from pandas import DataFrame
import operator
import datetime as dt

#Lectura de las bases de datos
liquidacion = pd.read_excel('Liquidación.xlsx', sheet_name='Hoja1')
ordenes = pd.read_excel('Ordenes.xlsx', sheet_name='Lib Ordenes')
mercado = pd.read_excel('Mercado.xlsx', sheet_name='Mercado')

#Excel para la información que se busca almacenar de los clientes
writer=pd.ExcelWriter('infoClientes.xlsx')

#Información general del mercado
empresas = []           #Lista vacía donde almacenamos la informacíon de las operaciones generales del mercado en la misma fecha
nombres = liquidacion.especie.unique()  #Nombres de las empresas de las que se tienen acciones
for i in nombres:
    #Mercados de futuro: AFFX, AFEQ, AFIR
    #Mercado de contado: EQTY, REPO, TTV
    #Lista con el orden: [0] especie, [1] precio promedio mercados futuros, [2] precio promedio mercados contables, [3] # de acciones futuras,
    #[4] # de acciones contables, [5] promedio de acciones futuras por operación, [6] promedio de acciones contables por operación
    empresa = [i,0,0,0,0,0,0]
    indices = mercado[mercado['Nemotécnico'].str.startswith(i)].index     #Indices en los que hay transacciones de esa empresa
    #Revisión de la información de la empresa
    for j in indices:
        movimiento = list(mercado.iloc[j,:])
        if movimiento[2] == 'Calzado':
            #Cálculo de las acciones en mercados de contado
            if movimiento[4] == 'EQTY':
                empresa[4] += movimiento[6]
                empresa[2] += movimiento[6]*movimiento[5]
                empresa[5] += 1
            #Cálculo de las acciones en mercados futuros
            elif movimiento[4] == 'AFFX' or movimiento[4] == 'AFEQ' or movimiento[4] == 'AFIR' or movimiento[4] == 'REPO' or movimiento[4] == 'TTV':
                empresa[3] += movimiento[6]
                empresa[1] += movimiento[6]*movimiento[5]
                empresa[6] += 1
    #Promedio de precio de las acciones
    if empresa[3] > 0:
        empresa[1] /= empresa[3]
    if empresa[4] > 0:
        empresa[2] /= empresa[4]
    if empresa[5] > 0:
        empresa[5] = empresa[3]/empresa[5]
    if empresa[6] > 0:
        empresa[6] = empresa[4]/empresa[6]
    empresas.append(empresa)

#Ordenes por cliente
clientes = []           #Lista vacia donde se almacena la info de los clientes
maxAcciones = []        #Empresa de la que más acciones vendió  y compró cada cliente
nombresClientes = ordenes.cod_Comitente.unique()  #Nombres de los clientes en el libro de órdenes
for i in nombresClientes:
    #Revisar en que indice y cuantas ordenes ha realizado cada cliente
    indices = ordenes[ordenes['cod_Comitente'] == i].index     #Indices en los que hay ordenes del cliente,
    #Lista con el orden: [0] ID de cliente, [1] # de ordenes cerradas, [2] # de ordenes pendientes, [3] # de ordenes anuladas, [4] ciudad
    #de las liquidaciones, [5] canal de operación, [6] autentificación, [7] # de ordenes mercado, [8] # de órdenes con límite, [9] # de ordenes
    #ingresadas antes del medio día
    cliente = [i,0,0,0,'','','',0,0,0]
    accionesV = {}      #Empresas en las que vendió acciones
    accionesC = {}      #Empresas en las que compró acciones
    limite = len(liquidacion[liquidacion['orden'] == ordenes.iloc[j,0]].index)
    hora = []
    for j in indices:
        estado = ordenes.iloc[j,11]
        if estado == 'Cerrada' or estado == 'Pendiente' or estado == 'Modificacion':
            liquidadas = liquidacion[liquidacion['orden'] == ordenes.iloc[j,0]].index     #Indices en los que hay operaciones de la orden
            for x in liquidadas:
                movimiento = list(liquidacion.iloc[x,:])
                if movimiento[9] == 'Cerrada' or (ordenes.iloc[j,10]-ordenes.iloc[j,6]) > 0:
                    if(movimiento[2] == 'V'):
                        if(movimiento[3] in accionesV):
                            accionesV[movimiento[3]] += movimiento[4]
                        else:
                            accionesV[movimiento[3]] = movimiento[4]
                    if(movimiento[2] == 'C'):
                        if(movimiento[3] in accionesC):
                            accionesC[movimiento[3]] += movimiento[4]
                        else:
                            accionesC[movimiento[3]] = movimiento[4]
                    cliente[1] += 1
                    cliente[4] = movimiento[6]
                    cliente[5] = movimiento[10]
                    cliente[6] = movimiento[11]
                    if ordenes.iloc[j,7] == 'Mercado':
                        cliente[7] += 1
                    else:
                        cliente[8] += 1
                    if ordenes.iloc[j,14] <= dt.time(12):
                        cliente[9] += 1
                else:
                    cliente[2] += 1
        elif estado == "Anulada":
            cliente[3] += 1
            break
    if(accionesV):
        maxV = max(accionesV.items(), key=operator.itemgetter(1))[0]
        maxAccionesV = [i,maxV,accionesV[maxV]]
    else:
        maxAccionesV = [i,'No vendió acciones en la fecha determinada',0]
    if(accionesC):
        maxC = max(accionesC.items(), key=operator.itemgetter(1))[0]
        maxAccionesC = [i,maxC,accionesC[maxC]]
    else:
        maxAccionesC = [i,'No compró acciones en la fecha determinada',0]
    maxAcciones.append(maxAccionesV+maxAccionesC)
    clientes.append(cliente)

#Escribir los resultados en un excel para manejarlos más fácil
dataAcciones = pd.DataFrame(maxAcciones,columns=['Cliente', 'Empresa', '# de acciones vendidas', 'Cliente','Empresa','# de acciones compradas'])
dataAcciones.to_excel(writer,sheet_name='Máximo de acciones',header=None,index=False) 
preciosMercado = pd.DataFrame(empresas)
preciosMercado.to_excel(writer,sheet_name='Mercado',header=None,index=False)
clientesInfo = pd.DataFrame(clientes)
clientesInfo.to_excel(writer,sheet_name='Clientes',header=None,index=False)
writer.save()