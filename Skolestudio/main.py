import streamlit as st
import pandas as pd
from lxml import html

# Set the title of the Streamlit app
st.title("Oversikt")

# Function to create a DataFrame from search results
def CreateDataFrameFromSearch(sokeord, list_flere_fag):
    # Initialize empty lists to store data
    url, title, trinn, fag, tema, type = [], [], [], [], [], []

    # Read the search results from HTML file
    str_treff = [open(f'søketreff_{sokeord}.html', 'r', encoding='utf-8').read()]

    # Loop through each search result
    for string in str_treff:
        tree = html.fromstring(string)

        # Extract URL and title
        elements = tree.xpath("/html/body/div/div/div/section/div/div/div/h2/a")
        for element in elements:
            element_string = html.tostring(element, encoding='unicode')
            url_i = element_string.split('"')[-2]
            url.append(url_i)
            title_i = element_string.split('"')[-1][1:-4]
            title.append(title_i)

        # Extract content type
        elements = tree.xpath("/html/body/div/div/div/section/div/div/div/span")
        for element in elements:
            element_string = html.tostring(element, encoding='unicode')
            type_i = element_string.split('"')[-1][1:-7]
            type.append(type_i)

        # Extract education level (trinn)
        elements = tree.xpath("/html/body/div/div/div/section/div/div/div/div/span")
        for element in elements:
            element_string = html.tostring(element, encoding='unicode')
            if "sc-bSgIji sc-eTNrTh jzhBfm" in element_string.split('"'):
                trinn_i = element_string.split('"')[-1][1:-7]
                trinn.append(trinn_i)

        # Extract subjects (fag)
        elements = tree.xpath("/html/body/div/div/div/section/div/div/div/div/span/span")
        element_string_list = []
        for element in elements:
            element_string = html.tostring(element, encoding='unicode')
            element_string_fag = element_string.split('"')[-1][8:]
            if "an>" not in str(element_string_fag):
                element_string_list.append(element_string_fag)
        for enkeltfag in element_string_list:
            fag.append([enkeltfag])

        # Combine subjects for multiple entries
        for index in list_flere_fag:
            fag[index].append(fag[index + 1][0])
            fag.pop(index + 1)

    # Filter data for specific education levels
    url_ny, title_ny, trinn_ny, fag_ny, tema_ny, type_ny = [], [], [], [], [], []
    for i in range(len(trinn)):
        if "8" in trinn[i] or "9" in trinn[i] or "10" in trinn[i]:
            trinn_ny.append(trinn[i])
            url_ny.append(url[i])
            fag_ny.append(fag[i])
            title_ny.append(title[i])
            type_ny.append(type[i])

    # Create DataFrame from filtered data
    Data = {
        "Tittel": title_ny,
        "Type": type_ny,
        "Trinn": trinn_ny,
        "fag": fag_ny,
        "url": url_ny,
        "Dukker opp i søk": sokeord
    }
    dataframe = pd.DataFrame(data=Data)
    return dataframe


# Define lists for additional subjects
list1 = [11, 23, 63]
list_flere_fag_sex = [6, 17, 18]
list_flere_fag_seksualitet = [58, 59, 60]
list_flere_fag_grenser = [12, 16, 16, 17]
list_flere_fag_seksuell_helse = [6, 16, 23]
list_flere_fag_pubertet = [0, 0, 4]
list_flere_fag_følelser = []

# Create DataFrames for different search terms
dataframe_sex = CreateDataFrameFromSearch("sex", list_flere_fag_sex)
dataframe_seksualitet = CreateDataFrameFromSearch("seksualitet", list_flere_fag_seksualitet)
dataframe_pubertet = CreateDataFrameFromSearch("pubertet", list_flere_fag_pubertet)
dataframe_grenser = CreateDataFrameFromSearch("grenser", list_flere_fag_grenser)
dataframe_seksuel_helse = CreateDataFrameFromSearch("seksuell_helse", list_flere_fag_seksuell_helse)
dataframe_følelser = CreateDataFrameFromSearch("følelser", list_flere_fag_følelser)

# Combine DataFrames and remove duplicates
dataframes = [dataframe_sex, dataframe_grenser, dataframe_seksualitet, dataframe_pubertet, dataframe_seksuel_helse,
              dataframe_følelser]
url_all, title_all, fag_all, type_all, trinn_all, sokeord_all = [], [], [], [], [], []
for dataframe in dataframes:
    for i in range(len(list(dataframe["url"]))):
        if dataframe["url"][i] not in url_all:
            url_all.append(dataframe["url"][i])
            title_all.append(dataframe["Tittel"][i])
            fag_all.append(dataframe["fag"][i])
            type_all.append(dataframe["Type"][i])
            trinn_all.append(dataframe["Trinn"][i])
            sokeord_all.append([dataframe["Dukker opp i søk"][i]])
        else:
            index = url_all.index(dataframe["url"][i])
            if dataframe["Dukker opp i søk"][i] not in sokeord_all[index]:
                sokeord_all[index].append(dataframe["Dukker opp i søk"][i])

# Create DataFrame from combined data
Data = {
    "Tittel": title_all,
    "Type": type_all,
    "Trinn": trinn_all,
    "fag": fag_all,
    "url": url_all,
    "Dukker opp i søk": sokeord_all
}
dataframe_all = pd.DataFrame(data=Data)

# Display the combined DataFrame
dataframe_all
