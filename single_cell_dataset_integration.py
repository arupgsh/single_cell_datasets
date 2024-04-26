# from pandas.api.types import (
#     is_categorical_dtype,
#     is_datetime64_any_dtype,
#     is_numeric_dtype,
#     is_object_dtype,
# )
#pandas sutogenerate sliders: https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/
import streamlit as st
import pandas as pd
from streamlit_modal import Modal
import re
from hashlib import md5

# Page setup
st.set_page_config(page_title="Single Cell Sequencing Data Search", page_icon="🧫", layout="wide")

# load and cache data with following function
@st.cache_data
def load_data()->pd.DataFrame:
    df = pd.read_csv('https://nxn.se/single-cell-studies/data.tsv', sep='\t', parse_dates= ['Date']).fillna("")
    df['hash'] = df.index.astype(str)
    return df

df = load_data()

#display the data
#st.dataframe(df, hide_index=True)#, column_config={"B": None})

colX, colY, colZ = st.columns([1,2,1])

with colY:
    st.title("scFinder")
    st.markdown(
                """
                This is a simple search app for single cell sequencing dataset searching incorporating multiple sources and multiple data types.
                """)
    # Use a text_input to get the keywords to filter the dataframe
    text_search = st.text_input("", value="", placeholder= "Type the search term and press enter ... ")

# Filter the dataframe using masks
m1 = df["Title"].str.contains(text_search, flags=re.IGNORECASE)
m2 = df["Tissue"].str.contains(text_search, flags=re.IGNORECASE)
df_search = df[m1 | m2]


#st.write(df_search.head())

#Filter based on available metadata
org_list = tuple(df_search['Organism'].unique())
tech_list = tuple(df_search['Technique'].unique())
mmt_list = tuple(df_search['Measurement'].unique())

#st.write(org_list)

col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,2])

# Show the cards
N_cards_per_row = 6
if text_search:
    #Handle empty results
    if df_search.empty:
        st.markdown(f"## Nothing found for search term: {text_search}")
        #break

    with col1:
        st.markdown(f"### Filter and sort results")
    with col2:
        date_sort = st.selectbox(
        "Sort by publication date",
        ("Recent", "Oldest"),
        index=None,
        placeholder="Sort order",
        )
    with col3:
        organism_sort = st.selectbox(
            "Filter by organism",
            org_list,
            index= None,
            placeholder= "Select organism"
        )
    with col4:
        technique_sort = st.selectbox(
            "Filter by technique",
            tech_list,
            index= None,
            placeholder= "Select method"
        )
    with col5:
        measurement_sort = st.selectbox(
            "Filter by measurement",
            mmt_list,
            index= None,
            placeholder= "Select measurement"
        )
    # with col6:
    #     cell_counts = st.slider("Number of cells ", min(df_search["Reported cells total"]), max(df_search["Reported cells total"]))
    #st.write(min(df_search["Reported cells total"]))
    #st.write(max(df_search["Reported cells total"]))

    #Sort the data by date
    if date_sort == "Oldest":
        df_search = df_search.sort_values('Date', ascending = True)
    else:
        df_search = df_search.sort_values('Date', ascending = False)
    
    #Limit the search based on dropdown options
    def filter_results(df,f,v)->pd.DataFrame:
        df = df.loc[df[f] == v]
        return df
    
    if organism_sort:
        df_search = filter_results(df_search, 'Organism', organism_sort)
    if technique_sort:
        df_search = filter_results(df_search, 'Technique', technique_sort)
    if measurement_sort:
        df_search = filter_results(df_search, 'Measurement', measurement_sort)


    # if cell_counts:
    #     df_search = df_search[df_search["Reported cells total"].between(cell_counts[0], cell_counts[1])]

    #The result formatting row
    for n_row, row in df_search.reset_index().iterrows():
        i = n_row%N_cards_per_row
        if i==0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        # draw the card
        with cols[n_row%N_cards_per_row]:
            #st.caption(f"{row['Evento'].strip()} - {row['Lugar'].strip()} - {row['Fecha'].strip()} ")
            st.caption(f"{row['Date'].strftime('%Y-%m-%d')} - Type: {row['Measurement'].strip()} ")
            st.markdown(f"**[{row['Title'].strip()}](https://doi.org/{row['DOI'].strip()})**")
            st.markdown(f"*Tissue : {row['Tissue'].strip()}; Cells: {row['Reported cells total']}*")
            #st.markdown(f"*Tissue : {row['Tissue'].strip()}, Cells: {row['Reported cells total']}*")
            st.markdown(f"**Organism: {row['Organism']}**")

            modal = Modal(
                        row['Title'].strip(), 
                        key= row['hash'].strip(),
                    )

            open_modal = st.button("Details", key= row['hash'].strip())
            
            if open_modal:
                modal.open()

            if modal.is_open():
                with modal.container():
                    st.write(f"Authors: *{row['Authors']}*")
                    st.write(f"Journal : {row['Journal']}")
                    st.write(f"Technique : {row['Technique']}")
                    st.write(f"Data Accession : {row['Data location']}")
                    st.write(f"Cell source : {row['Cell source']}")
                    st.write(f"Developmental stage : {row['Developmental stage']}")
                    st.write(f"Disease : {row['Disease']}")
                    st.write(f"H5AD location : {row['H5AD location']}")


st.markdown(
"""
## Todo:

- [ ] Create unique data accession id

- [ ] Create a streamlit searchable dashboard for the data with stats
    - [X] Search box
    - [ ] Stats

- [ ] Integrate more datasets from otehr data repositories i.e. 10x data portal

- [ ] Integrate online single data analysis tools ie https://www.kanaverse.org/kana/ and more

- [ ] Delelop a mechanism for feedbacks and improvement of the database

"""
)


st.markdown("""

## Data sources

- https://www.nxn.se/single-cell-studies/

""")