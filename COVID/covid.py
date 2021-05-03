import pandas as pd
import numpy as np
import json

data_file = "COVID_MX_2020_tst.xlsx"
catalog_file = "Catalogos.xlsx"
desc_file = "descriptor.json"

catalogs = {}
mappings = {}
covid_df = None


def load_files():
    global covid_df
    global mappings
    # Read the descriptor from the json file
    j_file = open(desc_file, "r")
    desc = json.loads(j_file.read())
    mappings = desc["fields"]
    load_catalogs(desc)
    j_file.close()

    print("Loading data source...")
    # Load the main data source
    xl = pd.ExcelFile(data_file)
    covid_df = xl.parse('Hoja1')
    # Describe our main data set
    # print(covid_df.index)       # Gives me the range of the indices (Number of rows)
    # Gives me rows and columns
    print("The data set contains " + str(covid_df.shape[0]) + " rows by " + str(covid_df.shape[1]) + " columns.")
    # print(covid_df.dtypes)      # Describes my data source by telling me how did pandas identify each column
    # print(covid_df.head(5))     # Prints the top n values of my data source
    print("Done.")
    print("Cleaning data...")
    merge_clean_data()
    print("Done.")
    print(covid_df.head(5))  # Prints the top n values of my data source
    # Save clean data
    covid_df.to_excel(r'export_dataframe.xlsx', index=False, header=True)


def load_catalogs(desc):
    print("Loading catalogs...")
    cat_xl = pd.ExcelFile(catalog_file)
    for i in desc["catalogs"]:
        # print("Catalogo: " + i)
        catalogs[i] = cat_xl.parse(i)
        # Clean NaN values
        catalogs[i].dropna(inplace=True)
        # Validate all the numeric columns to be integers
        dtypes = catalogs[i].dtypes.to_dict()
        if 'float64' in dtypes.values():
            for col_nam, typ in dtypes.items():
                if typ == 'float64':
                    catalogs[i][col_nam] = catalogs[i][col_nam].astype(int)
        # print(catalogs[i].dtypes)
        # print(catalogs[i].head())
    print("Done.")


def merge_clean_data():
    for fields in mappings:
        field = fields["name"]
        print(field)
        if fields["format"] == "ID":
            covid_df.set_index(field)
        elif fields["format"] == "ENTIDADES":
            catalog = catalogs[fields["format"]]
            covid_df[field].replace(catalog["CLAVE_ENTIDAD"].values, catalog["ABREVIATURA"].values, inplace=True)
        elif fields["format"] in catalogs.keys():
            catalog = catalogs[fields["format"]]
            covid_df[field].replace(catalog["CLAVE"].values, catalog["DESCRIPCIÓN"].values, inplace=True)
        # TODO: Fix the reference to the MUNICIPIOS CATALOG
        # 1. Create a unique key for every municipio in the catalog reading method
        # 2. Identify the unique key for every record in our data frame
        # TODO: Clean the values of the PAIS_NACIONALIDAD column


load_files()