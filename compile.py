import argparse
import os
import solc
import json
import lib

NAME = 'night compile'
DESCRIPTION = 'Compiles solidity and viper smart contracts.'

USAGE = "night compile [-s | --solidity] [-v | --viper] <file>\n\t\
i.e. night compile ~/solidity/smart_contract.sol\
i.e. night compile ~/viper/smart_contract.v.py\n\t\
i.e. night compile -s ~/solidity/smart_contract.sol"

parser = argparse.ArgumentParser(prog=NAME, usage=USAGE, description=DESCRIPTION)
parser.add_argument('-s', '--solidity', help="Force the compiler to use solidity.")
parser.add_argument('-v', '--viper', help="Force the compiler to use Viper.")
parser.add_argument('contract', help="Path to 'sol' or 'v.py' file")
args = parser.parse_args()


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

    def compile(self, memory=None):
        contracts = solc.compile_source(self.__source_code)
        memory = {}
        for contract in contracts:
            # extract contract name from obj
            name = contract[8:]
            # contract abi
            abi = json.dumps(contracts[contract]['abi'])
            abi_file = self.__path + name + '.abi'
            lib.save(abi_file, abi)
            # contract bytecode
            bytecode = contracts[contract]['bin']
            bin_file = self.__path + name + '.bin'
            lib.save(bin_file, bytecode)
            # contract memory for bash autocomplete
            if memory:
                memory[contract] = {'abi': contracts[contract]['abi'], 'bin': contracts[contract]['bin']}
                lib.save_memory(memory)