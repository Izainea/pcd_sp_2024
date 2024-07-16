import streamlit as st
from sodapy import Socrata  
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from dotenv import load_dotenv
load_dotenv('.env')

APP_TOKEN = os.getenv('TOKEN_SODAPY')
DATASET_ID = os.getenv('DATASET_ID')

st.title('Contratos')
st.write('Mi primer aplicativo para contratos')

## Selector de contratos, cargo datos de contratos desde sodapy y le permito al usuario escoger 
## un contrato a visualizar

client = Socrata("www.datos.gov.co", APP_TOKEN)

Query = """
select 
    id_contrato, nombre_entidad, departamento, descripcion_del_proceso, valor_del_contrato,fecha_de_firma
where
    fecha_de_firma >= '2024-01-01'
limit
1000
"""

results = client.get(DATASET_ID, query=Query)

df = pd.DataFrame.from_records(results)

contrato = st.selectbox('Seleccione un contrato', df['id_contrato'],
                        placeholder='Seleccione un contrato único',disabled=False)

dataset_contrato = df[df['id_contrato'] == contrato].T

st.dataframe(dataset_contrato)

## Visualización de contratos por departamento

st.write('Visualización de contratos por departamento')

df['departamento'] = df['departamento'].str.upper()

### Usamos sns para visualizar los contratos por departamento

fig, ax = plt.subplots()
sns.countplot(data=df, x='departamento', ax=ax)
plt.xticks(rotation=90)
st.pyplot(fig)