import streamlit as st
import dask.bag as db
import requests

def fetch_data(urls):
    def fetch(url):
        response = requests.get(url)
        data = response.json() # parse response content as a dictionary
        return data
    bag = db.from_sequence(urls)
    return bag.map(fetch).compute()

urls = st.text_input('Enter URLs, one per line')
if st.button('Fetch data'):
    urls = urls.split('\n')
    data = fetch_data(urls)
    st.write(data)
