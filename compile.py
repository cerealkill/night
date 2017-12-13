import os
import pickle

import solc
import json


class Solidity:
    """
    Compile Solidity contracts. Outputs abi and bytecode
    :param path: Path to contract file.
    """

    def __init__(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError("File " + path + " not found.")
        absolute_path = os.path.abspath(path)
        file_name = os.path.basename(absolute_path)
        self.__path = absolute_path.rstrip(file_name)
        with open(path) as contract_file:
            self.__source_code = contract_file.read()

    def compile(self):
        contracts = solc.compile_source(self.__source_code)
        for contract in contracts:
            name = contract[8:]
            abi = json.dumps(contracts[contract]['abi'])
            abi_file = name + '.abi'
            self.save(abi_file, abi)
            bin = contracts[contract]['bin']
            bin_file = name + '.bin'
            self.save(bin_file, bin)
            contract_file = name + '.pkl'
            self.save_pickle(contract_file, contracts[contract])

    def save(self, file_name, data):
        full_path = self.__path + file_name
        with open(full_path, 'w+') as file:
            file.write(data)

    def save_pickle(self, file_name, data):
        full_path = self.__path + file_name
        pickle.dump(data, open(full_path, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
