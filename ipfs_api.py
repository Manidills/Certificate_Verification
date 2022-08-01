import shutil

import ipfsApi
import os
import json
import requests
import streamlit as st



class IPFSApi:
    def __init__(self):
        pass

    def ipfs_add(self, certi_path):
        api = ipfsApi.Client(host='https://ipfs.infura.io', port=5001)
        res = api.add(certi_path)
        return res

    def nft_port_minting(self,record,wallet_address,ipfs_url):
        query_params = {
            "chain": "rinkeby",
            "name": "NFT_Name",
            "description": "NFT_Description",
            "mint_to_address": wallet_address
        }
        req = requests.get(ipfs_url, stream=True)
        if os.path.exists('tmp/'):
            shutil.rmtree('tmp/')
        os.makedirs('tmp/')
        file = 'tmp/{}.png'.format(record[0].get('ipfs_hash'))
        with open(file, 'wb') as f:
            shutil.copyfileobj(req.raw, f)

        response = requests.post(
            "https://api.nftport.xyz/v0/mints/easy/files",
            headers={"Authorization": "f6ce3372-a928-4947-8f50-87649f60cee2"},
            params=query_params,
            files={"file": file}
        )
        res_data = []
        if response.status_code == 200:
            res_data = json.loads(response.content.decode())
            res_data['file_url'] = ipfs_url
            res_data['description'] = 'Certificate metadata verification'
            res_data['name'] = 'MetaData'
            return res_data
        else:
            st.error('Failed to Minting with file')
            return res_data

    def upload_metadata_to_ipfs(self, data, ipfs_url):
        response_meta = requests.post(
            "https://api.nftport.xyz/v0/metadata",
            headers={"Authorization": "f6ce3372-a928-4947-8f50-87649f60cee2"},
            data=json.dumps(data)
        )
        if response_meta.status_code == 200:
            meta_url = json.loads(response_meta.content.decode()) \
                .get('metadata_uri')
            output_data = {
                'contract_address': data.get('contract_address'),
                'transaction_hash': data.get('transaction_hash'),
                'transaction_external_url': data.get('transaction_external_url'),
                'mint_to_address': data.get('mint_to_address'),
                'ipfs_url': ipfs_url,
                'metadata_url': meta_url
            }
            st.subheader('NTF and IPFS Paths')
            st.json(output_data)
        else:
            st.error('Failed to upload metadata to IPFS')