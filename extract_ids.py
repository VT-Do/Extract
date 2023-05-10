import pandas as pd
import numpy as np
import streamlit as st
import requests
import re
from bs4 import BeautifulSoup
import json
import pandas as pd
import ast
import re
from io import StringIO

st.set_page_config(layout="wide")
#st.sidebar.write('Hello')
def playstore_data(input):
    if (input!="Example: ['air.com.jogatina.ginrummy.android','air.com.jogatina.mahjong']"):
        try:
            list_bundleid=ast.literal_eval(input.strip())
        except:
            try:
                list=re.sub("[{}\]\[']", "", input.strip())
                list_bundleid=list.split(sep=',')
            except:
                st.write('Please check the input')
        for bundle_id in list_bundleid:
            try:
                url = "https://play.google.com/store/apps/details?id=" + bundle_id.strip()
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                title_element = soup.find("h1",class_=re.compile("Fd93Bb"))
                app_title = title_element.text.strip()
                app_data.append({'Bundle ID': bundle_id, 'App Title': app_title})
            except:
                try:
                    url = "https://apptopia.com/google-play/app/" + bundle_id.strip() + "/about"
                    response = requests.get(url)
                    soup = BeautifulSoup(response.text, "html.parser")
                    json_element = soup.find("script", type="application/ld+json")
                    json_data = json.loads(json_element.string)
                    app_title = json_data['name']
                    app_data.append({'Bundle ID': bundle_id, 'App Title': app_title})
                except:
                    app_data.append({'Bundle ID': bundle_id, 'App Title': '-'})	
    else:
        st.markdown(f'<h1 style="color:#de4b4b;font-size:15px;">{"Please insert input!"}</h1>', unsafe_allow_html=True)
    return app_data
	

def appstore_data(input):
    if (input!="Example: ['1331794412']"):
        try:
            list_bundleid=ast.literal_eval(input.strip())
        except:
            try:
                list=re.sub("[{}\]\[']", "", input.strip())
                list_bundleid=list.split(sep=',')
            except:
                st.write('Please check the input')
        for bundle_id in list_bundleid:
            try:
                 url = "https://apps.apple.com/it/app/apple-store/id" + str(bundle_id).strip()
                 response = requests.get(url)
                 soup = BeautifulSoup(response.text, "html.parser")
                 title_element = soup.find("h1",{"class": "product-header__title"})
                 app_title = title_element.text.strip().rstrip("\n").split("\n")[0].strip()
                 app_data.append({'Bundle ID': bundle_id, 'App Title': app_title})
            except:
                try:
                    url = "https://apptopia.com/ios/app/" + str(bundle_id).strip() + "/about"
                    response = requests.get(url)
                    soup = BeautifulSoup(response.text, "html.parser")
                    json_element = soup.find("script", type="application/ld+json")
                    json_data = json.loads(json_element.string)
                    app_title = json_data['name']
                    app_data.append({'Bundle ID': bundle_id, 'App Title': app_title})
                except:
                    app_data.append({'Bundle ID': bundle_id, 'App Title': '-'})
    else:
        st.markdown(f'<h1 style="color:#de4b4b;font-size:15px;">{"Please insert input!"}</h1>', unsafe_allow_html=True)
    return app_data
	

	
	
#download
def download(output):
    if output.shape[0]>0:
        col1, col2, col3= st.columns((7,2,2))
        with col1:	
            pd.set_option('display.max_colwidth', None)
            st.dataframe(output.reset_index(drop=True))
        with col2:
            csv = output.to_csv(index=False).encode('utf-8')
            st.download_button(
    		label="Download as CSV ⬇️",
    		data=csv,
    		file_name='data.csv',
    		mime='text/csv',
		)
            option = st.selectbox("Type",("CSV", "XLSX"))
        with col3:
            st.write('')
    else:
        st.write('')
        st.write('No output found')
   
col4, col5, col6 = st.columns((4, 7, 3))
with col4:
    st.write('')
with col5:
    st.title("Extracted Bundle IDs") 
with col6:
    st.write('')

st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#95e8a4;" /> """, unsafe_allow_html=True)
choice = st.sidebar.radio("Choose the store",('PlayStore','AppStore'), horizontal=True)
    
app_data = []

if (choice=="PlayStore"):
    list_bundleid = st.sidebar.text_area('Insert BundleIDs list', "Example: ['air.com.jogatina.ginrummy.android','air.com.jogatina.mahjong']")
    playstore_data(list_bundleid)
elif (choice=="AppStore"):
    list_bundleid = st.sidebar.text_area('Put bundleid list', "Example: ['1331794412']")
    appstore_data(list_bundleid)
        
if len(app_data) >0:
    df = pd.DataFrame(app_data)
    download(df)
