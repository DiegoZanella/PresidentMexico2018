import pandas as pd
import unidecode
import numpy as np

def depure(s):
    if s == 'Coahuila de Zaragoza':
        s = 'Coahuila'
    elif s == 'Michoacán de Ocampo':
        s = 'Michoacán'
    elif s == 'Veracruz de Ignacio de la Llave':
        s = 'Veracruz'
    elif s == 'CDMX':
        s = 'Ciudad de México'
    elif s == 'Cuatro Ciénegas':
        s = 'Cuatrocienegas'
    elif s == 'Cintalapa de Figueroa':
        s = 'Cintalapa'
    elif s == 'Villa Comaltitlán':
        s = 'Villacomaltitlan'
    elif s == 'Batopilas de Manuel Gómez Morín':
        s = 'Batopilas'
    elif s == 'General Simón Bolívar':
        s = 'Simon Bolivar'
    elif s == 'Jonacatepec de Leandro Valle':
        s = 'Jonacatepec'
    elif s == 'El Carmen':
        s = 'Carmen'
    elif s.split()[0] == 'Doctor' and s.split()[1] != 'Mora':
        s = 'Dr. ' + s.split()[1]
    elif s.split()[0] == 'General' and s.split()[1] not in ['Cepeda', 'Canuto', 'Heliodoro', 'Felipe',
                                                        'Plutarco', 'Enrique', 'Francisco', 'Pánfilo']:
        s = 'Gral. ' + s.split()[1]
    elif s == 'Juchitán de Zaragoza':
        s = 'Heróica Ciudad de Juchitán de Zaragoza'
    elif s == 'Heroica Villa de San Blas Atempa':
        s = 'San Blas Atempa'
    elif s == 'Villa de Santiago Chazumba':
        s = 'Santiago Chazumba'
    elif s == 'Heroica Villa Tezoatlán de Segura y Luna, Cuna de la Independencia de Oaxaca':
        s = 'H VILLA TEZOATLAN SEGURA Y LUNA CUNA IND OAX'
    elif s == 'Ahualulco del Sonido 13':
        s = 'Ahualulco'
    elif s == 'Ziltlaltépec de Trinidad Sánchez Santos':
        s = 'ZITLALTEPEC DE TRINIDAD SANCHEZ SANTOS'
    elif s == 'Cosamaloapan de Carpio':
        s = 'Cosamaloapan'
    elif s == 'Ozuluama de Mascareñas':
        s = 'Ozuluama'
    elif s == 'Zontecomatlán de López y Fuentes':
        s = 'Zontecomatlán'
    s = unidecode.unidecode(s)
    s = s.upper()
    return(s)
def county_codes(s):
    if int(s) < 10:
        s = '00' + str(s)
    elif int(s) < 100:
        s = '0' + str(s)
    return str(s)

def state_codes(s):
    if int(s) < 10:
        s = '0' + str(s)
    return str(s)

df = pd.read_excel('PRESIDENCIA_2018/2018_SEE_PRE_NAL_MUN.xlsx')

# Geolocalization data
geo = pd.read_csv('geo.csv')
geo = geo.drop_duplicates(subset=['CVE_ENT', 'CVE_MUN'])
geo['NOM_ENT'] = geo['NOM_ENT'].apply(depure)
geo['NOM_MUN'] = geo['NOM_MUN'].apply(depure)
ngeo = geo[['CVE_ENT', 'CVE_MUN', 'NOM_ENT', 'NOM_MUN', 'LAT_DECIMAL','LON_DECIMAL']]
ngeo['CVE_ENT'] = ngeo['CVE_ENT'].apply(state_codes)
ngeo['CVE_MUN'] = ngeo['CVE_MUN'].apply(county_codes)

print(ngeo[ngeo['NOM_MUN'] == 'CARMEN'])

# Cleaning election data
df.drop(labels=['ID_MUNICIPIO', 'SECCIONES', 'CASILLAS', 'CAND_IND1', 'CAND_IND2',
                'NUM_VOTOS_CAN_NREG', 'NUM_VOTOS_NULOS'], axis=1, inplace=True)

df['TOTAL_AMLO'] = df['PT'] + df['MORENA'] + df['ES'] \
                    + df['PT_MORENA_ES'] + df['PT_MORENA'] + df['PT_ES'] + df['MORENA_ES']
df['AMLO'] = df['TOTAL_AMLO'] / df['TOTAL_VOTOS']*100

df['TOTAL_JAM'] = df['PRI'] + df['PVEM'] + df['NA'] + df['PRI_PVEM_NA'] + df['PRI_PVEM'] \
                    + df['PRI_NA'] + df['PVEM_NA']
df['JAM'] = df['TOTAL_JAM'] / df['TOTAL_VOTOS']*100

df['TOTAL_RAC'] = df['PAN'] + df['PRD'] + df['MC'] + df['PAN_PRD_MC'] + df['PAN_PRD'] \
            + df['PAN_MC'] + df['PRD_MC']
df['RAC'] = df['TOTAL_RAC'] / df['TOTAL_VOTOS']*100

df['PARTICIPACIÓN'] = df['TOTAL_VOTOS'] / df['LISTA_NOMINAL'] *100
#print(df.columns)

ndf = df[['NOMBRE_ESTADO', 'MUNICIPIO', 'TOTAL_AMLO', 'AMLO', 'TOTAL_JAM','JAM',
          'TOTAL_RAC', 'RAC', 'PARTICIPACIÓN']]
ndf = ndf.drop(ndf[ndf['MUNICIPIO']=='VOTO EN EL EXTRANJERO'].index)

#ndf.set_index('MUNICIPIO', inplace=True)
print(ndf.columns)
print(ndf)
#print(ndf.index.unique())

ndf['NOMBRE_ESTADO'] = ndf['NOMBRE_ESTADO'].apply(depure)
ndf['MUNICIPIO'] = ndf['MUNICIPIO'].apply(depure)
ndf = ndf.merge(ngeo, how='left', left_on=['NOMBRE_ESTADO', 'MUNICIPIO'],
                right_on = ['NOM_ENT', 'NOM_MUN'])
#ndf['coordenadas'] = ndf['LAT_DECIMAL'] + ' , ' + ndf['LON_DECIMAL']

#ndf.drop(['NOM_ENT', 'NOM_MUN'], axis=1, inplace=True)
print(ndf.columns)
print(ndf)

problem = ndf[ndf['CVE_ENT'].isna() ][['NOMBRE_ESTADO',   'MUNICIPIO',  'CVE_ENT']]
print(problem)

ndf.set_index('MUNICIPIO', inplace=True)
ndf.to_excel('DatosPresidenciales2018.xlsx')


print('Done!')
