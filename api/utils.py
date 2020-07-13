'''
from web3 import Web3

def sendTransaction(message):
    w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/5471e52a04844eca9fcf39ee5791afc3'))
    address = '0x------'
    privateKey = '0x-----'
    nonce = w3.eth.getTransactionCount(address)
    gasPrice = w3.eth.gasPrice
    value = w3.toWei(0, 'ether')
    signedTx = w3.eth.account.signTransaction(dict(
        nonce = nonce,
        gasPrice = gasPrice,
        gas = 1000000,
        to = '0x0000000000000000000000000000000000000000',
        value = value,
        data = message.encode('utf-8')
    ), privateKey)
    tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)
    return txId
'''
