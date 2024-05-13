import pandas as pd
import streamlit as st
import ast
st.write("hello")
path = "aunivers.csv"
df = pd.read_csv(path, delimiter=";")

my_dict={"engelsk": "Engelsk",
         "fransk": "Fransk",
         "krle": "KRLE",
         "kunst_og_handverk": "Kunst og Håndverk",
         "mat_og_helse":"Mat og Helse",
         "matte":"Matematikk",
         "musikk":"Musikk",
         "naturfag": "Naturfag",
         "norsk": "Norsk",
         "samfunnsfag": "Samfunnsfag",
         "spansk":"Sapnsk",
         "trinn8": "8.Trinn",
         "trinn9": "9.Trinn",
         "trinn10": "10.Trinn",
         "tysk": "Tysk",
         "aaret_rundt": "Året Rundt",
         "":""
}

sortert_title = list(df["Tittel"])
sortert_undertema = list(df["Undertema"])
sortert_TYPE = list(df["Type"])
fag_string = list(df["fag"])
sortert_fag_orginal = [ast.literal_eval(fag) for fag in fag_string]
sortert_fag = [[my_dict.get(word, word) for word in sublist] for sublist in sortert_fag_orginal]

sortert_fag
i_søk_string = list(df["Dukker opp i søk"])
i_søk = [ast.literal_eval(søk) for søk in i_søk_string]
sortert_url = list(df["url"])
trinn_string = list(df["Trinn"])

sortert_trinn_orginal = [ast.literal_eval(trinn) for trinn in trinn_string]
sortert_trinn = [[my_dict.get(word, word) for word in sublist] for sublist in sortert_trinn_orginal]


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
dataframe