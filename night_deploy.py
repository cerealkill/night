import time
import web3

from lib import AsyncClientError, Spinner, logger

MAX_RETRIES = 100
SECONDS_BETWEEN_RETRIES = 5


# DEPLOY
try:

    logger.info("Connecting to ethereum client.")

    # web3.py instance
    w3 = web3.Web3(web3.HTTPProvider('http://localhost:8545'))

    synced_block_str = str(w3.eth.blockNumber)
    latest_block_obj = w3.eth.getBlock('latest')
    latest_block_str = str(latest_block_obj.number)

    peers = w3.net.peerCount

    if synced_block_str != latest_block_str or peers < 5:
        logger.info('Synced \033[1mOK')
    else:
        raise AsyncClientError

    logger.info("Unlocking default Account.")
    w3.personal.unlockAccount(account=args.account, passphrase=args.password)
    logger.warning("Account unlocked.")

    logger.info("Deploying contract.")
    # Instantiate and deploy contract
    contract = w3.eth.contract(contract_interface['abi'], bytecode=contract_interface['bin'])

    # Get transaction hash from deployed contract
    tx_hash = contract.deploy(transaction={'from': args.account}, args=['asd', 'qwe', 'assd'])
    logger.warning("Transaction hash: " + tx_hash)

    logger.info("Waiting Tx to be mined ")
    spinner = Spinner()
    spinner.start()
    for _ in range(MAX_RETRIES):
        # Get tx receipt to get contract address
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        if tx_receipt and tx_receipt['blockNumber']:
            break
        time.sleep(SECONDS_BETWEEN_RETRIES)
    spinner.stop()

    # Show the status to the user
    if tx_receipt['status'] == 0:
        logger.critical("Contract deployment failed. :(")
        if tx_receipt['gasUsed'] == tx_receipt['gasSent']:
            logger.critical("Most probably ran out of gas.")
    else:
        logger.warning("Contract address: " + tx_receipt['contractAddress'])
        logger.warning("Block number: " + str(tx_receipt['blockNumber']))
        logger.warning("Gas used: " + str(tx_receipt['gasUsed']))

except (requests.exceptions.ConnectionError, ConnectionRefusedError, ReadTimeout):
    logger.critical("Connection timed out. - Please verify that the ethereum client is running.")

except AsyncClientError:
    logger.error("Ethereum client is Out of Sync or Forked. Please check the client log and try again.")

except ValueError as ve:
    message =ve.args[0]['message']
    if message == "Unable to unlock the account.":
        logger.error("Wrong account password.")
    if message == "Method not found":
        logger.error("Unable to access Personal API.")
        logger.error("Run the ethereum client with appending flags: --jsonrpc-apis eth,net,web3,personal")
    else:
        logger.error("Client error message: " + message)

except Exception as e:
    logger.error("Unexpected error: " + str(e))

# CLEAN UP AND QUIT
finally:
    try:
        logger.info("Quitting.")
        logger.info("Locking account.")
        w3.personal.lockAccount(account=args.account)
        logger.info("Account locked, Bye :)")

    except (requests.exceptions.ConnectionError, ConnectionRefusedError, ReadTimeout):
        logger.info("Connection timed out. - Please verify that the ethereum client is running.")

    # Needed for Geth only. Parity unlocks the acc for a single sign.
    except ValueError as v:
        logger.info("All good, Bye :)")

    except Exception as e:
        logger.info("Unexpected error:", e.args[0]['message'])
