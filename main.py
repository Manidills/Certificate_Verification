from certificate import Blockchain
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import cv2 as cv
import ipfsApi

# 1. as sidebar menu

selected = option_menu("Main Menu", ["Home", 'Check'], 
    icons=['house', 'gear'], menu_icon="cast", default_index=1,  orientation="horizontal")



if selected == "Home":
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file:
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
        print(names)


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

            status = cv.imwrite(f'ouput/{certi_name}.png',img)
            print("Image written to file-system : ",status)
            res = api.add(f'ouput/{certi_name}.png')
            block.add_transaction(res)
            block.mine_block()
            
            
        st.write(block.get_chain())
        cv.destroyAllWindows()

