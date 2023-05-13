import streamlit as st


col1, col2, col3 = st.beta_columns(3)
if col1.button("CARTE"):
    st.write("Hello")
    sel_Map = st.selectbox("Choose Map type :", options=['Hello1', 'Hello2'], index=1)
    if sel_Map == 'Hello1':
        st.write("Hello world! 1")

    elif sel_Map == 'Hello2':
        st.write("Hello world! 2")

if col2.button("TABLEAU"):
    st.write("Hello world! 3")

if col3.button("SYNTHÈSE"):
    st.write("Hello world! 4")
