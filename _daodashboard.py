# -*- coding: utf-8 -*-
"""#DAODashBoard.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xUzpOCs7oLvw_BIhQil6cG0XQuCKCHmA

Video
"""

#Github API TOKEN
api_token = ''  #@param {type: "string"}

"""# DAODashBoard

**The Problem:**  There are few applications that allow to explore blockchain data collections specifically DAOs in a simple and efficient way.

**The Solution** Use data science tools that allow different actors to explore a DAO and make informed decisions.

*Use Case IPFS*
	Export to IPFS the result CVS files/graphs
*Use Case GraphQL*
	Use GraphQL to explore DAO activities @ github using Github GraphQL API

[Presentation](https://docs.google.com/presentation/d/1iJlb4ppdDnlAFhEmjU7Vsu6B0LvxC6Ow9oDl96lCyB0/edit?usp=sharing)

# DAO
DAOs are an effective and safe way to work with like-minded folks around the globe.
"""

from IPython.display import HTML
#@title Video
#@markdown <p align="left"><img src="https://bafybeierzl3pccswpdlzzvgirqa5fujkxja3xoaplgnt7ley2nadbghjsi.ipfs.dweb.link/DAOHack.png" width: 100% width= '80' alt="DAO Hacks"</p>
#0x87430F10FAD9b9Cb84056A37F836d8a804204303

HTML('<iframe width="560" height="315" src="https://www.youtube.com/embed/ByD70FKCdsI" frameborder="0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>')

"""# Use Case 
https://www.lexdao.coop
"""

from google.colab import files
import pandas as pd
import io
data_to_load = files.upload()

df = pd.read_csv(io.BytesIO(data_to_load['file.csv']))

df.describe()

df.head()

"""Identify who are the applicants of the DAO"""

applicants_ = df['applicant'].unique()
applicants_

len(applicants_)

"""Lets query their balance in Ethereum """

!pip install web3==5.23.1

from web3 import Web3, HTTPProvider
from eth_abi import decode_abi
from eth_utils import encode_hex, function_signature_to_4byte_selector


#@title DaoDashBoard
#@markdown <p align="left"><img src="https://bafybeierzl3pccswpdlzzvgirqa5fujkxja3xoaplgnt7ley2nadbghjsi.ipfs.dweb.link/DAOHack.png" width: 100% width= '80' alt="DAO Hacks"</p> 
#0x87430F10FAD9b9Cb84056A37F836d8a804204303
provider = "Ethereum" #@param ["Ethereum", "Ropsten", "Rinkeby"]
print('You selected', provider)
providerURL= 'https://ropsten.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161' #@param {type: "string"}

w3=Web3(HTTPProvider(endpoint_uri=providerURL))
connected = w3.isConnected()
query_block= w3.eth.get_block('latest')
query_block

#@markdown ****

#account = '0x87430F10FAD9b9Cb84056A37F836d8a804204303'
account = '0x87430F10FAD9b9Cb84056A37F836d8a804204303'  #@param {type: "string"}
balance = w3.eth.get_balance(account)
balance_ether = w3.fromWei(balance, 'ether')
print('Balance: ')
balance_ether

"""# IPFS

IPFS complete integration and DashBoard

"""

import requests
import json
import csv  

#Open the cvs and write to IPFS 
#as an example just the fileName
with open('file.cvs', 'w') as f:
  print(f.name)
  files = {
    'fileOne': (f.name),
  }

response = requests.post('https://ipfs.infura.io:5001/api/v0/add', files=files)
p = response.json()
hash = p['Hash']
print(hash)

# retreive
params = (
    ('arg', hash),
)
response_two = requests.post('https://ipfs.infura.io:5001/api/v0/block/get', params=params)
print(response_two.text)

"""# GraphQL"""

!pip install gql

import csv
import json
import os
import pprint

import pandas as pd
import requests

"""Last Issues Submited by in the GITHub Repo DAO"""

# get api token and set authorization

headers = {'Authorization': f'token {api_token}'}
# set url to a graphql endpoint
url = 'https://api.github.com/graphql' 

organization = 'lexDAO'  #@param {type: "string"}
author = 'LexCorpus' #@param {type: "string"}
# add a json query
query = """
{
  organization(login: "lexDAO") {
    name
    repository(name: "LexCorpus") {
        name
        issues(last: 5) {
          edges {
            node {
              number
              title
            }
          }
        }
    }
  }
}
"""

# submit the request
r = requests.post(url=url, json={'query': query}, headers=headers)

binderhub = r.json()
binderhub
issue_list = binderhub['data']['organization']['repository']['issues']['edges']
issue_list
print(f"{binderhub['data']['organization']['repository']['name']}: last five issues submitted")
for issue in issue_list:
    print(f"{issue['node']['number']:6}  {issue['node']['title']:30}")