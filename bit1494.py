import streamlit as st 
import requests 
import time

st.set_page_config (
    page_title="Balance by Bitquery",
    page_icon="random",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title('Bitquery Balance API')
st.write('This web application returns the balance of an ETH, BSC or Algorand token only.')
form = st.form("bitquery")
apiKey = form.text_input('Enter your API key')
blockchain = form.selectbox('Which blockchain does your address belong to?', ('ethereum', 'bsc', 'algorand'))
address = form.text_input('Enter your address')
submitted = form.form_submit_button('Submit')

def bitqueryAPICall(query: str, api: str):  
    headers = {'X-API-KEY': api}
    request = requests.post('https://graphql.bitquery.io/', json={'query': query, 'variables': variables}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed and return code is {}.      {}'.format(request.status_code,query))

queryETHAndBSC = """
query MyQuery($network: EthereumNetwork, $address: String){
  ethereum(network: $network){
    address(address: {is: $address}){
      balance
    }
  }
}
"""

queryALGO = """ 
query MyQuery($network: AlgorandNetwork, $address: String){
  algorand(network: $network){
    address(address: {is: $address}){
      balance
    }
  }
}
"""

variables = {
	"network": blockchain,
	"address": address
}

if submitted: 
	while True:
		if apiKey != "" or apiKey != " ":
			if blockchain == "ethereum" or blockchain == "bsc": 
				result = bitqueryAPICall(queryETHAndBSC, apiKey)
				st.success('The Balance of the token is {}'.format(result['data']['ethereum']['address'][0]['balance']))
			elif blockchain == "algorand":
				result = bitqueryAPICall(queryALGO, apiKey)
				st.success('The Balance of the token is {}'.format(result['data']['algorand']['address'][0]['balance']))
		else:
			pass
		time.sleep(300)
