import pandas as pd
import numpy as np
import streamlit as st
import requests
import re
from bs4 import BeautifulSoup
import json
import pandas as pd


st.set_page_config(layout="wide")
#st.sidebar.write('Hello')

#download
def download(output):
    if output.shape[0]>0:    
        csv = output.to_csv(index=False).encode('utf-8')
        st.download_button(
    		label="Download as CSV ⬇️",
    		data=csv,
    		file_name='data.csv',
    		mime='text/csv',
		)	
        st.dataframe(output.reset_index(drop=True),2000,1000)

    else:
        st.write('')
        st.write('No output found')
      
choice = st.sidebar.radio("Select the store",('PlayStore','AppStore'), horizontal=True)

col4, col5,col6 = st.columns((4, 7, 1))
    with col4:
        st.write('')
    with col5:
        st.title("Extracted Bundle IDs") 
    with col6:
	st.write('')

st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#95e8a4;" /> """, unsafe_allow_html=True)
    
list_bundleid = st.sidebar.text_area('Put lines here', 'Ex: [1,2]')     
app_data = []

        

if (choice=="PlayStore") and (list_bundleid!='Ex: [1,2]'):
    st.sidebar.write('Hello PlayStore')	
    
    for bundle_id in list_bundleid:
        try:
            url = "https://play.google.com/store/apps/details?id=" + bundle_id
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            title_element = soup.find("h1",class_=re.compile("Fd93Bb"))
            app_title = title_element.text.strip()
            app_data.append({'Bundle ID': bundle_id, 'App Title': app_title})
        except:
            try:
                url = "https://apptopia.com/google-play/app/" + bundle_id + "/about"
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                json_element = soup.find("script", type="application/ld+json")
                json_data = json.loads(json_element.string)
                app_title = json_data['name']
                app_data.append({'Bundle ID': bundle_id, 'App Title': app_title})
            except:
                app_data.append({'Bundle ID': bundle_id, 'App Title': '-'})	
elif (choice=="AppStore"):
    st.sidebar.write('Hello AppStore')
				 
       
	

if len(app_data) >0:
    df = pd.DataFrame(app_data)
    download(df)



