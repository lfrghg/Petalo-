#coding: utf-8

from numpy import empty
import streamlit as st
import pandas as pd
import datetime as dt
   
# #### Configuración de la página
st.set_page_config(page_title="Petalo Full Included", page_icon='logo.png', layout='centered', initial_sidebar_state='auto')

#  #### Crear titulos de la página principal
st.title("Herramienta para el dimensionamiento de plantas de autogeneración")
st.subheader("Generación Pétalo y Consumo Fronteras")

# centrar figura mendiante la creación de columnas
col1, col2, col3 = st.columns(3)
with col1:
    st.image("Solar PV.jpg",width=350)
    
### Crear títulos barra lateral
st.sidebar.title("Panel interactivo")
st.sidebar.write("Indique el periodo de consulta")
    
today = dt.date.today() + dt.timedelta(days=-4)
tomorrow = today + dt.timedelta(days=1)
date_beg = st.sidebar.date_input('Fecha inicial', today)
date_end = st.sidebar.date_input('Fecha final', tomorrow)
if date_beg > date_end:
    st.sidebar.error('Error: La fecha final debe ser posterior a la fecha inicial')
   # st.sidebar.success('Fecha inicial: `%s`\n\nFecha final:`%s`' % (date_beg, date_end)) 
    
from pydataxm.pydataxm import ReadDB  
XM        = ReadDB()
df_Gen   = XM.request_data("Gene",1,date_beg, date_end )
df_Gen = df_Gen.drop(columns=['Id'])
df_recursos = XM.request_data('ListadoRecursos',0,date_beg,date_end) 
df_gen_full = pd.merge(df_Gen,df_recursos,left_on=['Values_code'],right_on=['Values_Code'])
df_solar = df_gen_full[df_gen_full.Values_EnerSource=='RAD SOLAR']
#df_solar = df_gen_full[df_gen_full.Values_Name=='LA SIERPE']
df_solar = df_gen_full[df_gen_full.Values_Name=='PETALO DE CORDOBA I']  

df_Con   = XM.request_data("DemaComeNoReg",1,date_beg, date_end )
df_Come = df_Con[df_Con.Values_code=='GNYC']
#df_Come = df_Come.drop(columns=['Id','Values_code','Date'])

df_Prec   = XM.request_data("PrecBolsNaci",0,date_beg, date_end)

st.markdown("### Generación Pétalo de Córdoba:")
df_solar
st.markdown("### Consumos totales fronteras:")
df_Come
st.markdown("### Precios de bolsa:")
df_Prec

