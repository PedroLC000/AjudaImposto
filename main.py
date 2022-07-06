import argparse
import pandas as pd
import numpy as np
import csv
from csv import writer

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--inputfile')
args = vars(parser.parse_args())

if not args.get('inputfile', False):
  print('Erro, nenhuma entrada encontrada')
  exit()
else:
  df = pd.read_csv(args['inputfile'], encoding='ISO-8859-1')
  
df_collumn0 = df['Valor da Operação'].to_list()
df_collumn1 = df['Movimentação'].to_list()
dfDy = df.copy()
dfLiquidacao = df.copy()

for cont, i in enumerate(df_collumn1):
  if i != 'Dividendo' and i != 'Juros Sobre Capital Próprio' and i != 'Rendimento':
    dfDy.drop(cont, axis= 0, inplace=True)

for cont, a in enumerate(df_collumn1):
  if a != 'Transferência - Liquidação':
    dfLiquidacao.drop(cont, axis= 0, inplace=True)

for cont, i in enumerate(df_collumn0):
  if i == ' - ':
    df.drop(cont, axis= 0, inplace=True) 

dfLiquidacao_Debito = dfLiquidacao[dfLiquidacao['Entrada/Saída'] == 'Debito']
dfLiquidacao_Credito = dfLiquidacao[dfLiquidacao['Entrada/Saída'] == 'Credito']

df_collumn2 = dfDy['Produto'].to_list()
allValuesDY = set(df_collumn2)

extractAll = []
extractAll2 = []

for df_allValuesDY in allValuesDY:
  soma = 0
  df_newAllValuesDY = dfDy[dfDy['Produto'] == df_allValuesDY]['Valor da Operação']
  for a in df_newAllValuesDY:
    b = a.replace('R$', '')
    c = float(b.replace(',', '.'))
    soma = soma + c  

  extract = {}
  extract['Ativo c/ Dividendos'] = df_allValuesDY
  extract['Dividendos'] = 'R$%.2f' % round(soma, 2)
  extractAll.append(extract)
  
  with open('Dividendos.csv', 'w', newline='', encoding='UTF-8') as csvfile:
    fieldnames = ['Ativo c/ Dividendos', 'Dividendos']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(extractAll)

df_collumn3 = dfLiquidacao['Produto'].to_list()
allValues = set(df_collumn3)

for df_allValues in allValues:
  soma_entSaida = 0
  soma_quant = 0
  df_newAllValues = dfLiquidacao[dfLiquidacao['Produto'] == df_allValues]['Valor da Operação']
  df_entSaida = dfLiquidacao[dfLiquidacao['Produto'] == df_allValues]['Entrada/Saída'].to_list()
  df_quant = dfLiquidacao[dfLiquidacao['Produto'] == df_allValues]['Quantidade'].to_list()

  for cont, a in enumerate(df_newAllValues):
    b = a.replace('R$', '')
    c = float(b.replace(',', '.'))
    soma_quant = soma_quant + df_quant[cont]

    if df_entSaida[cont] == 'Credito':
      soma_entSaida = soma_entSaida + c  
    else:
      soma_entSaida = soma_entSaida - c  

  extract = {}
  extract['Ativo Movimentados'] = df_allValues
  extract['Preço Total'] = 'R$%.2f' % round(soma_entSaida, 2)
  extract['Quantidade'] = soma_quant
  extract['Preço Médio'] = 'R$%.2f' % round((soma_entSaida/soma_quant),2)
  extractAll2.append(extract)
  
  with open('Liquidacao.csv', 'w', newline='', encoding='UTF-8') as csvfile:
    fieldnames = ['Ativo Movimentados', 'Preço Total', 'Quantidade', 'Preço Médio']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(extractAll2)