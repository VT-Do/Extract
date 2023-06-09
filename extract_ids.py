import pandas as pd
import numpy as np
import streamlit as st
import requests
import re
from bs4 import BeautifulSoup
import json
import pandas as pd
import re
from io import StringIO
from streamlit import session_state as state


st.set_page_config(layout="wide")
if 'download_option' not in state:
    state.option = 'CSV'


def playstore_data(input):
    if (input!="Example: ['air.com.jogatina.ginrummy.android','air.com.jogatina.mahjong']"):
        try:
            list=re.sub("[{}\]\['\"]", "", input.strip())
            if '\n' in list:
                list=re.sub("[,]", "", list)
                list_bundleid=list.split(sep='\n')
                list_bundleid = [x for x in list_bundleid if  not x.isspace() and x != '' ]
            else:
                list_bundleid=list.split(sep=',')
                list_bundleid = [x for x in list_bundleid if not x.isspace() and x != '']
        except:
            st.warning('Please check the input')
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
            list=re.sub("[{}\]\['\"]", "", input.strip())
            if '\n' in list:
                list=re.sub("[,]", "", list)
                list_bundleid=list.split(sep='\n')
                list_bundleid = [x for x in list_bundleid if not x.isspace() and x != '' ]
            else:
                list_bundleid=list.split(sep=',')
                list_bundleid = [x for x in list_bundleid if not x.isspace() and x != '']
        except:
                st.warning('Please check the input')
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
	
with st.sidebar.expander("Allowed formats"):
    st.write("""BundleID1""")
    st.write("""BundleID2""")
    st.write("""BundleID3""")
    st.write("""[BundleID1,BundleID2,BundleID3]""")
    st.write("""['BundleID1','BundleID2','BundleID3']""")
    st.write("""BundleID1,BundleID2,BundleID3""")
    st.write("""'BundleID1','BundleID2','BundleID3'""")

	

if len(app_data) >0:
    output = pd.DataFrame(app_data)
    #download
    if output.shape[0]>0:
        col1, col2, col3= st.columns((7,2,2))
        with col1:	
            pd.set_option('display.max_colwidth', None)
            st.dataframe(output.reset_index(drop=True))
        with col2:
            container=st.container()
            option = st.selectbox("Type",("CSV", "XLSX"))
            if option =="CSV":
                csv = output.to_csv(index=False).encode('utf-8')
                container.download_button(
    		label="Download as "+ option+ " ⬇️",
    		data=csv,
    		file_name='output.csv',
    		mime='text/csv',
		)
            elif option =="XLSX":
                output=output.to_excel("output.xlsx",index=False)
                with open("output.xlsx", "rb") as template_file:
                    template_byte = template_file.read()
                container.download_button(label="Download as "+ option+ " ⬇️",
                        data=template_byte,
                        file_name="template.xlsx",
                        mime='application/octet-stream')
        with col3:
            st.write('')
    else:
        st.write('')
        st.write('No output found')
	# Store the value of the download option in SessionState
    state.option = option

