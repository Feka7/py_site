'''
from web3 import Web3


w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/5471e52a04844eca9fcf39ee5791afc3'))
account = w3.eth.account.create()
privateKey = account.privateKey.hex()
address = account.address

print(f"Your address: {address}\nYour key: {privateKey}")
'''
