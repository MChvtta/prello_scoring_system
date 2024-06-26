#!/usr/bin/env python
# coding: utf-8

# # ⚙️ **CLEANED DATA IMPORT**
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import RobustScaler, MinMaxScaler, StandardScaler

DATA_PATH = '../data/cleaned'

POI_FILENAME = 'poi_df_cleaned.csv'
SITE_FILENAME = 'site_df_cleaned.csv'
SALARY_FILENAME = 'salary_df_cleaned.csv'
GEOREF_FILENAME = 'georef_df_cleaned.csv'
STOCK_FILENAME = 'stock_df_cleaned.csv'
SALES_FILENAME = 'sales_df_cleaned.csv'
POPULATION_FILENAME = 'population_df_cleaned.csv'
POVERTY_FILENAME = 'poverty_df_cleaned.csv'
REAL_ESTATE_FILENAME = 'real_estate_df_cleaned.csv'

poi_df = pd.read_csv(os.path.join(DATA_PATH, POI_FILENAME))
site_df = pd.read_csv(os.path.join(DATA_PATH, SITE_FILENAME))
salary_df = pd.read_csv(os.path.join(DATA_PATH, SALARY_FILENAME))
georef_df = pd.read_csv(os.path.join(DATA_PATH, GEOREF_FILENAME))
stock_df = pd.read_csv(os.path.join(DATA_PATH, STOCK_FILENAME))
sales_df = pd.read_csv(os.path.join(DATA_PATH, SALES_FILENAME))
population_df = pd.read_csv(os.path.join(DATA_PATH, POPULATION_FILENAME))
poverty_df = pd.read_csv(os.path.join(DATA_PATH, POVERTY_FILENAME))
real_estate_df = pd.read_csv(os.path.join(DATA_PATH, REAL_ESTATE_FILENAME))


###____TOURISM (2 KPIS)____###
# Nombre de sites touristiques par départements : num_sites_per_department
# Répartition des catégories touristiques par départements :tourism_category_per_department


###____REAL ESTATE & SECONDARY HOME (5 KPIS)____###
# Prix moyen du m2 par département : average_price_per_m2
# Stock de biens par départements : total_stock_per_department
# Superficie moyenne des logements vendus par départements :average_surface_per_department
# Taux de répartition des maisons secondaires par départements : secondary_home_rate_per_department
# Évolution du % des maisons secondaires par département (entre 2008 et 2018) : secondary_home_rate_evolution_department
# Nombre de maisons vacantes (en 2019) : vacants_housing_per_department
# Taxe d'habitation (valeur et nombre) en 2023 par département : tax_df


###___LIFE QUALITY (4 KPIS)____###
# Salaire moyen par département : avg_salary_per_department
# Nombre de professionnels de santé pour 100 000 habitants par départements (en 2023) : health_df
# Taux de criminalité pour 1000 habitants par départements (en 2020) : criminality_per_department
# Nombre de jours de soleil par an par départements : sunny_df_per_department
# Fusion de tous DF Life Quality  par départements (POUR NORMALISATIN AU SCORING) : life_quality_df

# DF CLEANED CHECK
poi_df.info()
site_df.info()
salary_df.info()
georef_df.info() 
print (stock_df.info())
sales_df.info()
population_df.info() 
poverty_df.info()
real_estate_df.info()


#test
stock_df_test = stock_df.merge(georef_df, on="municipality_code")
stock_df_test = stock_df_test.groupby(["year", "department_name"])["nb_second_home"].sum().reset_index()
filtered_df = stock_df_test[stock_df_test["department_name"] == "Guyane"]
filtered_df


# ### CLEANING

# ##### DF_SALES CLEANING

# SALES_DF: Suppression des doublons > nous passons de 4,3M de lignes à 3,821M
sales_df = sales_df.drop_duplicates()
sales_df.shape

# SALES_DF: Check si les doublons on été enlevés : OK
sales_df.duplicated().sum()

# SALES_DF: Suppression des prix au m2 supérieur à 30K€ et inférieur à 1K€ > nous passons à 3,3399M de lignes
sales_df = sales_df[(sales_df['sales_price_m2'] <= 30000) & (sales_df['sales_price_m2'] >= 500)]
sales_df.shape

# SALES_DF:
s2 = (sales_df['sales_amount']
             .value_counts()
             .loc[sales_df['sales_amount'].value_counts() > 10])

# SALES_DF:
sales_df = sales_df[sales_df['sales_amount'] > 1] # on enlève les 166 fois ou sales_amount = 1€
sales_df.shape

# SALES_DF: changement du type sales_date en datetime
sales_df['sales_date'] = pd.to_datetime(sales_df['sales_date'])
sales_df["municipality_code"].nunique()


# ##### DF_SALARY CLEANING

# DF_SALARY: ROUND avg_net_salary
salary_df['avg_net_salary'] = salary_df['avg_net_salary'].round()
salary_df.head()


# ##### DF_REAL_ESTATE CLEANING

# DF_REAL_ESTATE: suppression des nulls
real_estate_df = real_estate_df.dropna(axis=1)
real_estate_df.isnull().sum()


# ##### DF_SITE CLEANING


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


# SITE_DF: création d'un dictionnaire intégrant toutes les différentes valeurs inclues dans la colonne "poi"
s = site_df["poi"].value_counts()[site_df["poi"]]
{k: "toto" for k in s.index}


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


# SITE_DF: création de la colonne "catégorie"
site_df["Category"] = site_df["poi"].map(category_dict)
site_df


# # 🧪 **DATA TRANSFORMATION**
# ### KPIS AGGREGATION BY DEPARTMENT
# ##### 1. TOURISM

#création de tables permettant de scorer le potentiel touristique de chaque département
site_df = site_df.merge (georef_df, on=["municipality_code"])
site_df.head(5)


#sélection des colonnes dont on aura besoin pour le calcul
site_df_department = site_df[["poi", "name", "municipality_code", "importance", "name_reprocessed", "department_name"]]
site_df_department

#groupement par département, puis classement par le département ayant le + d'atouts touristiques
group_site = site_df_department.groupby("department_name")[["importance"]].sum()
group_site
group_site.sort_values("importance", ascending =False)


#même calcul que précédemment, mais pour la partie concernant les logements/lieux de villégiature
poi_df = poi_df.merge (georef_df, on=["municipality_code"])
poi_df.head(5)


#sélection des colonnes dont on aura besoin pour le calcul
poi_df_department = poi_df[["poi", "municipality_code", "importance", "department_name"]]
poi_df_department


#groupement par département, puis classement par le département ayant le + de logements/lieux de villégiature
group_poi = poi_df_department.groupby("department_name")[["importance"]].sum()
group_poi
group_poi.sort_values("importance", ascending =False)


#ajout des 2 calculs d'importance
department_merged_df = group_poi.merge (group_site, on=["department_name"])
#department_merged_df["somme_importance"]=department_merged_df["importance_x"]+department_merged_df["importance_y"]
#department_merged_df = department_merged_df.drop(columns=["importance_x", "importance_y"])
#department_merged_df
#department_merged_df.sort_values("somme_importance", ascending =False)
department_merged_df



# ##### 2. REAL ESTATE
# 2.1 calcul du loyer au m2 médian par municipality_code
rental_med = real_estate_df [["municipality_code", "rental_med_all"]]
rental_med

#calcul du prix d'achat au m2 médian par municipality_code
sales_df
sales_df_grouped = sales_df.groupby(["municipality_code"])[["sales_amount", "surface", "premise_type"]].agg({"sales_amount": "sum", "surface": "sum", "premise_type": "count"})
sales_df_grouped = pd.DataFrame (sales_df_grouped)
sales_df_grouped


#jointure pour rajouter dans cette table le loyer médian par municipality_code
sales_df
real_estate_grouped = sales_df_grouped.merge(rental_med, on="municipality_code")
real_estate_grouped


#ajout du nom du département correspondant à chaque municipality code
real_estate_department = real_estate_grouped.merge(georef_df, on="municipality_code")
real_estate_department
real_estate_department = real_estate_department [["municipality_code", "sales_amount", "surface", "rental_med_all", "department_name", "premise_type"]]


real_estate_department


#calcul du prix au m2 par département
average_price_per_m2 = real_estate_department.groupby(["department_name"])[["sales_amount", "surface"]].agg({"sales_amount": "sum", "surface": "sum"})
average_price_per_m2
average_price_per_m2["average_price_per_m2"] = average_price_per_m2["sales_amount"]/average_price_per_m2["surface"]
average_price_per_m2.sort_values("average_price_per_m2")


#calcul du loyer médian par départment
real_estate_department["intermediate_sum"]=real_estate_department["rental_med_all"]*real_estate_department["premise_type"]
real_estate_department
average_rental = real_estate_department.groupby(["department_name"])[["intermediate_sum", "premise_type"]].agg({"intermediate_sum": "sum", "premise_type": "sum"})
average_rental
average_rental["average_rental"]= average_rental["intermediate_sum"]/average_rental["premise_type"]
average_rental


#regroupement des colonnes avec le loyer moyen au m2 par département et le prix d'achat au m2 moyen par département
yield_calculation = average_price_per_m2.merge(average_rental, on="department_name")
yield_calculation
yield_calculation = yield_calculation.drop(columns=["sales_amount", "surface", "intermediate_sum", "premise_type"])
yield_calculation["yield_rate"]=yield_calculation["average_rental"]*12/yield_calculation["average_price_per_m2"]*100
yield_calculation.sort_values("yield_rate", ascending=True)


#Informations sur la rentabilité locative
yield_calculation


# 2.2 calcul de la variation entre 2018 et 2021

#ajout d'une colonne "year"
sales_df.info()
sales_df["year"]=sales_df["sales_date"].dt.year

#merge pour rajouter le département
sales_info_per_department = sales_df.merge (georef_df, on=["municipality_code"])
sales_info_per_department

#filtre uniquement sur les années 2020 et 2021 (car ce sont les seules années où nous avons toutes les informations)
sales_info_per_department = sales_info_per_department[sales_info_per_department['year'].isin([2020, 2021])]
sales_info_per_department

#groupement par année et par département
sales_df_per_year = sales_info_per_department.groupby(["department_name", "year"])[["sales_amount", "surface"]].agg({"sales_amount": "sum", "surface": "sum"})
sales_df_per_year


#calcul du prix moyen au m2
sales_df_per_year["average_price_m2"]=sales_df_per_year["sales_amount"]/sales_df_per_year["surface"]
sales_df_per_year
sales_df_per_year.head(50)

#calcul de l'évolution entre 2018 et 2021
sales_df_per_year['price_m2_growth'] = sales_df_per_year.groupby('department_name')['average_price_m2'].pct_change()
sales_df_per_year

#calcul final de l'évolution
sales_df_per_year = sales_df_per_year.dropna()
sales_df_per_year.drop (columns=["sales_amount", "surface"])
sales_df_per_year.sort_values ("price_m2_growth", ascending=False)

#calcul du nb de maisons vacantes en 2019
stock_df_2018 = stock_df[stock_df['year'].isin([2018])]
stock_df_2018
stock_df_2018 = stock_df_2018.merge (georef_df, on=["municipality_code"])
vacants_housing_per_department = stock_df_2018.groupby("department_name")["nb_vacants_housing"].sum()
vacants_housing_per_department = pd.DataFrame(vacants_housing_per_department)
vacants_housing_per_department


# 2.3 taxe d'habitation sur les maisons secondaires par département
TAX_FILENAME = 'taxe_habitation.xlsx'

tax_df = pd.read_excel(os.path.join(DATA_PATH, TAX_FILENAME))
tax_df.head()
tax_df = tax_df.rename(columns={'RÉGIONS': 'department_name'})
tax_df


# ##### 3. SECONDARY HOME
# 3.1 Superficie moyenne des logements vendus par départements

# Joindre les informations de géolocalisation pour obtenir les départements
real_estate_sales_dep = sales_df.merge(
    georef_df[['municipality_code', 'department_code', 'department_name']],
    on='municipality_code'
)

# Calculer la surface moyenne des logements vendus par département
average_surface_municipality = real_estate_sales_dep.groupby('department_name')['surface'].mean().reset_index()
average_surface_municipality



# 3.2 Évolution du % des maisons secondaires par département
# Filtrer les données pour les années 2008 et 2018
housing_2008 = stock_df[stock_df['year'] == 2008]
housing_2018 = stock_df[stock_df['year'] == 2018]

# Renommer les colonnes pour les années spécifiques
housing_2008 = housing_2008[['municipality_code', 'nb_second_home']].rename(columns={'nb_second_home': 'nb_second_home_2008'})
housing_2018 = housing_2018[['municipality_code', 'nb_second_home']].rename(columns={'nb_second_home': 'nb_second_home_2018'})

# Joindre les données pour les années 2008 et 2018 sur le code de municipalité
secondary_home_rate_comparison = housing_2008.merge(housing_2018, on='municipality_code')

# Joindre les informations de géolocalisation pour obtenir les départements
secondary_home_rate_comparison = secondary_home_rate_comparison.merge(
    georef_df[['municipality_code', 'department_code', 'department_name']],
    on='municipality_code'
)

# Calculer l'évolution moyenne du pourcentage de maisons secondaires par département
secondary_home_rate_evolution_department = secondary_home_rate_comparison.groupby(['department_name'])[['nb_second_home_2008', "nb_second_home_2018"]].agg({'nb_second_home_2008': "sum", "nb_second_home_2018": "sum"})
secondary_home_rate_evolution_department["evolution_secondary_homes"]=((secondary_home_rate_evolution_department["nb_second_home_2018"]-secondary_home_rate_evolution_department["nb_second_home_2008"])/secondary_home_rate_evolution_department["nb_second_home_2008"])*100
secondary_home_rate_evolution_department.head(50)

# 3.3 taxe d'habitation sur les maisons secondaires par département
TAX_FILENAME = 'taxe_habitation.xlsx'

tax_df = pd.read_excel(os.path.join(DATA_PATH, TAX_FILENAME))
tax_df.head()
tax_df = tax_df.rename(columns={'RÉGIONS': 'department_name'})
tax_df


# ##### 4. LIFE QUALITY
# 4.1 Professionnels de santé pour 100 000 habitants par départements en 2023
DATA_PATH = '../data/cleaned'
HEALTH_FILENAME = 'health_df_cleaned.csv'

health_df = pd.read_csv(os.path.join(DATA_PATH, HEALTH_FILENAME))
health_df.head(50)

# 4.2 Taux de criminalité pour 1000 habitants par départements en 2020
CRIMINALITY_FILENAME = 'criminality_df_cleaned.csv'

criminality_df = pd.read_csv(os.path.join(DATA_PATH, CRIMINALITY_FILENAME))

# Convertir criminality_per_1000 en type numérique (si nécessaire)
criminality_df['criminality_per_1000'] = pd.to_numeric(criminality_df['criminality_per_1000'].str.replace(',', '.'))

# Agréger georef_df par département_name pour obtenir une seule ligne par département
georef_aggregated = georef_df.groupby('department_name').first().reset_index()

# Effectuer une fusion (merge) pour ajouter department_code à criminality_aggregated en utilisant department_name comme clé
criminality_aggregated = criminality_df.groupby('department_name')['criminality_per_1000'].mean().reset_index()
criminality_per_department = criminality_aggregated.merge(georef_aggregated[['department_name', 'department_code']], on='department_name')

# Afficher les premières lignes du dataframe mis à jour
criminality_per_department.tail(50)


# 4.3 Nombre de jours de soleil par an par départements
SUNNY_FILENAME = 'heures_ensoleillement.xlsx'

sunny_df = pd.read_excel(os.path.join(DATA_PATH, SUNNY_FILENAME))
sunny_df.head()
sunny_df = sunny_df.rename(columns={'Départements Français et Dom Tom': 'department_name'})
sunny_df
sunny_df_per_department = sunny_df.drop (columns=["Num dép", "Classement"])
sunny_df_per_department.tail(50)


# # 🚀 ENRICHED EXPORT
# Chemin du dossier où les fichiers seront enregistrés
output_folder = "../data/enriched"
os.makedirs(output_folder, exist_ok=True)


# Liste des DataFrames et leurs noms
dataframes = {
    "num_sites_per_department": num_sites_per_department,
    "tourism_category_per_department": tourism_category_per_department,    
    "average_price_per_m2_per_department": avg_price_per_m2_per_department,
    "total_stock_per_department": total_stock_per_department,    
    "average_surface_per_department": average_surface_per_department,
    "secondary_home_rate_per_department": secondary_home_rate_per_department,
    "secondary_home_rate_evolution_department": secondary_home_rate_evolution_department,
    "vacants_housing_per_department": vacants_housing_per_department,
    "avg_salary_per_department": avg_salary_per_department,
    "health_df_per_derpartment": health_df,
    "criminality_per_department": criminality_per_department,
    "sunny_df_per_department": sunny_df_per_department,
    "life_quality_df": life_quality_df
    "taxe_habitation_per_department": tax_df,
}

# Exportation des DataFrames en CSV
for name, df in dataframes.items():
    output_path = os.path.join(output_folder, f"{name}_enriched.csv")
    df.to_csv(output_path, index=False)
    print(f"DataFrame {name} exporté vers {output_path}")


# # SCORING
# ##### 1. TOURISM
department_merged_df["ranking_hosting"]= department_merged_df["importance_x"]
department_merged_df["ranking_touristic_sites"]= department_merged_df["importance_y"]
calculation_tourism_scoring = department_merged_df.drop (columns=["importance_x", "importance_y"])
calculation_tourism_scoring


# ##### 2. REAL ESTATE
#fusion des différents dataframes pour réaliser le scoring
real_estate_scoring_merge_1 = yield_calculation.merge(sales_df_per_year, on="department_name")
real_estate_scoring_merge_2 = real_estate_scoring_merge_1.merge(vacants_housing_per_department, on="department_name")
real_estate_scoring_merge_2
#fusion du dernier dataframe
real_estate_scoring_merge_3 = real_estate_scoring_merge_2.merge(tax_df, on="department_name")
real_estate_scoring_merge_3
real_estate_scoring_merge_3 = real_estate_scoring_merge_3.drop(columns=["average_price_per_m2","sales_amount","surface","average_price_m2","average_rental","Nombre d'avis d'impôt"
])
real_estate_scoring_merge_3
#éléments pour le calcul du scoring immo
calculation_real_estate_scoring = real_estate_scoring_merge_3
calculation_real_estate_scoring.head(50)
calculation_real_estate_scoring["Taxe d'habitation moyenne en 2023"].astype(float)
calculation_real_estate_scoring.tail(50)
calculation_real_estate_scoring = calculation_real_estate_scoring.drop(columns="Taxe d'habitation moyenne en 2023")
calculation_real_estate_scoring

# ##### 3. SECONDARY HOME
#fusion des différents dataframes pour réaliser le scoring
calculation_secondary_home_scoring_merge_1 = average_surface_municipality.merge(secondary_home_rate_evolution_department, on="department_name")
calculation_secondary_home_scoring_merge_2 = calculation_secondary_home_scoring_merge_1.merge(tax_df, on="department_name")
calculation_secondary_home_scoring_merge_2
calculation_secondary_home_scoring=calculation_secondary_home_scoring_merge_2.drop (columns=["nb_second_home_2008", "nb_second_home_2018", "Nombre d'avis d'impôt"])
calculation_secondary_home_scoring


# ##### 4. LIFE QUALITY
# MERGE DES 3 DF
life_quality_df = sunny_df_per_department.merge(criminality_per_department, on='department_name', how='inner')
life_quality_df = life_quality_df.merge(health_df, on='department_name', how='outer')
# Remplacer les NaN par des valeurs nulles
life_quality_df = life_quality_df.fillna(0)  # Vous pouvez remplacer 0 par d'autres valeurs par défaut si nécessaire
# Supprimer les colonnes redondantes department_code_x et department_code_y
life_quality_df = life_quality_df.drop(columns=['department_code_x', 'department_code_y', "ensemble des médecins", "dont généralistes", "dont spécialistes", "chirurg. dentistes", "pharm."])
calculation_life_quality_scoring = pd.DataFrame (life_quality_df)
calculation_life_quality_scoring.tail(50)
#modification des 3 lignes nulles (je n'ai pas compris pourquoi elles l'étaient)
calculation_life_quality_scoring.at[21,"criminality_per_1000"]=36.72
calculation_life_quality_scoring.at[22,"criminality_per_1000"]=30.92
calculation_life_quality_scoring.at[21,"Ensoleillement (heures)"]=1789
calculation_life_quality_scoring.at[22,"Ensoleillement (heures)"]=1512
calculation_life_quality_scoring.at[92,"Ensoleillement (heures)"]=1719
calculation_life_quality_scoring.at[92,"criminality_per_1000"]=43.79


# # **SCALING**
# ##### 1. TOURISM
scaler = MinMaxScaler()
#scaling pour calculer le scoring
calculation_tourism_scoring_numeric = calculation_tourism_scoring.select_dtypes(include="number")
df_scaled_tourism = scaler.fit_transform(calculation_tourism_scoring_numeric)
df_scaled_tourism = pd.DataFrame(df_scaled_tourism, columns=calculation_tourism_scoring_numeric.columns, index=calculation_tourism_scoring.index)
df_scaled_tourism.head(50)

#cleaning des différents KPI
df_scaled_tourism['ranking_hosting'] = round(df_scaled_tourism['ranking_hosting'], 2)
df_scaled_tourism['ranking_touristic_sites'] = round(df_scaled_tourism['ranking_touristic_sites'], 2)
df_scaled_tourism


# ##### 2. REAL ESTATE
#scaling pour calculer le scoring
calculation_real_estate_scoring_numeric = calculation_real_estate_scoring.select_dtypes(include="number")
scaler = MinMaxScaler()
df_scaled_real_estate = scaler.fit_transform(calculation_real_estate_scoring_numeric)
df_scaled_real_estate = pd.DataFrame(df_scaled_real_estate, index=real_estate_scoring_merge_2.index, columns=calculation_real_estate_scoring_numeric.columns)
df_scaled_real_estate


#cleaning des différents KPI
df_scaled_real_estate['yield_rate'] = round(df_scaled_real_estate['yield_rate'], 2)
df_scaled_real_estate['price_m2_growth'] = round(df_scaled_real_estate['price_m2_growth'], 2)
df_scaled_real_estate['nb_vacants_housing'] = round(df_scaled_real_estate['nb_vacants_housing'], 2)
df_scaled_real_estate

calculation_real_estate_scoring.tail(50)


# ##### 3. SECONDARY HOME
#scaling pour calculer le scoring
calculation_secondary_home_scoring_numeric = calculation_secondary_home_scoring.select_dtypes(include="number")
df_scaled_secondary_home = scaler.fit_transform(calculation_secondary_home_scoring_numeric)
df_scaled_secondary_home = pd.DataFrame(df_scaled_secondary_home, columns=calculation_secondary_home_scoring_numeric.columns, index=calculation_secondary_home_scoring["department_name"])
df_scaled_secondary_home.head(50)

#cleaning des différents KPI
df_scaled_secondary_home['surface'] = round(df_scaled_secondary_home['surface'], 2)
df_scaled_secondary_home['evolution_secondary_homes'] = round(df_scaled_secondary_home['evolution_secondary_homes'], 2)
df_scaled_secondary_home["Taxe d'habitation moyenne en 2023"] = round(1 - df_scaled_secondary_home["Taxe d'habitation moyenne en 2023"], 2)
df_scaled_secondary_home


# ##### 4. LIFE QUALITY
#scaling pour calculer le scoring
calculation_life_quality_scoring_numeric = calculation_life_quality_scoring.select_dtypes(include="number")
df_scaled_life_quality = scaler.fit_transform(calculation_life_quality_scoring_numeric)
df_scaled_life_quality = pd.DataFrame(df_scaled_life_quality, columns=calculation_life_quality_scoring_numeric.columns, index=calculation_life_quality_scoring["department_name"])
df_scaled_life_quality.tail(50)
#cleaning des différents KPI
df_scaled_life_quality['Ensoleillement'] = round(df_scaled_life_quality['Ensoleillement (heures)'], 2)
df_scaled_life_quality['Criminality'] = round(1 - df_scaled_life_quality['criminality_per_1000'], 2)
df_scaled_life_quality['Health'] = round(df_scaled_life_quality['ensemble des médecins.1'], 2)
df_scaled_life_quality = df_scaled_life_quality.drop(columns=["Ensoleillement (heures)", "criminality_per_1000", "ensemble des médecins.1"])
df_scaled_life_quality


# # **NORMALIZATION**
# ##### 1. TOURISM
tourism_scoring = pd.DataFrame()
tourism_scoring['Hosting_score'] = df_scaled_tourism['ranking_hosting']*10
tourism_scoring['Touristic_sites_score'] = df_scaled_tourism['ranking_touristic_sites']*10
tourism_scoring['Global_tourism_score'] = round((tourism_scoring['Hosting_score'] + tourism_scoring['Touristic_sites_score'])/2,1)
tourism_scoring.sort_values("Global_tourism_score", ascending=False).head()


# ##### 2. REAL ESTATE
real_estate_scoring= pd.DataFrame()
real_estate_scoring['Rentability_score'] = df_scaled_real_estate['yield_rate']*10
real_estate_scoring['Growth_score'] = df_scaled_real_estate['price_m2_growth']*10
real_estate_scoring['Vacancy_score'] = df_scaled_real_estate['nb_vacants_housing']*10
real_estate_scoring['Global_real_estate_score'] = round((real_estate_scoring['Rentability_score'] + real_estate_scoring['Growth_score'] + (real_estate_scoring['Vacancy_score']/2))/2.5,1)
real_estate_scoring.sort_values("Global_real_estate_score", ascending=False).head()


# ##### 3. SECONDARY HOME
secondary_home_scoring= pd.DataFrame()
secondary_home_scoring['Surface_score'] = df_scaled_secondary_home['surface']*10
secondary_home_scoring['Secondary_home_growth_score'] = df_scaled_secondary_home['evolution_secondary_homes']*10
secondary_home_scoring['Tax_score'] = df_scaled_secondary_home["Taxe d'habitation moyenne en 2023"]*10
secondary_home_scoring['Global_secondary_home_score'] = round(((secondary_home_scoring['Surface_score']/2) + secondary_home_scoring['Secondary_home_growth_score'] + secondary_home_scoring['Tax_score'])/2.5,1)
secondary_home_scoring.sort_values("Global_secondary_home_score", ascending=False).head()


# ##### 4. LIFE QUALITY
life_quality_scoring= pd.DataFrame()
life_quality_scoring['Sun_score'] = df_scaled_life_quality['Ensoleillement']*10
life_quality_scoring['Safety_score'] = df_scaled_life_quality['Criminality']*10
life_quality_scoring['Health_score'] = df_scaled_life_quality["Health"]*10
life_quality_scoring['Global_life_quality_score'] = round(((life_quality_scoring['Sun_score'])/2 + life_quality_scoring['Safety_score'] + life_quality_scoring['Health_score'])/2.5,1)
life_quality_scoring.sort_values("Global_life_quality_score", ascending=False).head()


# ##### 5. GLOBAL SCORE
global_scoring_merge_1 = tourism_scoring.merge(real_estate_scoring, on="department_name")
global_scoring_merge_2 = global_scoring_merge_1.merge(secondary_home_scoring, on="department_name")
global_scoring_merge_3 = global_scoring_merge_2.merge(life_quality_scoring, on="department_name")
global_scoring_merge_3["Global_scoring"]= round((global_scoring_merge_3["Global_tourism_score"]+global_scoring_merge_3["Global_real_estate_score"]+global_scoring_merge_3["Global_secondary_home_score"]+global_scoring_merge_3["Global_life_quality_score"])/4,1)
global_scoring_table=global_scoring_merge_3
global_scoring_table.sort_values("Global_scoring", ascending=False).head(25)
#rajout dans le tableau "global score" de toutes les informations sur les départements qui ont permis de calculer le Global Score
global_scoring_info_merge_1 = global_scoring_table.merge(calculation_real_estate_scoring, on="department_name", how="outer")
global_scoring_info_merge_2 = global_scoring_info_merge_1.merge(calculation_secondary_home_scoring, on="department_name", how="outer")
global_scoring_info_merge_3 = global_scoring_info_merge_2.merge(calculation_life_quality_scoring, on="department_name", how="outer")


# Fonction pour remplacer les points par des virgules dans les valeurs flottantes
def replace_dot_with_comma(value):
    if isinstance(value, float):
        return str(value).replace('.', ',')
    return value

# Appliquer la fonction à toutes les cellules du DataFrame
global_scoring_info_merge_3 = global_scoring_info_merge_3.apply(lambda x: x.apply(replace_dot_with_comma))
global_scoring_info_merge_3.head(80)


# Chemin du dossier où les fichiers seront enregistrés
output_folder = "../data/enriched"
os.makedirs(output_folder, exist_ok=True)

dataframes = {
    "global_scoring_per_department": global_scoring_info_merge_3,
}



# Exportation du Global Scoring en CSV
for name, df in dataframes.items():
    output_path = os.path.join(output_folder, f"{name}_enriched.csv")
    df.to_csv(output_path, index=False)
    print(f"DataFrame {name} exporté vers {output_path}")
