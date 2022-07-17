# Certificate_Generation_And_Validation

Sometimes organisations issue certificates for events they organize. However, the certificates can easily be forged as there are no authentication criteria. This application is a prototype for a certificate generator and validator.

# How The System Works?

The core technology for the validation is Blockchain. Each certificate is uploaded on a decentralized system IPFS and can easily be seen and accessed by anyone across the world by using a unique hash. Each certificate contains the participant's name and a unique hash. This hash and other metadata (name, IPFS unique hash) is stored onto the blockchain network. If a person wants to verify that the certificate is valid or an official certificate, the person can simply contact the organization and give them the unique hash, i.e., it is printed onto the certificate. The organisation, hence, matches the person's name and the hash onto their blockchain network and can easily verify if the certificate is official or forged.

# Accessing The Certificate

The certificate can be accessed using the link https://gateway.ipfs.io/ipfs/(your ipfs hash)

# Technology's Used

1. Blockchain
2. IPFS
3. Computer Vision

BLOCKCHAIN used for validation purpose that verifies each certificate with a unique hash (tx_hash).

IPFS used to store and retrieve the certificate and certificates metadata, the main idea behind this is to decentralize the data.

COMPUTER VISON is used on automating the certificate generation, it creates the 'N' number of the certificate based on requirements.

# Framework used

1. IPFS & INFURA [https://github.com/ipfs-shipyard/py-ipfs-http-client]

    Store the data -  
    api = ipfsApi.Client(host='https://ipfs.infura.io', port=5001)
    
    api.add(data)
    
    Retrieve via gateway url -
    https://gateway.ipfs.io/ipfs/(your ipfs hash)
    
2. OPENCV & PIL
3. SQLITE DATABASE ( To save each ipfs_hash, tx_hash and name of the file )
4. PANDAS 
5. STREAMLITE

# Deployed URL

https://manidills-certificate-verification-main-5ewbc9.streamlitapp.com/


1.HOME ( STORE & RETRIVE FROM IPFS )

    Organization should upload there xlsx file, that contain's list of name's. Then you will get the dataframe that shows IPFS HASH, NAME and TX_HASH also with download button to get certificates with participants names. ( STORE DATA TO IPFS AND RETRIVE ). It should shared with participants via mail or drive.
    
  ![Screenshot](https://i.ibb.co/19gwKWr/valid-1.png)
    
2.CHECK (RETRIVE IPFS )

    If the participants or organization want to valid or download the specific certificate, by entering the name || date to retrive the certificate from IPFS and also with IPFS URL.
    
    
  ![Screenshot](https://i.ibb.co/j58kn2J/valid-2.png)
    
    
# Downloaded File with automated all participants certificates
![Screenshot](https://i.ibb.co/Hty4Ydf/valid-3.png)


