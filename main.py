import shutil
# import wget
from database import TableDba, create_db, TableModel, AccountDba, Account
import zipfile
from certificate import Blockchain
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import cv2 as cv
import ipfsApi
import os
import json
import requests

authentication_status = True


def process_file():
    st.title("Upload XLSX with list of names")
    uploaded_file = st.file_uploader("Choose a file")
    print('upload file', uploaded_file)

    if uploaded_file is not None:
        api = ipfsApi.Client(host='https://ipfs.infura.io', port=5001)
        print('api', api)
        block = Blockchain()
        block.mine_block()
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, r'output')
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        template_path = 'template_certificate.png'
        output_path = 'output/'

        font_size = 3
        font_color = (0, 0, 0)

        coordinate_y_adjustment = -30
        coordinate_x_adjustment = 10

        df = pd.read_excel(uploaded_file, engine='openpyxl')
        names = df['Name'].tolist()

        for i in names:
            print('in for')
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

            cv.putText(img, certi_name, (text_x, text_y), font, font_size, font_color, 2)
            cv.putText(img, proof, (190, 680), font, 1, font_color, 2)

            certi_path = output_path + certi_name + '.png'

            status = cv.imwrite(f'output/{certi_name}.png', img)
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
                    table_values.append({'name': val['Name'], 'ipfs_hash': val['Hash'], "tx_hash": tx_hash})
                    dynamic_model = TableModel()
                    dba = TableDba(model=dynamic_model)
                    dynamic_model.name = val['Name'].split('/')[-1].split('.')[0]
                    dynamic_model.ipfs_hash = val['Hash']
                    dynamic_model.block_chain_hash = tx_hash
                    result = dba.add_entry(dynamic_model)
                except Exception as e:
                    pass
        st.subheader("Generated_Certificates_Table")
        st.dataframe(pd.DataFrame(table_values))
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
    if st.button('clear all data'):
        dynamic_model = TableModel()
        dba = TableDba(model=dynamic_model)
        ret = dba.delete_all()
        st.write('Database clear now')


# 1. as sidebar menu

selected = option_menu("Certificate Validation", ["Home", 'Check'],
                       icons=['house', 'gear'], menu_icon="cast", default_index=1, orientation="horizontal")
create_db()
acc_dba = AccountDba()
print('default account')
acc_dba.add_default_account()


def authentication():
    authentication_status = False
    st.sidebar.subheader("Login Section")
    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password", type='password')
    if st.sidebar.button('Login'):
        print('test')
        res = acc_dba.get_by_user_name(username)
        if res:
            if res[0].get('password') == password:
                authentication_status = True
            else:
                authentication_status = False
    return authentication_status


if selected == "Home":
    # authentication_status = authentication()
    if authentication_status:
        # process_file()
        st.title("Upload XLSX with list of names")
        uploaded_file = st.file_uploader("Choose a file")

        if uploaded_file is not None:
            api = ipfsApi.Client(host='https://ipfs.infura.io', port=5001)
            block = Blockchain()
            block.mine_block()
            current_directory = os.getcwd()
            final_directory = os.path.join(current_directory, r'output')
            if not os.path.exists(final_directory):
                os.makedirs(final_directory)

            template_path = 'template_certificate.png'
            output_path = 'output/'

            font_size = 3
            font_color = (0, 0, 0)

            coordinate_y_adjustment = -30
            coordinate_x_adjustment = 10

            df = pd.read_excel(uploaded_file, engine='openpyxl')
            names = df['Name'].tolist()

            for i in names:
                print('in for')
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

                cv.putText(img, certi_name, (text_x, text_y), font, font_size, font_color, 2)
                cv.putText(img, proof, (190, 680), font, 1, font_color, 2)

                certi_path = output_path + certi_name + '.png'

                status = cv.imwrite(f'output/{certi_name}.png', img)
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
                        table_values.append({'name': val['Name'], 'ipfs_hash': val['Hash'], "tx_hash": tx_hash})
                        dynamic_model = TableModel()
                        dba = TableDba(model=dynamic_model)
                        dynamic_model.name = val['Name'].split('/')[-1].split('.')[0]
                        dynamic_model.ipfs_hash = val['Hash']
                        dynamic_model.block_chain_hash = tx_hash
                        result = dba.add_entry(dynamic_model)
                    except Exception as e:
                        pass
            st.subheader("Generated_Certificates_Table")
            st.dataframe(pd.DataFrame(table_values))
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
        if st.button('clear all data'):
            dynamic_model = TableModel()
            dba = TableDba(model=dynamic_model)
            ret = dba.delete_all()
            st.write('Database clear now')
    elif not authentication_status:
        st.error('Username / password is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your username and password')
    # if st.button('Logout'):
    #     st.session_state.authentication_status = False

if selected == "Check":
    name = st.text_input('Enter the Name')
    record_date = st.date_input('Select Date')
    wallet_address = None
    if st.checkbox('NTF Port'):
        wallet_address = st.text_area('Wallet Address')

    if st.button('search'):
        dynamic_model = TableModel()
        dba = TableDba(model=dynamic_model)
        ret = dba.get(name=name, record_date=record_date)
        record = ret.get('data')
        if len(record):
            ipfs_url = 'https://gateway.ipfs.io/ipfs/{}'.format(record[0].get('ipfs_hash'))
            st.image(ipfs_url)
            st.write(ipfs_url)
            if wallet_address:
                query_params = {
                    "chain": "rinkeby",
                    "name": "NFT_Name",
                    "description": "NFT_Description",
                    "mint_to_address": wallet_address
                }
                req = requests.get(ipfs_url, stream = True)
                os.mkdir('tmp')
                file = 'tmp/{}.png'.format(record[0].get('ipfs_hash'))
                with open(file, 'wb') as f:
                    shutil.copyfileobj(req.raw, f)

                response = requests.post(
                    "https://api.nftport.xyz/v0/mints/easy/files",
                    headers={"Authorization": "f6ce3372-a928-4947-8f50-87649f60cee2"},
                    params=query_params,
                    files={"file": file}
                )
                if response.status_code == 200:
                    res_data = json.loads(response.content.decode())
                    res_data['file_url'] = ipfs_url
                    res_data['description'] = 'Certificate metadata verification'
                    res_data['name'] = 'MetaData'

                    response_meta = requests.post(
                        "https://api.nftport.xyz/v0/metadata",
                        headers={"Authorization": "f6ce3372-a928-4947-8f50-87649f60cee2"},
                        data=json.dumps(res_data)
                    )
                    if response_meta.status_code == 200:
                        meta_url = json.loads(response_meta.content.decode())\
                            .get('metadata_uri')
                        output_data = {
                            'contract_address': res_data.get('contract_address'),
                            'transaction_hash': res_data.get('transaction_hash'),
                            'transaction_external_url': res_data.get('transaction_external_url'),
                            'mint_to_address': res_data.get('mint_to_address'),
                            'ipfs_url': ipfs_url,
                            'metadata_url': meta_url
                        }
                        st.subheader('NTF and IPFS Paths')
                        st.json(output_data)
                    else:
                        st.error('Failed to upload metadata to IPFS')
                else:
                    st.error('Failed to Minting with file')

        else:
            st.write('No record found')
