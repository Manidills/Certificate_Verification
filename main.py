import shutil
import zipfile
from certificate import Blockchain
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import cv2 as cv
import ipfsApi
import os
import glob

# 1. as sidebar menu

selected = option_menu("Main Menu", ["Home", 'Check'], 
    icons=['house', 'gear'], menu_icon="cast", default_index=1,  orientation="horizontal")



if selected == "Home":
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        api = ipfsApi.Client(host='https://ipfs.infura.io', port=5001)
        block = Blockchain()
        block.mine_block()

        template_path = 'template_certificate.png'
        output_path = 'output/'

        font_size = 3
        font_color = (0,0,0)


        coordinate_y_adjustment = -30
        coordinate_x_adjustment = 10

        df =  pd.read_excel(uploaded_file, engine='openpyxl')
        names = df['Name'].tolist()


        for i in names:
            
            proof = block.get_previous_hash()
            print(proof)
            certi_name = i
            block.add_transaction(proof)
            
            
            img = cv.imread(template_path)

            font = cv.FONT_HERSHEY_PLAIN

            text_size = cv.getTextSize(certi_name, font, font_size, 10)[0]
            text_x = (img.shape[1] - text_size[0]) / 2 + coordinate_x_adjustment
            text_y = (img.shape[0] + text_size[1]) / 2 - coordinate_y_adjustment
            text_x = int(text_x)
            text_y = int(text_y)

            cv.putText(img, certi_name, (text_x ,text_y ), font, font_size, font_color, 2)
            cv.putText(img, proof, (190 ,680), font, 1, font_color, 2)

            certi_path = output_path + certi_name + '.png'

            status = cv.imwrite(f'output/{certi_name}.png',img)
            print("Image written to file-system : ",status)
            res = api.add(f'output/{certi_name}.png')
            block.add_transaction(res)
            block.mine_block()
            
            
        data = block.get_chain()
        table_values = []
        for i in data['chain']:
            if i['transactions'] is not None:
                try:
                   val = i['transactions'][1][0]
                   tx_hash = i['transactions'][0]
                   table_values.append({'name': val['Name'], 'ipfs_hash': val['Hash'],"tx_hash": tx_hash})
                except:
                    pass
        st.write(table_values)
        shutil.make_archive('output/', 'zip', 'output/')
        with open("output.zip", "rb") as fp:
            btn = st.download_button(
                label="Download ZIP",
                data=fp,
                file_name="output.zip",
                mime="application/zip"
            )


        dir = 'output/'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        
        
