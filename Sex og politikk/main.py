import streamlit as st  # Importerer Streamlit for å bygge webapplikasjonen
import pandas as pd  # Importerer pandas for å håndtere data i DataFrame
from lxml import html  # Importerer lxml for å analysere HTML-strukturer

st.title("Oversikt")  # Setter tittelen på Streamlit-siden til "Oversikt"

# Leser innholdet i HTML-filene og lagrer dem i lister
str_grenser = [open(r'Grenser - Sex og politikk.html', 'r', encoding='utf-8').read()]
str_idealer = [open(r'Idealer, normer og forventninger - Sex og politikk.html', 'r', encoding='utf-8').read()]
str_identitet = [open(r'Identitet - Sex og politikk.html', 'r', encoding='utf-8').read()]
str_kroppen = [open(r'Kroppen - Sex og politikk.html', 'r', encoding='utf-8').read()]
str_lover = [open(r'Lover og seksuelle rettigheter - Sex og politikk.html', 'r', encoding='utf-8').read()]
str_relasjoner = [open(r'Relasjoner og følelser - Sex og politikk.html', 'r', encoding='utf-8').read()]
str_sexogprev = [open(r'Sex og Prevensjon - Sex og politikk.html', 'r', encoding='utf-8').read()]

# Samler all innhold i en liste og titler på sidene i en annen liste
all_sites = [str_grenser, str_idealer, str_identitet, str_kroppen, str_lover, str_relasjoner, str_sexogprev]
all_sites_title = ['Grenser', 'Idealer, normer og forventninger', 'Identitet', 'Kroppen', 'Lover og seksuelle rettigheter', 'Relasjoner og følelser', 'Sex og prevensjon']
# Tom liste for variabler
url, title, trinn, fag, tema, kategori, treff = [],[],[],[],[],[],[]
antall_elementer = 8  # Antall elementer per treff

# Går gjennom alle HTML-sidene og henter data
for site in all_sites:
    tema_i = all_sites_title[all_sites.index(site)]
    for string in site:
        tree = html.fromstring(string)
        # Henter tittel for hvert treff
        elements = tree.xpath("/html/body/main/div/div/div/article/div/div/ul/li/a/div/h2")
        for element in elements:
            element_string = html.tostring(element, encoding='unicode')
            title_i = element_string.split('>')[1][:-4]
            title.append(title_i)
        # Henter treffinformasjon
        elements = tree.xpath("/html/body/main/div/div/div/article/div/div/ul/li/a/div/ul/li/div")
        for element in elements:
            element_string = html.tostring(element, encoding='unicode')
            treff_i = element_string.split('>')
            treff.append(treff_i)
        # Henter URL-er og tilhørende tema
        elements = tree.xpath("/html/body/main/div/div/div/article/div/div/ul/li/a")
        for element in elements:
            element_string = html.tostring(element, encoding='unicode')
            url_i = element_string.split('"')[3]
            url.append(url_i)
            tema.append(tema_i)

# Henter ut kategori og fag fra treffinformasjon
for i in range(len(treff)):
    if 'Fag</span' in treff[i]:
        kategori_i = treff[i+5][1][:-5]
        kategori.append(kategori_i)
        fag_i = treff[i + 1][1][:-5]
        fag.append(fag_i)

# Legger til tomme elementer for kategori og fag på indeks 18 for å matche antall elementer
kategori.insert(18, "")
fag.insert(18, "")
# Lager en DataFrame med den ekstraherte informasjonen
Data = {
    "Tittel": title,
    "Type": kategori,
    "Tema": tema,
    "Fag": fag,
    "URL": url,
}
dataframe = pd.DataFrame(data=Data)

dataframe  # Viser den opprettede DataFrame-en



