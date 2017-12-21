import json
import web3

ACCOUNT = '0x00E27b1BB824D66d8ec926f23b04913Fe9b1Bd77'
ABI = json.loads('[{"constant": false, "inputs": [], "name": "kill", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "deviceId", "outputs": [{"name": "manufacturer", "type": "string"}, {"name": "model", "type": "string"}, {"name": "serialNumber", "type": "bytes32"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [{"name": "", "type": "uint256"}], "name": "registry", "outputs": [{"name": "timestamp", "type": "uint256"}, {"name": "value", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"name": "_timestamp", "type": "uint256"}, {"name": "_value", "type": "uint256"}], "name": "log", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"name": "_manufacturer", "type": "string"}, {"name": "_model", "type": "string"}, {"name": "_serialNumber", "type": "bytes32"}], "payable": false, "stateMutability": "nonpayable", "type": "constructor"}]')
CONTRACT = '0x2B6768D71CCc45219C381B12F4A34c41f3fc79C0'
PWD = '48qzjbhPdZnw'

w3 = web3.Web3(web3.HTTPProvider('http://localhost:8545'))

# Contract instance in concise mode
contract_instance = w3.eth.contract(ABI, CONTRACT, ContractFactoryClass=web3.contract.ConciseContract)

try:
    print('Contract value: {}'.format(contract_instance.registry()))
    print('Setting value to: Nihao')
    #w3.personal.unlockAccount(account=ACCOUNT, passphrase=PWD)
    contract_instance.greet('Nihao', transact={'from': ACCOUNT})
    print('Contract value: {}'.format(contract_instance.greet()))

except Exception as e:
    print(e)
    print('- DEU RUIM CORAI')
    pass
