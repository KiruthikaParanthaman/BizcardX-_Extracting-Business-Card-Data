import os
import cv2
import easyocr
import re
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path
from streamlit_option_menu import option_menu
import pymysql
from sqlalchemy import create_engine,text
from urllib.parse import quote
import mysql.connector

# Function to extract name and designation
def name_desg(name_text):
    name = []
    desg = []
    name.append(name_text[0])
    desg.append(name_text[1])
    return (name,desg)

#Company name extratcor
def cmp_name(vc_text):
    cmp_name = []
    vc_split = list(vc_text[-2:])
    print(vc_split)
    
    for i in range(len(vc_split)):
        if "123" in vc_split[i]:
            cmp_name.append(vc_split[i-1])
        if "www" in vc_split[i]:
            cmp_name.append(vc_split[i-1])
        if "wwW" in vc_split[i]:
            cmp_name.append(vc_split[i-1])   
    return cmp_name

#Phone number extractor
def mob(vc_text):
    mobile = []
    for i in vc_text:
        mob_regex = "([+]*\d{2,3}\D{1}\d{3}\D\d{4})"
        r = re.compile(mob_regex)
        match = re.findall(r, i)
        if match:
            mobile.append(match) 
    mobile_list = sum(mobile,[])
    return mobile_list

#gmail address extractor
def email(vc_text):
    email = []
    for i in vc_text:
        email_regex = "([a-zA-Z0-9]+@{1}[a-zA-Z0-9]+.[a-zA-Z]{3})"
        r = re.compile(email_regex)
        match = re.search(r, i)
        if match is not None:
            email.append(match.group(0))
    return email   

#Street Extractor
def street(vc_text):
    street = []
    for i in vc_text:
        street_regex = "((123)\s[A-Za-z]{3,6}\s(St))"
        r = re.compile(street_regex)
        match = re.search(r, i)
        if match is not None:
            street.append(match.group(0))
    return street

#City Extractor based on street index
def city(vc_text):
    city=[]
    State = []
    city_index = []
    index = 0
    for i in vc_text:
        street_regex = "((123)\s[A-Za-z]{3,6}\s(St))"
        r = re.compile(street_regex)
        match = re.search(r, i)
        if match is not None:
            city_index.append(index)            
        index +=1
    vc_text_split = vc_text[city_index[0]].replace(';','').split(",")
    if vc_text_split[1]!="":
        #Second split to capture city alone in strings where state merged
        vc_txt_split2 = vc_text_split[1].split()
        city.append(vc_txt_split2[0])
    else:
        city.append(vc_text_split[2])                 
    return city

#State Extractor
def state(vc_text):
    state=[]
    for i in vc_text:
        state_regex = "([A-Z]{1}[a-z]+[A-Z]{1}[a-z]+)"
        r = re.compile(state_regex)
        match = re.search(r, i)
        if match is not None:
            state.append(match.group(0))
    return state

#Pincode extractor
def pincode(vc_text):
    pincode = []
    for i in vc_text:
        pin_regex = "([0-9]{6,7})"
        r = re.compile(pin_regex)
        match = re.search(r, i)
        if match is not None:
            pincode.append(match.group(0))
    return pincode

# Function to check whether bizcardz database exists
def sql_db_check():
    mydb = mysql.connector.connect(host="localhost",user="root",password="Nila@3110")
    mycursor = mydb.cursor()
    try:
        mycursor.execute("USE Bizcardx_project")
        flag = 1
    except:
        flag = 0
    return flag

# Function to create sql table if doesn't exist
def create_sql_table():
    sql_check = sql_db_check() 
    if sql_check==0:
        mydb = mysql.connector.connect(host="localhost",user="root",password="Nila@3110")
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE Bizcardx_project")
        mydb = mysql.connector.connect(host="localhost",user="root",password="Nila@3110",database = "bizcardx_project")
        mycursor = mydb.cursor()
        mycursor.execute('''CREATE TABLE Visiting_card_details (Id INT NOT NULL AUTO_INCREMENT,Name VARCHAR(255),Designation VARCHAR(255),Company_name VARCHAR(255) ,
                            Phone_num VARCHAR(255),Email_address VARCHAR(255),Address VARCHAR(255),City  VARCHAR(255),State  VARCHAR(255),
                            Pincode INT,Image_link Text,PRIMARY KEY (iD))''')        
    return True

#Function to store image and return path
def store_image(uploaded_image):
    save_folder = r"E:/Winnie Documents/Guvi/project/Bizcard data/uploaded_images"
    save_path = Path(save_folder, uploaded_image.name)
    with open(save_path, mode='wb') as w:
        w.write(uploaded_image.getvalue())
    return save_path
      

        
#Streamlit Configuration
st.set_page_config(page_title="Business card Reader", layout="wide", initial_sidebar_state="collapsed", menu_items=None)
selected = option_menu(None, ["Home",'Modify','Delete'], icons=['house', 'pencil', 'trash3'], menu_icon="cast", default_index=0, 
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#ededed"},
        "icon": {"color": "red", "font-size": "20px"}, 
        "nav-link": {"font-color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#e6bbad"}
    })  

st.markdown("<h2 style='text-align: center; color: Black;'> Business Card Reader</h2>", unsafe_allow_html=True)
st.markdown('''<p style= 'text-align: center;'>Business card Reader app helps you to extract information from Business card image using advanced OCR Extracted details can be saved to database,modified and deleted with one click.
                Upload your business card to get started</p>''', unsafe_allow_html=True)
 
if selected == "Home":
    uploaded_image = st.file_uploader("Upload visiting card image",type=['png','jpg','jpeg'],label_visibility="hidden")
    if uploaded_image is not None:
        # To read file as bytes:
        bytes_data = uploaded_image.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        reader = easyocr.Reader(['en'],gpu = False)
        vc_coord = reader.readtext(cv2_img,paragraph="False")
        #To extract text other than name and designation
        vc_text1 = reader.readtext(cv2_img,paragraph="False",detail=0)
        
        # To extract name and designation
        vc_text2 = reader.readtext(cv2_img,paragraph=True,detail=0,y_ths=-0.01)
        for (coord,text) in vc_coord:
            (tl, tr, br, bl) = coord
            tl = (int(tl[0]), int(tl[1]))
            tr = (int(tr[0]), int(tr[1]))
            br = (int(br[0]), int(br[1]))
            bl = (int(bl[0]), int(bl[1]))
            cv2.rectangle(cv2_img,tl,br,(255,0,0),2)
        col1,col2 = st.columns([1,3])
        with col1:
              st.write("Extracted image")
              st.image(cv2_img,width = 300)
              st.write("Original image")
              st.image(uploaded_image,width = 300)

        with col2:
              with st.form("vcform", border=True):
                name,desg= name_desg(vc_text2) 
                company_name = cmp_name(vc_text1)
                phone_num = mob(vc_text1)
                phone_num_list = ",".join(phone_num)
                email_add = email(vc_text1)
                email_list = ", ".join(email_add)
                street_add = street(vc_text1)
                city_add = city(vc_text1)
                state_name = state(vc_text1)
                pincode_num = pincode(vc_text1)


                name = st.text_input("Name :",name[0].title())
                desg = st.text_input("Designation :",desg[0].title())
                comp_name = st.text_input("Company name :",company_name[0].title())                 
                mob_num = st.text_input("Phone number :",phone_num_list)
                mail = st.text_input("Email Address :",email_list)
                street_address = st.text_input("Address :",street_add[0])
                city_address = st.text_input("City :",city_add[0])
                states_name = st.text_input("State :",state_name[0])
                pincode_num = st.text_input("Pincode :",pincode_num[0])
                r1,r2,r3 = st.columns([2,1,2])
                with r2:
                        submit = st.form_submit_button(" Save ")
                        if submit:                        
                            create_sql_table()
                            mydb = mysql.connector.connect(host="localhost",user="root",password="Nila@3110",database = "bizcardx_project")
                            mycursor = mydb.cursor()
                            image_pat = store_image(uploaded_image)
                            image_path = str(image_pat)
                            query = '''INSERT INTO Visiting_card_details(Name,Designation,Company_name,Phone_num,Email_address,
                            Address,City,State,Pincode,Image_link) VALUES (%s, %s ,%s ,%s, %s, %s, %s, %s, %s ,%s)'''
                            value = (name,desg,comp_name,mob_num,mail,street_address,city_address,states_name,pincode_num,image_path)
                            mycursor.execute(query,value)
                            mydb.commit()
                            st.write('''Successful''')
#Modify page
if "Edit" not in st.session_state:
        st.session_state.Edit = False

def callback():
    st.session_state.Edit = True


if selected == "Modify":    
    col1,col2,col3 = st.columns([1,2,1])
    db_check = sql_db_check()
    if db_check == 1:
        engine = create_engine("mysql+pymysql://root:%s@localhost:3306/bizcardx_project" % quote('Nila@3110'),echo = True)
        conn = engine.connect()
        query = text('''SELECT Name FROM bizcardx_project.visiting_card_details;''')
        mysql_data = pd.read_sql(query, con=conn)
        name_list = mysql_data['Name'].to_list()            

        with col2:
            with st.form("vcform", border=True):
                vc_selected = st.selectbox("Select name to view/modify business card details",options= name_list,key="vcselected",index=None)
                st.form_submit_button("Edit")
                if st.session_state.Edit and vc_selected!= None:                    
                    values = {'vc_selected' : vc_selected }
                    query1 = text(f'''SELECT * FROM bizcardx_project.visiting_card_details WHERE Name = :vc_selected''')
                    mysql_data = pd.read_sql(query1, con=conn,params = values)
                    sql_values = mysql_data.loc[0, :].values.tolist()
                    st.text(" ")
                    name = st.text_input("Name :",sql_values[1].title())
                    desg = st.text_input("Designation :",sql_values[2].title())
                    comp_name = st.text_input("Company name :",sql_values[3].title())                 
                    mob_num = st.text_input("Phone number :",sql_values[4])
                    mail = st.text_input("Email Address :",sql_values[5])
                    street_address = st.text_input("Address :",sql_values[6])
                    city_address = st.text_input("City :",sql_values[7])
                    states_name = st.text_input("State :",sql_values[8])
                    pincode_num = st.text_input("Pincode :",sql_values[9])
                    id = sql_values[0]
                    sql_img_path = sql_values[10]
                    image = cv2.imread(sql_img_path)
                    st.image(image,width = 300)
                    save = st.form_submit_button("Save",on_click = callback())
                    if save:
                        mydb = mysql.connector.connect(host="localhost",user="root",password="Nila@3110",database = "bizcardx_project")
                        mycursor = mydb.cursor()                                     
                        mycursor.execute(f'''UPDATE bizcardx_project.visiting_card_details SET Name = "{name}", Designation = "{desg}", Company_name = "{comp_name}" ,
                                        Phone_num = "{mob_num}",Email_address = "{mail}",Address = "{street_address}" ,City = "{city_address}" ,State ="{states_name}" ,
                                        Pincode = {pincode_num}
                                        WHERE Id = {id}''')
                        mydb.commit()
                        st.write("Modified Successfully")
                        
# Delete page 
if "delt" not in st.session_state:
        st.session_state.delt = False

def callback():
    st.session_state.delt = True

if selected == "Delete":
    col1,col2,col3 = st.columns([1,2,1])
    db_check = sql_db_check()
    with col2:
        if db_check == 1:
            engine = create_engine("mysql+pymysql://root:%s@localhost:3306/bizcardx_project" % quote('Nila@3110'),echo = True)
            conn = engine.connect()
            query = text('''SELECT Name FROM bizcardx_project.visiting_card_details;''')
            mysql_data = pd.read_sql(query, con=conn)
            name_list = mysql_data['Name'].to_list()
            st.text(" ")
            st.text(" ")
            selected = st.selectbox("Choose name and click delete button to delete",options=name_list)
            if selected:
                r1,r2,r3 = st.columns(3)
                with r2:
                    delete = st.button("Delete",on_click = callback())
                    if delete:
                        mydb = mysql.connector.connect(host="localhost",user="root",password="Nila@3110",database = "bizcardx_project")
                        mycursor = mydb.cursor()                                     
                        mycursor.execute(f'''DELETE FROM bizcardx_project.visiting_card_details WHERE Name = "{selected}"''')
                        mydb.commit()        
                        st.write("Successful")
                         


# ======================================================   /   /   Completed   /   /   ====================================================== #



                        
                







    