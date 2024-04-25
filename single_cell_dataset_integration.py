import streamlit as st
import pandas as pd
from streamlit_modal import Modal
from hashlib import md5

# Page setup
st.set_page_config(page_title="Single Cell Sequencing Data Search", page_icon="🧫", layout="wide")

#grid for the page title and intro text
st.title("scFinder")
st.markdown(
"""
This is a simple search app for single cell sequencing dataset searching incorporating multiple sources and multiple data types.

""")

# load and cache data with following function
@st.cache_data
def load_data()->pd.DataFrame:
    df = pd.read_csv('https://nxn.se/single-cell-studies/data.tsv', sep='\t',parse_dates=["Date"]).fillna("")
    df['hash'] = df.index.astype(str)
    return df

df = load_data()

#display the data
#st.dataframe(df, hide_index=True)#, column_config={"B": None})

# Use a text_input to get the keywords to filter the dataframe
text_search = st.text_input("Search for single cell datasets", value="")

# Filter the dataframe using masks
m1 = df["Title"].str.contains(text_search)
m2 = df["Tissue"].str.contains(text_search)
df_search = df[m1 | m2]

# Show the cards
N_cards_per_row = 6
if text_search:
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
                    st.write(f"Authors: {row['Authors']}")
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