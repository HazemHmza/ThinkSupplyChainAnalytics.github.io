# -*- coding: utf-8 -*-
"""
Created on Sat May 21 10:04:31 2022

@author: Hazem
"""


import streamlit as st  # pip install streamlit
import pandas as pd  # pip install pandas
import plotly.express as px  # pip install plotly-express
import base64  # Standard Python Module
from io import StringIO, BytesIO  # Standard Python Module





#--------------- Functions of download --------------
def generate_excel_download_link(df):
    # Credit Excel: https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/5
    towrite = BytesIO()
    df.to_excel(towrite, encoding="utf-8-sig", index=False, header=True)  # write to BytesIO buffer
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Download Excel File</a>'
    return st.markdown(href, unsafe_allow_html=True)

def generate_html_download_link(fig):
    # Credit Plotly: https://discuss.streamlit.io/t/download-plotly-plot-as-html/4426/2
    towrite = StringIO()
    fig.write_html(towrite, include_plotlyjs="cdn")
    towrite = BytesIO(towrite.getvalue().encode())
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="plot.html">Download Plot</a>'
    return st.markdown(href, unsafe_allow_html=True)


#---------- Page title ---------------
# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/

st.set_page_config(page_title="Think Supply Chain Analysis Tool",page_icon=":roller_coaster:", layout='wide')
st.title('Think Supply Chain Data Analysis Tool 📈')
st.subheader('By: Hazem Hamza ')
# st.write("[Let's Connect on LinkedIn](https://www.linkedin.com/in/hazem-hamza-mm-scm/)")
# st.write("[Watch he video from here ](https://youtu.be/criQYC4Zq70)")
# st.write("[How to handle errors video from here](https://youtu.be/COgW2lKOjSU)")
st.subheader('Upload or Drag the Excel')

# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# ------------ Uploaded File -----------

uploaded_file= st.file_uploader('Choose a XLSX File', type='xlsx')

@st.cache()
def read(file):
    df= pd.read_excel(file, engine='openpyxl')
    return df

if uploaded_file:
    st.markdown('---')
    df= read(uploaded_file )
    # st.dataframe(df)
    # groupby_column= st.selectbox(
    #     'Select the Date Column',
    #     (df.columns)
    #     )
    groupby_column= st.selectbox(
        'What would you like to analyze?',
        (df.columns)
        )
    # columnss= [groupby_column,groupby_column1]

    columns= df.columns.tolist()
    # date_column= st.text_input("Name of the Date Column")
    target_column= st.text_input("Name of Target Column (should be numerical column)")
    target_column2= st.text_input("Name of other Column (Optional and should be numerical column)")
    
    
    try:
        #-------------- Group DataFrame -----------
      if target_column2:
                # min_date= min(df[date_column])
                # max_date= max(df[date_column])
          
                # date_selection = st.slider('Date:', min_value=min(df[date_column]), max_value=max(df[date_column]), value=(min_date, max_date))  
            
                output_columns= [target_column,target_column2]
                
                df_grouped= df.groupby(groupby_column, as_index=False)[output_columns].sum()
                
                #----------- Plot Data -------------------
                fig= px.bar(
                    df_grouped,
                    x= groupby_column,
                    y= target_column,
                    color= target_column2,
                    color_continuous_scale=['red', 'yellow', 'green'],
                    
                    template='plotly_white',
                    width=1000,
                    height=600,
                    title=f'<b>{target_column} & {target_column2} by {groupby_column}</b>'
                    )
                st.plotly_chart(fig, use_container_width=True)
                            #------------- Download Section ------------
                st.subheader('Downloads:')
                generate_excel_download_link(df_grouped)
                generate_html_download_link(fig)
                                #------------- Contacts ------------------------
                # with st.container():
                #     st.write("---")
                #     st.header("Contacts")
                #     st.subheader("Hazem Hamza :wave:")
                #     st.write(" MIT Alumni Affiliate | Supply Chain Expert | Supply Chain Instructor | Data Scientist | Statistics & Operations Research | Logistics Engineering | Business Process Re-Engineering")
                #     st.write("[Let's Connect on LinkedIn >](https://www.linkedin.com/in/hazem-hamza-mm-scm/)")
                #     st.write("[YouTube Channel >](https://www.youtube.com/c/HazemHamza)")
                #     st.write("[Our Website >](https://share.streamlit.io/hazemhmza/web/app.py)")


             
        
      else:
                output_columns= target_column
                df_grouped= df.groupby(groupby_column, as_index=False)[output_columns].sum()
            #----------- Plot Data -------------------
                fig= px.bar(
                    df_grouped,
                    x= groupby_column,
                    y= target_column,
                    # color= target_column2,
                    color_continuous_scale=['red', 'yellow', 'green'],
                    template='plotly_white',
                    width=1000,
                    height=600,
                    title=f'<b>{target_column} by {groupby_column}</b>'
                    )
                st.plotly_chart(fig, use_container_width=True)          
                
                
                #------------- Download Section ------------
                st.subheader('Downloads:')
                generate_excel_download_link(df_grouped)
                generate_html_download_link(fig)
                                 
                

    except:
        st.error("Please make sure that watch the video first")
        st.write("[Watch he video from here --->](https://youtu.be/criQYC4Zq70)")
        st.write("[How to handle errors video from here >](https://youtu.be/COgW2lKOjSU)")
        # st.stop()
        
    
                 #------------- Contacts ------------------------
with st.container():
               st.write("---")
               # st.header("Contacts")
               st.subheader("Hazem Hamza :wave:")
               st.write(" MIT Alumni Affiliate | Supply Chain Expert | Supply Chain Instructor | Data Scientist | Statistics & Operations Research | Logistics Engineering | Business Process Re-Engineering")
               st.write("[LinkedIn](https://www.linkedin.com/in/hazem-hamza-mm-scm/)")
               st.write("[YouTube Channel](https://www.youtube.com/c/HazemHamza)")
               st.write("[Our Website](https://share.streamlit.io/hazemhmza/web/app.py)")   











