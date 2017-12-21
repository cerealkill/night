import argparse
import json
import os
import logging
import requests
import solc
import time
import web3

from requests import ReadTimeout

from lib import AsyncClientError, Spinner, logger


NAME = 'Night'
VERSION = '0.1'
BUILD = 'dec.2017'
AUTHOR = 'github.com/cerealkill/night'
V = '{n} version {v} {b} {a}'.format(n=NAME, v=VERSION, b=BUILD, a=AUTHOR)

USAGE = "night [--version] [--help] [--verbose] <command> [<args>]\n\n\
   compile   Compile a Smart Contract and save it for deployment.\n\
   deploy    Deploy a Smart Contract to a local client from memory or file.\n\
   test      Drop to an interactive console with pre loaded contract and web3.\n\n\
'night help <command>' to get help for sub commands."

DESCRIPTION = 'Night is a Ethereum smart contract compilation and deployment tool.'

HEADER = '{n} v{v}'.format(n=NAME, v=VERSION)


parser = argparse.ArgumentParser(prog=NAME, usage=USAGE, description=DESCRIPTION)
parser.add_argument("command", help="Run night --help to list commands.")

parser.add_argument('--version', action='version', version=V)
parser.add_argument("--verbose", help="Increase output verbosity.", action="store_true")
args = parser.parse_args()

print(HEADER)


if args.verbose:
    logger.level = logging.DEBUG
    logger.info("Verbosity is \033[1mON")


# ---------------------------------------------------------------------------

if args.command == 'compile':
    import compile

    try:
        compiler = compile.Solidity(compile.args.contract)
        with open(args.contract) as contract_file:
            contract_source_code = contract_file.read()

        if len(contract_source_code) < 10:
            logger.critical("File " + args.contract + " is empty.\n")
            exit()

    except FileNotFoundError as e:
        logger.critical("File not found.")
        logger.warning("Quitting.")
        exit()

    except solc.exceptions.SolcError as e:
        logger.warning("Failed to compile smart contract. Fix error bellow:\n")
        logger.exception(".")
        logger.warning("Quitting.")
        exit()

    except Exception as e:
        logger.error("Unexpected error: " + str(e))
        logger.warning("Quitting.")
        exit()


# # DEPLOY
# try:
#
#     logger.info("Connecting to ethereum client.")
#
#     # web3.py instance
#     w3 = web3.Web3(web3.HTTPProvider('http://localhost:8545'))
#
#     synced_block_str = str(w3.eth.blockNumber)
#     latest_block_obj = w3.eth.getBlock('latest')
#     latest_block_str = str(latest_block_obj.number)
#
#     if synced_block_str == latest_block_str:
#         logger.info('Synced \033[1mOK')
#     else:
#         raise AsyncClientError
#
#     logger.info("Unlocking default Account.")
#     w3.personal.unlockAccount(account=args.account, passphrase=args.password)
#     logger.warning("Account unlocked.")
#
#     logger.info("Deploying contract.")
#     # Instantiate and deploy contract
#     contract = w3.eth.contract(contract_interface['abi'], bytecode=contract_interface['bin'])
#
#     # Get transaction hash from deployed contract
#     tx_hash = contract.deploy(transaction={'from': args.account}, args=['asd', 'qwe', 'assd'])
#     logger.warning("Transaction hash: " + tx_hash)
#
#     logger.info("Waiting Tx to be mined ")
#     spinner = Spinner()
#     spinner.start()
#     for _ in range(MAX_RETRIES):
#         # Get tx receipt to get contract address
#         tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
#         if tx_receipt and tx_receipt['blockNumber']:
#             break
#         time.sleep(SECONDS_BETWEEN_RETRIES)
#     spinner.stop()
#
#     # Show the status to the user
#     if tx_receipt['status'] == 0:
#         logger.critical("Contract deployment failed. :(")
#         if tx_receipt['gasUsed'] == tx_receipt['gasSent']:
#             logger.critical("Most probably ran out of gas.")
#     else:
#         logger.warning("Contract address: " + tx_receipt['contractAddress'])
#         logger.warning("Block number: " + str(tx_receipt['blockNumber']))
#         logger.warning("Gas used: " + str(tx_receipt['gasUsed']))
#
# except (requests.exceptions.ConnectionError, ConnectionRefusedError, ReadTimeout):
#     logger.critical("Connection timed out. - Please verify that the ethereum client is running.")
#
# except AsyncClientError:
#     logger.error("ethereum client is Out of Sync. Please check the client log and try again.")
#
# except ValueError as ve:
#     message =ve.args[0]['message']
#     if message == "Unable to unlock the account.":
#         logger.error("Wrong account password.")
#     if message == "Method not found":
#         logger.error("Unable to access Personal API.")
#         logger.error("Run the ethereum client with appending flags: --jsonrpc-apis eth,net,web3,personal")
#     else:
#         logger.error("Client error message: " + message)
#
# except Exception as e:
#     logger.error("Unexpected error: " + str(e))
#
# # CLEAN UP AND QUIT
# finally:
#     try:
#         logger.info("Quitting.")
#         logger.info("Locking account.")
#         w3.personal.lockAccount(account=args.account)
#         logger.info("Account locked, Bye :)")
#
#     except (requests.exceptions.ConnectionError, ConnectionRefusedError, ReadTimeout):
#         logger.info("Connection timed out. - Please verify that the ethereum client is running.")
#
#     # Needed for Geth only. Parity unlocks the acc for a single sign.
#     except ValueError as v:
#         logger.info("All good, Bye :)")
#
#     except Exception as e:
#         logger.info("Unexpected error:", e.args[0]['message'])
