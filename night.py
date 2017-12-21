import argparse


NAME = 'Night'
VERSION = '0.1'
BUILD = 'dec.2017'
AUTHOR = 'github.com/cerealkill/night'
V = '{n} version {v} {b} {a}'.format(n=NAME, v=VERSION, b=BUILD, a=AUTHOR)

USAGE = "night [--version] [--help] [--verbose] <command> [<args>]\n\n\
   compile   Compile a Smart Contract and save it for deployment.\n\
   deploy    Deploy a Smart Contract to a local client from memory or file.\n\
   test      Drop to an interactive console with pre loaded contract and web3.\n"

DESCRIPTION = 'Night is a Ethereum smart contract compilation and deployment tool.'

HEADER = '{n} v{v}'.format(n=NAME, v=VERSION)

parser = argparse.ArgumentParser(prog=NAME, usage=USAGE, description=DESCRIPTION)

parser.add_argument('--version', action='version', version=V)
args = parser.parse_args()

print(USAGE)
