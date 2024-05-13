from bs4 import BeautifulSoup
import pandas as pd
from lxml import html

# Dictionary mapping categories to their respective IDs for the 'Sex' topic
kategorier_dictionary_sex = {
    "all": 9,
    "samfunnsfag": 1,
    "trinn8": 6,
    "trinn9": 5,
    "trinn10": 4,
    "aaret_rundt": 3,
}

# Dictionary mapping categories to their respective IDs for the 'Sexuality' topic
kategorier_dictionary_seksualitet = {
    "all": 7,
    "samfunnsfag": 2,
    "trinn8": 5,
    "trinn9": 4,
    "trinn10": 3,
    "aaret_rundt": 2,
}

# Dictionary mapping categories to their respective IDs for the 'Boundaries' topic
kategorier_dictionary_grenser = {
    "all": 17,
    "samfunnsfag": 1,
    "trinn8": 6,
    "trinn9": 5,
    "trinn10": 4,
    "aaret_rundt": 3,
}

# Dictionary mapping categories to their respective IDs for the 'Emotions' topic
kategorier_dictionary_følelser = {
    "all": 46,
    "samfunnsfag": 4,
    "trinn8": 22,
    "trinn9": 23,
    "trinn10": 22,
    "aaret_rundt": 7,
}

# Dictionary mapping categories to their respective IDs for the 'Puberty' topic
kategorier_dictionary_pubertet = {
    "all": 2,
    "samfunnsfag": 0,
    "trinn8": 1,
    "trinn9": 1,
    "trinn10": 1,
    "aaret_rundt": 1,
}

# Dictionary mapping categories to their respective IDs for the 'Sexual Health' topic
kategorier_dictionary_seksuell_helse = {
    "all": 3,
    "samfunnsfag": 0,
    "trinn8": 0,
    "trinn9": 0,
    "trinn10": 3,
    "aaret_rundt": 0,
}

# A list containing all the category dictionaries for different topics
kategorier_dictionary_alle = [kategorier_dictionary_sex, kategorier_dictionary_seksualitet,
                              kategorier_dictionary_følelser, kategorier_dictionary_grenser,
                              kategorier_dictionary_pubertet, kategorier_dictionary_seksuell_helse]

# List of keywords corresponding to each topic
sokeord_list = ["sex", "seksualitet", "følelser", "grenser", "pubertet", "seksuell_helse"]

# List of all categories
#kategorier_alle = list(kategorier_dictionary.keys())

# List of counts of resources for each category
#kategorier_antall = list(kategorier_dictionary.values())

# List of categories in a readable format
kategorier_alle_riktig = ["all", "Samfunnsfag", "8.trinn", "9.trinn", "10.trinn", "Året rundt"]

# List of categories related to subjects
kategorier_fag = ["aaret_rundt", "samfunnsfag"]

# List of categories related to grades
kategorier_trinn = ["trinn8", "trinn9", "trinn10"]


# Function to extract title and other information from a page
def find_title_one_page(html, sokeord):
    # Open the HTML file
    with open(html, 'r', encoding='utf-8') as fp:
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(fp, 'html.parser', from_encoding=('utf-8'))
    # CSS class for the title
    class_title_title = 'line-clamp-3 outline-0 before:absolute before:inset-0 before:rounded-2xl before:transition before:hover:shadow-lg before:focus-visible:ring'
    # Find all elements with the specified class for titles
    liststring_title_for_page = soup.find_all('a', class_=class_title_title)
    # Find all elements with the specified class for types (e.g., article, video, etc.)
    liststring_type_for_page = soup.find_all('aside')
    # Extract title, URL, and type information
    title_for_page = [title.text.strip() for title in liststring_title_for_page]
    url_for_page = [url['href'][:50] for url in liststring_title_for_page]
    url_for_page_full = [url['href'] for url in liststring_title_for_page]
    type_for_page = [TYPE.text for TYPE in liststring_type_for_page if 'Nytt' not in TYPE]
    if 'Aschehoug © 2024' in type_for_page:
        type_for_page.pop(-1)


    # Create a dictionary containing the extracted information
    Data = {
        "Tittel": title_for_page,
        "Type": type_for_page,
        "url": url_for_page,
        "url_full": url_for_page_full,
        "Dukker opp i søk": sokeord
    }

    # Create a DataFrame from the dictionary and return it
    dataframe_page = pd.DataFrame(data=Data)
    return dataframe_page


def dataframe_kategori(sokeord, kategori, antall_i_kategori):
    # Combine search keyword and category
    sokeord_kategori = f'{sokeord}/{kategori}'
    # Generate a list of paths based on the combined keyword and category and the number of pages
    path_list = [f"{sokeord_kategori}/p{y}.html" for y in range(1, antall_i_kategori+1)]

    # Collect dataframes from each page
    dataframe_sok = [find_title_one_page(path, sokeord) for path in path_list]
    title_in_search, type_in_search, url_in_search, sokeord_in_search, url_in_search_full = [], [], [], [], []

    # Iterate through dataframes to collect unique titles, types, and URLs
    for df in dataframe_sok:
        for i in range(len(list(df['url']))):
            if df.loc[i, "url"] not in url_in_search:
                title_in_search.append(df.loc[i, "Tittel"])
                type_in_search.append(df.loc[i, "Type"])
                url_in_search.append(df.loc[i, "url"])
                url_in_search_full.append(df.loc[i, "url_full"])
                sokeord_in_search.append(df.loc[i, "Dukker opp i søk"])

    # Create a DataFrame from the collected data
    Data = {
        "Tittel": title_in_search,
        "Type": type_in_search,
        "url": url_in_search,
        "url_full": url_in_search_full,
        "kategori": kategori,
        "Dukker opp i søk": sokeord_in_search
    }
    dataframe_kategori = pd.DataFrame(data=Data)
    return dataframe_kategori

# Function to collect search results for all categories for a given keyword
def dataframe_sok(sokeord, kategorier_dictionary):
    # Extract category names and their corresponding counts
    kategorier_alle = list(kategorier_dictionary.keys())
    kategorier_antall = list(kategorier_dictionary.values())

    # Collect search results for each category
    soketreff = [dataframe_kategori(sokeord, kategorier_alle[i], kategorier_antall[i]) for i in range(len(kategorier_antall))]

    # Initialize lists to store data
    fag, trinn = [], []
    title_in_search, type_in_search, url_in_search, sokeord_in_search, url_in_search_fag, url_in_search_trinn, url_in_search_full = [], [], [], [], [], [], []

    # Define categories related to subjects and grades
    kategorier_trinn = ["trinn8", "trinn9", "trinn10"]
    kategorier_fag = ["aaret_rundt", "samfunnsfag"]

    # Initialize lists to store index of categories related to subjects and grades
    index_in_trinn, index_in_fag = [], []

    # Find the index of categories related to subjects and grades
    for i in range(len(kategorier_alle)):
        if kategorier_alle[i] in kategorier_trinn:
            index_in_trinn.append(i)
        if kategorier_alle[i] in kategorier_fag:
            index_in_fag.append(i)

    # Collect URLs from categories related to grades and subjects
    for i in index_in_trinn:
        df_temp = soketreff[i]
        for url in list(df_temp['url']):
            if url not in url_in_search_trinn:
                url_in_search_trinn.append(url)
    for i in index_in_fag:
        df_temp = soketreff[i]
        for url in list(df_temp['url']):
            if url not in url_in_search_fag:
                url_in_search_fag.append(str(url))

    # Collect search results common in categories related to grades and subjects
    for df in soketreff:
        for i in range(len(list(df['url']))):
            url_temp = df.loc[i, "url"]
            if url_temp in url_in_search_fag and url_temp in url_in_search_trinn:
                if df.loc[i, "url"] not in url_in_search:
                    title_in_search.append(df.loc[i, "Tittel"])
                    type_in_search.append(df.loc[i, "Type"])
                    url_in_search.append(df.loc[i, "url"])
                    url_in_search_full.append(df.loc[i, "url_full"])
                    sokeord_in_search.append(df.loc[i, "Dukker opp i søk"])
                    trinn.append([])
                    fag.append([])

    # Collect categories for each search result
    for y in range(len(url_in_search)):
        for i in index_in_trinn:
            for j in range(len(list(soketreff[i]['url']))):
                url_temp = soketreff[i].loc[j, "url"]
                if url_temp == url_in_search[y]:
                    trinn[y].append(soketreff[i].loc[i, "kategori"])
        for i in index_in_fag:
            for j in range(len(list(soketreff[i]['url']))):
                url_temp = soketreff[i].loc[j, "url"]
                if url_temp == url_in_search[y]:
                    fag[y].append(soketreff[i].loc[j, "kategori"])

    # Create a DataFrame from the collected data
    Data = {
        "Tittel": title_in_search,
        "Type": type_in_search,
        "url": url_in_search,
        "url_full": url_in_search_full,
        "Fag": fag,
        "Trinn": trinn,
        "Dukker opp i søk": sokeord_in_search,
    }
    dataframe_sok= pd.DataFrame(data=Data)
    return dataframe_sok

# Function to collect search results for all keywords
def all_dataframe_sok(sokeord_list, kategorier_dictionary_alle):
    # Collect search results for each keyword
    soketreff = [dataframe_sok(sokeord_list[i], kategorier_dictionary_alle[i]) for i in range(len(sokeord_list))]
    title_in_search, type_in_search, url_in_search, sokeord_in_search, url_in_search_full, trinn_in_search, fag_in_search = [], [], [], [], [], [], []

    # Iterate through search results to collect unique URLs and associated information
    for df in soketreff:
        for i in range(len(list(df['url']))):
            url_temp = df.loc[i, "url"]
            if url_temp not in url_in_search:
                title_in_search.append(df.loc[i, "Tittel"])
                type_in_search.append(df.loc[i, "Type"])
                url_in_search.append(df.loc[i, "url"])
                url_in_search_full.append(df.loc[i, "url_full"])
                trinn_in_search.append(df.loc[i, "Trinn"])
                fag_in_search.append(df.loc[i, "Fag"])
                sokeord_in_search.append([])

    # Associate keywords with search results
    for y in range(len(url_in_search)):
        for i in range(len(sokeord_list)):
            for j in range(len(list(soketreff[i]['url']))):
                url_temp = soketreff[i].loc[j, "url"]
                if url_temp == url_in_search[y]:
                    sokeord_in_search[y].append(soketreff[i].loc[j, "Dukker opp i søk"])

    # Create a DataFrame from the collected data
    Data = {
        "Tittel": title_in_search,
        "Type": type_in_search,
        "url": url_in_search,
        "url_full": url_in_search_full,
        "Fag": fag_in_search,
        "Trinn": trinn_in_search,
        "Dukker opp i søk": sokeord_in_search,
    }
    dataframe_sok_full = pd.DataFrame(data=Data)
    return dataframe_sok_full


print(all_dataframe_sok(sokeord_list, kategorier_dictionary_alle))
#print(dataframe_sok(sokeord_list[0],kategorier_dictionary)["Trinn"])
#fulldataframe = [dataframe_sok(sokeord_list[i], kategorier_dictionary_alle[i]) for i in range(len(sokeord_list))]
#print(fulldataframe)

df= all_dataframe_sok(sokeord_list, kategorier_dictionary_alle)



# Read HTML content from files and store them as strings
str_sex_og_sant = [open(r'laringslop\sex og sant.html','r',encoding='utf-8').read()]
str_grenser = [open(r'laringslop\grenser.html','r',encoding='utf-8').read()]
str_if_you_kiss_a_boy = [open(r'laringslop\if you kiss a boy.html','r',encoding='utf-8').read()]
str_porno_og_parvirkning = [open(r'laringslop\porno og pavirkning.html','r',encoding='utf-8').read()]

# Initialize lists to store extracted data
full_name_sex_og_sånt = []
title_sex_og_sånt = []
url_sex_og_sånt =[]
full_name_grenser = []
title_grenser = []
url_grenser = []
title_if_you_kiss_a_boy = []
url_if_you_kiss_a_boy = []
title_porno_og_pavirkning = []
url_porno_og_pavirkning = []

# Extract data from the HTML content for 'Sex og sant'
for string in str_sex_og_sant:
    tree = html.fromstring(string)
    elements = tree.xpath("/html/body/div/div/div/main/div/div/div/div/div/nav/div/h3/a")

    # Extract title and URL
    for element in elements:
        element_string = html.tostring(element, encoding='unicode')  # Convert element to string
        full_name_sex_og_sånt.append(element_string.split(">")[-2][:-3])
        title_sex_og_sånt.append(element_string.split(">")[-2][3:-3])
        url_sex_og_sånt.append(element_string.split('"')[1])

# Extract data from the HTML content for 'Grenser'
for string in str_grenser:
    tree = html.fromstring(string)
    elements = tree.xpath("/html/body/div/div/div/main/div/div/div/div/div/nav/div/div/a")

    # Extract title and URL
    for element in elements:
        element_string = html.tostring(element, encoding='unicode')  # Convert element to string
        title_grenser.append(element_string.split('">')[-1][:-16])
        url_grenser.append(element_string.split('"')[1])

# Extract data from the HTML content for 'If You Kiss a Boy'
for string in str_if_you_kiss_a_boy:
    tree = html.fromstring(string)
    elements = tree.xpath("/html/body/div/div/div/main/div/div/div/div/div/nav/div/div/a")

    # Extract title and URL
    for element in elements:
        element_string = html.tostring(element, encoding='unicode')  # Convert element to string
        title_if_you_kiss_a_boy.append(element_string.split('">')[-1][:-16])
        url_if_you_kiss_a_boy.append(element_string.split('"')[1])

# Extract data from the HTML content for 'Porno og påvirkning'
for string in str_porno_og_parvirkning:
    tree = html.fromstring(string)
    elements = tree.xpath("/html/body/div/div/div/main/div/div/div/div/div/nav/div/div/a")

    # Extract title and URL
    for element in elements:
        element_string = html.tostring(element, encoding='unicode')  # Convert element to string
        title_porno_og_pavirkning.append(element_string.split('">')[-1][:-16])
        url_porno_og_pavirkning.append(element_string.split('"')[1])

# Lists to organize extracted data
undertema = []
sortert_undertema = []
sortert_TYPE = []
sortert_title = []
sortert_trinn = []
sortert_fag = []
sortert_url = []

# List of titles for each theme
laringslop_title = [title_sex_og_sånt, title_grenser, title_if_you_kiss_a_boy, title_porno_og_pavirkning]
tema_i_undertema = ["Sex og sånt", "Grenser", "If You Kiss a Boy", "Porno og påvirkning"]
laringslop_url = [url_sex_og_sånt, url_grenser, url_if_you_kiss_a_boy,url_porno_og_pavirkning]

i_søk= []

# Extracted data from DataFrame
title = list(df["Tittel"])
fag = list(df["Fag"])
TYPE = list(df["Type"])
url_full = list(df["url_full"])
trinn = list(df["Trinn"])
søketreff = list(df["Dukker opp i søk"])

# Loop through each theme and its titles
for i in range(len(laringslop_title)):
    for j in range(len(laringslop_title[i])):

        if j == 0 and i != 0 and tema_i_undertema[i] in title:
            index = title.index(tema_i_undertema[i])
            i_søk.append(søketreff[index])
            sortert_title.append(title[index])
            sortert_fag.append(fag[index])
            sortert_trinn.append(trinn[index])
            sortert_TYPE.append(TYPE[index])
            sortert_url.append(url_full[index])
            sortert_undertema.append(tema_i_undertema[i])

        sortert_title.append(laringslop_title[i][j])
        sortert_url.append(laringslop_url[i][j])
        sortert_undertema.append(tema_i_undertema[i])
        if laringslop_title[i][j] in title:
            index = title.index(laringslop_title[i][j])
            i_søk.append(søketreff[index])
            sortert_fag.append(fag[index])
            sortert_trinn.append(trinn[index])
            sortert_TYPE.append(TYPE[index])
        else:
            i_søk.append(["nei"])
            sortert_fag.append([])
            sortert_trinn.append([])
            sortert_TYPE.append("")

# Add remaining titles to the sorted lists
for i in range(len(title)):
    if title[i] not in sortert_title or title[i] == "Text":
        if "https://aunivers.no/sok?fullText=" not in url_full[i]:
            sortert_title.append(title[i])
            sortert_url.append(url_full[i])
            i_søk.append(søketreff[i])
            sortert_fag.append(fag[i])
            sortert_trinn.append(trinn[i])
            sortert_TYPE.append(TYPE[i])
            sortert_undertema.append("")

# Create DataFrame from the collected data
Data = {
    "Tittel": sortert_title,
    "Type": sortert_TYPE,
    "Undertema": sortert_undertema,
    "Trinn": sortert_trinn,
    "fag": sortert_fag,
    "url": sortert_url,
    "Dukker opp i søk": i_søk
}
dataframe = pd.DataFrame(data=Data)
dataframe.to_csv("aunivers.csv", sep=';')