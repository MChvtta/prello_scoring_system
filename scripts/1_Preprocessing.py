#!/usr/bin/env python
# coding: utf-8

# # ⚙️ **DATA IMPORT**

# In[1]:


import pandas as pd
import numpy as np
import os

DATA_PATH = '../data/raw'

POI_FILENAME = 'POI_tourist_establishments.csv'
SITE_FILENAME = 'POI_touristic_sites_by_municipality.csv'
SALARY_FILENAME = 'average_salary_by_municipality.csv'
GEOREF_FILENAME = 'geographical_referential.csv'
STOCK_FILENAME = 'housing_stock.csv'
SALES_FILENAME = 'notary_real_estate_sales.csv'
POPULATION_FILENAME = 'population_by_municipality.csv'
POVERTY_FILENAME = 'poverty_population_by_municipality.csv'
REAL_ESTATE_FILENAME = 'real_estate_info_by_municipality.csv'

poi_df = pd.read_csv(os.path.join(DATA_PATH, POI_FILENAME),usecols=lambda column: column != 'name')
site_df = pd.read_csv(os.path.join(DATA_PATH, SITE_FILENAME))
salary_df = pd.read_csv(os.path.join(DATA_PATH, SALARY_FILENAME),usecols=lambda column: column != 'country_code')
georef_df = pd.read_csv(os.path.join(DATA_PATH, GEOREF_FILENAME),usecols=lambda column: column != 'country_code')
stock_df = pd.read_csv(os.path.join(DATA_PATH, STOCK_FILENAME),usecols=lambda column: column not in ['int64_field_0', 'country_code'])
sales_df = pd.read_csv(os.path.join(DATA_PATH, SALES_FILENAME))
population_df = pd.read_csv(os.path.join(DATA_PATH, POPULATION_FILENAME),usecols=lambda column: column != 'country_code')
poverty_df = pd.read_csv(os.path.join(DATA_PATH, POVERTY_FILENAME),usecols=lambda column: column != 'country_code')
real_estate_df = pd.read_csv(os.path.join(DATA_PATH, REAL_ESTATE_FILENAME))


# # 🔭 **DATA EXPLORATION**
# 
# 
# 

# #### DF POI

# In[ ]:


poi_df.head() #DATA CLEAN
# importance : poids interne pour évaluer l'importance


# In[ ]:


# Création de la carte avec Plotly Express
#fig = px.scatter_mapbox(poi_df, lat='latitude', lon='longitude', hover_name='name_reprocessed',
                        #color='poi', size='importance', zoom=5, height=990)

# Personnalisation du titre et du style de la carte
#fig.update_layout(
    #title='Répartition des points d\'intérêt',
    #mapbox_style='open-street-map'  # Vous pouvez choisir parmi d'autres styles de carte, par exemple 'carto-positron'
#)

# Réduction de la taille des points
#fig.update_traces(marker=dict(size=4))

# Affichage du graphique
#fig.show()


# In[ ]:


#poi_count = poi_df['poi'].value_counts()

# Création du diagramme circulaire avec Plotly Express
#fig = px.pie(names=poi_count.index, values=poi_count.values, title='Répartition des points d\'intérêt (POI)')

# Affichage du graphique
#fig.show()


# In[ ]:


# 0 DOUBLONS !
poi_df.duplicated().sum()#.drop_duplicates()


# In[ ]:


poi_df.info()
poi_df.isnull().sum()


# #### DF SITE

# In[ ]:


site_df.head() # DATA CLEAN
# importance : poids interne pour évaluer l'importance


# In[ ]:


# Création de la carte avec Plotly Express
#fig = px.scatter_mapbox(site_df, lat='latitude', lon='longitude', hover_name='name_reprocessed',
                        #color='poi', size='importance', zoom=5, height=990)

# Personnalisation du titre et du style de la carte
#fig.update_layout(
    #title='Répartition des site touristiques',
    #mapbox_style='open-street-map'  # Vous pouvez choisir parmi d'autres styles de carte, par exemple 'carto-positron'
#)

# Réduction de la taille des points
#fig.update_traces(marker=dict(size=4))

# Affichage du graphique
#fig.show()


# In[ ]:


#poi_count = site_df['poi'].value_counts()

# Création du diagramme circulaire avec Plotly Express
#fig = px.pie(names=poi_count.index, values=poi_count.values, title='Répartition des site touristiques')

# Affichage du graphique
#fig.show()


# In[ ]:


# 0 DOUBLONS !
site_df.duplicated().sum()#.drop_duplicates()


# In[ ]:


site_df.info()
site_df.isnull().sum()


# #### DF SALARY

# In[ ]:


salary_df.head() # DATA CLEAN


# In[ ]:


salary_df["year"].unique()


# In[ ]:


# 0 DOUBLONS !
salary_df.duplicated().sum()#.drop_duplicates()


# In[ ]:


salary_df.info()
salary_df.isnull().sum()


# #### DF GEO REF

# In[ ]:


georef_df.head()


# In[ ]:


georef_df["municipality_type"].unique()


# In[ ]:


# 0 DOUBLONS !
georef_df.duplicated().sum()#.drop_duplicates()


# In[ ]:


georef_df.info()
georef_df.isnull().sum()


# #### DF STOCK

# In[3]:


stock_df.head() #drop de int64_field_0


# In[2]:


stock_df["year"].unique()


# In[ ]:


# 0 DOUBLONS !
stock_df.duplicated().sum()#.drop_duplicates()


# In[ ]:


stock_df.info() # supprimer la colonne int64_field-0
stock_df.isnull().sum()


# #### DF SALES

# In[ ]:


sales_df.head()


# In[ ]:


# 510 211 DOUBLONS !
sales_df.duplicated().sum()#.drop_duplicates()


# In[ ]:


s = (sales_df['sales_amount']
             .value_counts()
             .loc[sales_df['sales_amount'].value_counts() > 10])


# In[ ]:


s.index = s.index.astype(int)
s.loc[(s.index % 10) != 0]


# In[ ]:


s.plot


# In[ ]:


sales_df['sales_amount'].value_counts().loc[sales_df['sales_amount'].value_counts() > 10] #[220623264]#sort_values(ascending=True).astype(int)


# In[ ]:


sales_df.info(), #il manque des latitude et longitude
sales_df.isnull().sum()


# #### DF POPULATION

# In[ ]:


population_df.head()


# In[ ]:


population_df["year"].unique()


# In[ ]:


# ??? DOUBLONS !
population_df.duplicated().sum


# In[ ]:


population_df.info() #colonne YEAR en format INT64
population_df.isnull().sum()


# #### DF POVERTY

# In[ ]:


poverty_df.head()


# In[ ]:


poverty_df["year"].unique()


# In[ ]:


# 0 DOUBLONS !
poverty_df.duplicated().sum()


# In[ ]:


poverty_df.info() # YEAR est en type INT64 et non DATE
poverty_df.isnull().sum()


# #### DF REAL ESTATE

# In[2]:


real_estate_df.head()


# In[ ]:


# 0 DOUBLONS !
real_estate_df.duplicated().sum()


# In[ ]:


real_estate_df.info()
real_estate_df.isnull().sum()


# # 🧹 **DATA CLEANING**

# ### CLEANING

# ##### DF_SALES CLEANING

# In[ ]:


# SALES_DF: Suppression des doublons > nous passons de 4,3M de lignes à 3,821M
sales_df = sales_df.drop_duplicates()
sales_df.shape


# In[ ]:


# SALES_DF: Check si les doublons on été enlevés : OK
sales_df.duplicated().sum()


# In[ ]:


# SALES_DF: Suppression des prix au m2 supérieur à 30K€ et inférieur à 1K€ > nous passons à 3,3399M de lignes
sales_df = sales_df[(sales_df['sales_price_m2'] <= 30000) & (sales_df['sales_price_m2'] >= 1000)]
sales_df.shape


# In[ ]:


# SALES_DF:
s2 = (sales_df['sales_amount']
             .value_counts()
             .loc[sales_df['sales_amount'].value_counts() > 10])


# In[ ]:


# SALES_DF:
s2.index = s2.index.astype(int)
s2.loc[(s2.index % 10) != 0]


# In[ ]:


# SALES_DF:
sales_df = sales_df[sales_df['sales_amount'] > 1] # on enlève les 166 fois ou sales_amount = 1€
sales_df.shape


# In[ ]:


# SALES_DF: changement du type sales_date en datetime
sales_df['sales_date'] = pd.to_datetime(sales_df['sales_date'])
sales_df.info()


# In[ ]:


# SALES_DF: Création de l'histogramme avec Plotly Express
#fig = px.histogram(sales_df, x='sales_price_m2', nbins=700, title='Distribution de sales_price_m2')

# SALES_DF: Affichage du graphique
#fig.show()


# In[ ]:


# SALES_DF: Création de l'histogramme avec Plotly Express
#fig = px.histogram(sales_df, x='sales_amount', nbins=400, title='Distribution de sales')

# SALES_DF: Affichage du graphique
#fig.show()


# ##### DF_SALARY CLEANING

# In[ ]:


# DF_SALARY: ROUND avg_net_salary
salary_df['avg_net_salary'] = salary_df['avg_net_salary'].round()
salary_df.head()


# ##### DF_REAL_ESTATE CLEANING

# In[ ]:


# DF_REAL_ESTATE: suppression des nulls
real_estate_df = real_estate_df.dropna(axis=1)
real_estate_df.isnull().sum()


# ##### DF_SITE CLEANING

# In[ ]:


# SITE_DF: tri avec les données entre parenthèses de la colonne "name" inclues

import re

site_df['data_inside_parenthesis'] = site_df['name'].apply(lambda x: re.search(r'\((.*?)\)', x).group(1) if re.search(r'\((.*?)\)', x) else '')
site_df

#suppression de la colonne "name" dans un second temps

site_df.drop(columns=["name"])

#check pour savoir les informations présentes dans la colonne "poi", et si elles correspondent aux valeurs présentes dans la colonne "type"
print (site_df["poi"].value_counts())
print (site_df["data_inside_parenthesis"].value_counts().head(50))

#faire un mapping des colonnes poi, qui sont en fait plus pertinentes que celles de la colonne "type"


# In[ ]:


# SITE_DF: création d'un dictionnaire intégrant toutes les différentes valeurs inclues dans la colonne "poi"
s = site_df["poi"].value_counts()[site_df["poi"]]
{k: "toto" for k in s.index}


# In[ ]:


# SITE_DF: création d'un dictionnaire avec les catégories associées aux valeurs de la colonne POI

category_dict = {'1': 'Patrimoine',
 '2': 'Patrimoine',
 'zoo': 'Entertainment',
 'dune': 'Nature',
 'park': 'Nature',
 'rock': 'Nature',
 'sand': 'Nature',
 'beach': 'Nature',
 'cliff': 'Nature',
 'islet': 'Nature',
 'ridge': 'Nature',
 'water': 'Nature',
 'wreck': 'Patrimoine',
 'casino': 'Entertainment',
 'castle': 'Patrimoine',
 'cinema': 'Culture',
 'forest': 'Nature',
 'geyser': 'Nature',
 'marina': 'Nature',
 'meadow': 'Nature',
 'museum': 'Culture',
 'valley': 'Nature',
 'theatre': 'Culture',
 'volcano': 'Nature',
 'wetland': 'Nature',
 'heritage': 'Patrimoine',
 'monument': 'Patrimoine',
 'vineyard': 'Nature',
 'viewpoint': 'Nature',
 'waterfall': 'Nature',
 'allotments': 'Patrimoine',
 'attraction': 'Entertainment',
 'theme_park': 'Entertainment',
 'water_park': 'Entertainment',
 'golf_course': 'Entertainment',
 'cave_entrance': 'Culture',
 'national_park': 'Nature',
 'protected_area': 'Nature'}


# In[ ]:


# SITE_DF: création de la colonne "catégorie"
site_df["Category"] = site_df["poi"].map(category_dict)
site_df


# ### CLEANED DF CHECK

# In[ ]:


poi_df.info()
site_df.info()
salary_df.info()
georef_df.info() 
stock_df.info() 
sales_df.info()
population_df.info() 
poverty_df.info()
real_estate_df.info()


# In[ ]:


poi_df.head(1)


# In[ ]:


site_df.head(1) 


# In[ ]:


salary_df.head(1)


# In[ ]:


georef_df.head(1) 


# In[ ]:


stock_df.head(1) 


# In[ ]:


sales_df.dtypes


# In[ ]:


population_df.head(1) 


# In[ ]:


poverty_df.head(1)


# In[ ]:


real_estate_df.head(1)


# # 🚀 **EXPORT**

# In[ ]:


# Chemin du dossier où les fichiers seront enregistrés
output_folder = "../data/cleaned"

# Assurez-vous que le dossier existe
os.makedirs(output_folder, exist_ok=True)

# Liste des DataFrames et leurs noms
dataframes = {
    "poi_df": poi_df,
    "site_df": site_df,
    "salary_df": salary_df,
    "georef_df": georef_df,
    "stock_df": stock_df,
    "sales_df": sales_df,
    "population_df": population_df,
    "poverty_df": poverty_df,
    "real_estate_df": real_estate_df
}

# Exportation des DataFrames en CSV
for name, df in dataframes.items():
    output_path = os.path.join(output_folder, f"{name}_cleaned.csv")
    df.to_csv(output_path, index=False)
    print(f"DataFrame {name} exporté vers {output_path}")

