import streamlit as st
import dask.bag as db
import requests

def fetch_data(urls):
    def fetch(url):
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
        return app_data
    bag = db.from_sequence(urls)
    return bag.map(fetch).compute()

urls = st.text_input('Enter URLs, one per line')
if st.button('Fetch data'):
    urls = urls.split('\n')
    data = fetch_data(urls)
    st.write(data)

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
