import pandas as pd
import seaborn as sns

#Rutas de importación y exportación.

sldb = pd.read_csv('synergy_logistics_database.csv', index_col=0, parse_dates=[5])
"""
Analisis para las 10 rutas
"""
rutas = sldb.groupby(['direction','origin', 'destination', 'transport_mode'])
suma = rutas.sum()['total_value']
rutas = rutas['total_value'].describe()

rutas['suma_total'] = suma
rutas = rutas.reset_index()

"""
Analisis para exportaciones: Top 10 rutas por demanda y por ganancias
"""
exportaciones = rutas[ rutas['direction'] == 'Exports']
importaciones = rutas[rutas['direction'] == 'Imports']

def sol1(df, top=10):
    suma_total_df = df['suma_total'].sum()
    most_used = df.sort_values(by='count', ascending=False).head(top)
    suma_total_top = most_used.suma_total.sum()

    total_usos = most_used['count'].sum()
    porcentaje = (suma_total_top / suma_total_df) * 10000
    porcentaje = int(porcentaje) / 100
    print(f'Las {top} rutas mas demandadas aportan {porcentaje}% de las ganancias, en un total de {total_usos} servicios')
    return most_used

print(f'En el caso de las Exportaciones:')
mu = sol1(exportaciones)
mu

print(f'En el caso de las Importaciones:')
mu = sol1(importaciones)
mu

# Analisis por medios de transporte

sldb = pd.read_csv('synergy_logistics_database.csv', index_col=0, parse_dates=[5])
ax = sns.countplot(x='transport_mode', data=sldb)

# Analisis por medios de transporte anual

transportes_anuales = sldb.groupby(by=['year', 'transport_mode'])
valor_anual_transporte = transportes_anuales['total_value'].agg(pd.Series.sum)

info_transp_anual = pd.DataFrame()
info_transp_anual['valor_total'] = valor_anual_transporte
info_transp_anual['frecuencia'] = transportes_anuales['total_value'].describe()['count']

sns.lineplot(x='year', y='frecuencia', hue='transport_mode', data=info_transp_anual)

#Valor total de exportaciones

sldb = pd.read_csv('synergy_logistics_database.csv', index_col=0, parse_dates=[5])
datos = sldb[ sldb['direction'] == 'Exports' ][['origin', 'total_value']]
suma = datos.groupby('origin').sum()
cuenta = datos.groupby('origin').count()
lista = suma.reset_index()
lista = lista.merge(cuenta, left_on='origin', right_index=True)
cols = {'total_value_x':'valor', 'total_value_y':'cant. servicios'}
lista = lista.rename(columns=cols)
lista['porcentaje'] = (lista['valor'] / lista['valor'].sum()) * 100
lista = lista.sort_values(by='valor', ascending=False)
lista['porcentaje acum.'] = lista.cumsum()['porcentaje']
lista

#Valor total de importaciones 

"""
datos = sldb[ sldb['direction'] == 'Imports' ][['origin', 'total_value']]
suma = datos.groupby('origin').sum()
cuenta = datos.groupby('origin').count()
lista = suma.reset_index()
lista = lista.merge(cuenta, left_on='origin', right_index=True)
cols = {'total_value_x':'valor', 'total_value_y':'cant. servicios'}
lista = lista.rename(columns=cols)
lista['porcentaje'] = (lista['valor'] / lista['valor'].sum()) * 100
lista = lista.sort_values(by='valor', ascending=False)
lista['porcentaje acum.'] = lista.cumsum()['porcentaje']
lista"""
