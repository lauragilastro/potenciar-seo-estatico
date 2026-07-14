import pandas as pd

# SALVAR EL SEO DE LOS CLIENTES POBRES
# Este código me ayudará a detectar las PCs que son las MEJORES de cada monitoreo.
# ¿Para qué? porque estos clientes pobres al no poder pagarme el SEO orgánico, que al menos se -->
# --> pueda potenciar al máximo el SEO estático, dando lo mejor posible.
# Aunque tengas el mejor SEO estático del mundo, si Google no nota cambios, deja de leer la página -->
# --> y esta cae en posicionamiento.
# Por ello, vale con hacer algunos cambios aunque sean nimios para refrescar el contenido para Google.
# Y puestos a hacerlo, ¿por qué no con lo mejor?
# Hago un monitoreo mensual en GSC y saco las PCs más top (top 15, muchas imrpesiones, y CTR alto).
# Reemplazo en Astro los alt de img y metadatos con esas PCs.
# "Pero quitar lo que ya funciona del SEO estático es contraproducente" pues por eso esta herramienta -->
# --> es necesaria, para que puestos a cambiarlo, cambiarlo con lo más top del último mes.
# Resultado: google nota que la web se refresca pero no rompemos el SEO estático.

# BLOQUE 1: CARGA DE DATOS: python abre el excel y lo examina
ruta_excel = 'gsc-lauragilastro.xlsx'
excel_completo = pd.read_excel(ruta_excel, sheet_name=None)

# Extraemos las pestañas que necesitamos usando los nombres exactos
df_consultas = excel_completo['Consultas']
df_paginas = excel_completo['Páginas']

# Limpieza de datos: a veces Google pone "0" o símbolos raros, vamos a asegurarnos de que los números sean números
df_consultas['Clics'] = pd.to_numeric(df_consultas['Clics'], errors='coerce')
df_consultas['Posición'] = pd.to_numeric(df_consultas['Posición'], errors='coerce')
df_consultas['Impresiones'] = pd.to_numeric(df_consultas['Impresiones'], errors='coerce')
df_consultas['CTR'] = pd.to_numeric(df_consultas['CTR'], errors='coerce')

# BLOQUE 2: FILTRAMOS LAS PALABRAS CLAVE

# Pasito 1: buscamos la palabra con más impresiones y calculamos su 75%
max_impresiones = df_consultas['Impresiones'].max()
umbral = df_consultas['Impresiones'].quantile(0.75)

# Pasito 2: usamos ese umbral para filtrar
oportunidades = df_consultas[df_consultas['Impresiones'] > umbral].copy()

# Pasito 3: buscamos palabras con CTR bajo (-5%) y positions del 4 al 20
poderosas = oportunidades[
    (oportunidades['Posición'] >= 1) &
    (oportunidades['Posición'] <= 15)
].copy()



# BLOQUE 3: CLASIFICACIÓN Y CÁLCULO DE PÉRDIDAS DE CLICKS
poderosas = poderosas.sort_values(by='Impresiones', ascending=False)
poderosas = poderosas.head(30) # Solo muestra 30 palabras

# Lo que printeamos:
if poderosas.empty:
    print("No se han encontrado palabras clave poderosas")
else:
    print("PALABRAS CLAVE PODEROSAS PARA REFRESCAR ESTE MES:")
    print(poderosas[['Consultas principales', 'Posición', 'Impresiones', 'CTR']].to_string(index=False))

