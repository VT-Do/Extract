import streamlit as st
from streamlit import SessionState


session_state = SessionState.get(col1=False, col2=False, col3=False)
col1, col2, col3 = st.beta_columns(3)
col1_one = col1.button("CARTE", key="1")
col2_one = col2.button("TABLEAU", key="2")
col3_one = col3.button("SYNTHÈSE", key="3")

if col1_one or session_state.col1:
    session_state.col1 = True
    session_state.col2 = False
    session_state.col3 = False
    sel_Map = st.selectbox("Choose Map type :", options=['Hello1', 'Hello2'], index=1)
    if sel_Map == 'Hello1':
        st.write("Hello world! 1")
    elif sel_Map == 'Hello2':
        st.write("Hello world! 2")

if col2_one or session_state.col2:
    session_state.col1 = False
    session_state.col2 = True
    session_state.col3 = False
    st.write("Hello world! 3")

if col3_one or session_state.col3:
    session_state.col1 = False
    session_state.col2 = False
    session_state.col3 = True
    st.write("Hello world! 4")
