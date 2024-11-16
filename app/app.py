import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.title("Ventes de voiture aux Etats-Unis")

# Récupération des données depuis un fichier csv
df = pd.read_csv("./car_prices_clean.csv", delimiter = ',', encoding='utf-8')

##########################################################################################################################
# Implémenter la fonctionnalité de tri du jeu de données
##########################################################################################################################


# Menu déroulant des colonnes
colonnes = st.sidebar.selectbox( 'Trier sur cette colonne :', df.columns , placeholder = 'Choisir une colonne') # enlever valeur par défaut

# Menu déroulant ascendant/descendant
asc_desc = st.sidebar.selectbox('Type de tri', ['Croissant', 'Décroissant'], index = None, placeholder = 'Choisir un ordre')

# Tri selon la colonne sélectionnée
if colonnes :
    df = df.sort_values(by = colonnes)

    # Tri selon croissant/décroissant
    if asc_desc == 'Décroissant':
        df = df.sort_values(by = colonnes, ascending = False)

 

##########################################################################################################################
# Implémenter les fonctionnalités de filtre des lignes 
##########################################################################################################################
 

# Filtrer les lignes 

# On change le type de la colonne 'make'
df['make'] = df['make'].astype('category')

#print(df.dtypes)


# Création du input pour la marque et pour le modèle
input_mark = st.sidebar.text_input ('Marque du véhicule')
if input_mark :
    df = df[df['make'].isin([input_mark])]          # si la valeur dans la colonne est = à la valeur renseignée dans l'input c'est True  +  filtre du df pour filtrer les lignes
    print(df)

    if df.empty :
        st.error(f"Cette marque n'existe pas dans la base")
    else: 
        print("Entrée input marque valide") 
else: 
    print("Marque filtrée")


input_model = st.sidebar.text_input ('Modèle du véhicule')
if input_model :
    df = df[df['model'].isin([input_model])]
    if df.empty :
        st.error(f"Ce modèle n'existe pas dans la base")
    else: 
        print("Entrée input modèle valide") 
else: 
    print("Modèle filtré")



# Création du input pour le prix
min_price = int(df['sellingprice'].min())
max_price = int(df['sellingprice'].max())

input_price = st.sidebar.slider ('Prix', value = [min_price, max_price ])

    # Récupération des lignes 
if input_price :
    df = df[df['sellingprice'].between(left=input_price[0], right=input_price[1])]


# Création du input pour les kilomètres
min_km = int(df['odometer'].min())
max_km = int(df['odometer'].max())

input_km = st.sidebar.slider ('Kilomètres', value = [min_km, max_km ])

    # Récupération des lignes 
if input_km:
    df = df[df['odometer'].between(left=input_km[0], right=input_km[1])]





# Création du input pour la date de vente


    # Changement du type
#print(df.dtypes)
df['saledate'] = pd.to_datetime(df['saledate'], utc = True).dt.tz_convert(None)
#print(df.dtypes)

   
    # Affichage de la date de vente sans l'heure
column_config = {
    "saledate": st.column_config.DateColumn(
            "saledate",
            help="Date de la vente du véhicule",
            format="DD.MM.YYYY",
            step=1,
        ),
}

    # Input
min_date = df['saledate'].min()
max_date = df['saledate'].max()

input_date = st.sidebar.date_input ('Choisir la date de vente', value = [min_date, max_date], format = 'DD.MM.YYYY')

start_date = pd.to_datetime(input_date[0]).tz_localize(None) 
end_date = pd.to_datetime(input_date[1]).tz_localize(None)
print(type(start_date), type(end_date))

    # Récupération des lignes 
if start_date > end_date:
    st.error("La date de début doit être antérieure à la date de fin.")
else:
    df = df[df['saledate'].between(left=start_date, right=end_date)]




############################################################################################################################
# BOUTON EXCEL
############################################################################################################################

#from io import BytesIO 
# Fonction pour convertir le DataFrame en un fichier Excel 
#def to_excel(df): 
    #output = BytesIO() 
    #writer = pd.ExcelWriter(output, engine='xlsxwriter') 
    #df.to_excel(writer, index=False, sheet_name='Sheet1') 
    #writer.close() 
    #processed_data = output.getvalue() 
    #return processed_data 

#df_xlsx = to_excel(df) 

# Ajouter le bouton de téléchargement 
#st.download_button(label='Télécharger les données en Excel', 
#                   data=df_xlsx, 
#                   file_name='car_prices.xlsx', 
#                   mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')




############################################################################################################################
# Filtrage automatique en fonction du type de données (optionnel)
############################################################################################################################
col_type = df[colonnes].dtype

# Filtrer en fonction du type de colonne
if col_type == 'object' or col_type == 'category':
    # Pour les colonnes de type chaîne de caractères ou catégorie, utiliser un `selectbox`
    unique_values = df[colonnes].dropna().unique()  # Récupérer les valeurs uniques
    filter_value = st.sidebar.selectbox(f"Filtrer par {colonnes} (choisir une valeur)", unique_values, key=colonnes)
    filtered_df = df[df[colonnes] == filter_value]  # Filtrer la DataFrame par la valeur choisie

elif np.issubdtype(col_type, np.number):
    # Pour les colonnes numériques (int64, float64), utiliser un `slider`
    min_val = float(df[colonnes].min()) if not pd.isna(df[colonnes].min()) else 0
    max_val = float(df[colonnes].max()) if not pd.isna(df[colonnes].max()) else 1000000
    filter_value = st.sidebar.slider(f"Filtrer par {colonnes} (valeur numérique)", min_value=min_val, max_value=max_val, value=(min_val, max_val), key=colonnes)
    filtered_df = df[df[colonnes].between(filter_value[0], filter_value[1])]  # Filtrer selon la plage choisie

elif np.issubdtype(col_type, np.datetime64):
    # Pour les colonnes de type datetime64, utiliser un `date_input`
    min_date = df[colonnes].min().date() if not pd.isna(df[colonnes].min()) else pd.to_datetime("01-01-1900").date()
    max_date = df[colonnes].max().date() if not pd.isna(df[colonnes].max()) else pd.to_datetime("01-01-2100").date()
    filter_value = st.sidebar.date_inp5ut(f"Filtrer par {colonnes} (date)", min_value=min_date, max_value=max_date, value=(min_date, max_date), key=colonnes)
    start_date = pd.to_datetime(filter_value[0])
    end_date = pd.to_datetime(filter_value[1])
    filtered_df = df[df[colonnes].between(start_date, end_date)]  # Filtrer selon la plage de dates choisie

else:
    filtered_df = df  # Pas de filtrage pour les autres types non pris en charge



# Afficher la DataFrame filtrée
st.dataframe(filtered_df, use_container_width=True, height=600)







#for colonne in df.columns :

    # si la colonne est de type objet
 #   if df[colonne].dtype == 'object':
  #      input_filter = st.sidebar.selectbox( 'Ajouter un filtre :', pd.Series(df[colonnes]).unique(), placeholder = 'Choisir une option') 
        
    #   if input_filter :
   #     df = df[df[colonne].isin([input_filter])]


#for i, colonne in enumerate(df.columns): 
    # Si la colonne est de type object 
#    if df[colonne].dtype == 'object': 
#        unique_values = df[colonne].unique() 
#        input_filter = st.sidebar.selectbox(f'Ajouter un filtre pour {colonne} :', unique_values, index=0, key=f'filter_{i}') 
#       if input_filter: 
#            df = df[df[colonne].isin([input_filter])]


    # si la colonne est de type int
#    elif df[colonne].dtype == 'int64':
#        values_min = pd.Series(df[colonne]).min()
#        values_max = pd.Series(df[colonne]).max()
#        input_filter = st.sidebar.slider(f'Valeurs de {colonne}', value = [values_min, values_max])


############################################################################################################################
# GroupBy(optionnel)
############################################################################################################################

# Grouper selon la marque et faire la moyenne du prix de vente

# Grouper selon la marque, le modèle, trim et body  et faire la moyenne des km, du prix de vente et de l'état
#df.groupby(['make', 'model', 'trim', 'body'], as_index = False).agg( 
  #  prix_moyen = ('sellingprice', 'mean'),
 #   km_moyen = ('odometer', 'median')
#)

############################################################################################################################
# BOUTON csv
############################################################################################################################


@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


csv = convert_df(df)

st.download_button(
   "Exporter en Csv",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)




# (color interieur , color) , 
