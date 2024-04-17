import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.markdown(
"""
## Todo:

- [ ] Create unique data accession id

- [ ] Create a streamlit searchable dashboard for the data with stats

- [ ] Integrate more datasets from otehr data repositories i.e. 10x data portal

- [ ] Integrate online single data analysis tools ie https://www.kanaverse.org/kana/ and more

- [ ] Delelop a mechanism for feedbacks and improvement of the database

"""
)

# load and cache data with following function
@st.cache_data
def load_data()->pd.DataFrame:
    df = pd.read_csv('https://nxn.se/single-cell-studies/data.tsv', sep='\t')
    return df

df = load_data()

#display the data
st.dataframe(df, hide_index=True, column_config={"B": None})