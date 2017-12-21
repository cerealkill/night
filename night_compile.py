import argparse

import os

from lib.compile import Solidity, Viper
from lib.commons import logger, NoCompilerError, Memory
from solc.exceptions import SolcError


NAME = 'Night-Compile'
DESCRIPTION = "Night compiles solidity and viper smart contracts. \
Uses file extension to detect contract language.\n"

USAGE = "night compile <file>\n\n\
i.e. \n\
night compile ~/solidity/smart_contract.sol\n\
night compile ~/viper/smart_contract.v.py\n"

parser = argparse.ArgumentParser(prog=NAME, usage=USAGE, description=DESCRIPTION)
parser.add_argument('contract', help="Path to 'sol' or 'v.py' file")
parser.add_argument('--verbose', help="Increase output verbosity.", action="store_true")
parser.add_argument('--silent', help="Only outputs errors.", action="store_true")
args = parser.parse_args()

if args.verbose and not args.silent:
    logger.level = logger.levels.DEBUG
    logger.info("High verbosity is \033[1mON")

if args.silent:
    logger.level = logger.levels.ERROR

logger.warning("-= Night Compiler =-\n")
try:
    if not os.path.exists(args.contract):
        raise FileNotFoundError("File " + args.contract + " not found.")
    # Find paths to store the compiled files
    absolute_path = os.path.abspath(args.contract)
    file_name = os.path.basename(absolute_path)
    save_path = absolute_path.rstrip(file_name)
    # Switch compiler by file extension.
    prefix, extension = os.path.splitext(args.contract)
    extension = extension.lower()
    if extension == '.sol':
        compiler = Solidity(absolute_path, save_path)
        logger.info("Selected solidity compiler.")
    elif extension.lower() == '.py' or extension.lower() == '.py':
        compiler = Viper(absolute_path, save_path)
        logger.info("Selected viper compiler.")
    else:
        raise NoCompilerError
    # Compile the contracts
    contracts = compiler.compile()
    # Save to user memory in home folder
    user_memory = Memory('.night')
    user_memory.save_memory(contracts)
    for contract in contracts:
        logger.info('Created ' + contract + '.abi and .bin in ' + save_path)
        logger.warning('Compiled: \033[1m' + contract)


except NoCompilerError as e:
    logger.critical('No compiler for the provided contract.')
    exit()

except SolcError as e:
    logger.warning("Failed to compile smart contract. Fix error bellow:\n")
    logger.exception(".")
    exit()

except Exception as e:
    logger.error("Unexpected error: " + str(e))
    exit()