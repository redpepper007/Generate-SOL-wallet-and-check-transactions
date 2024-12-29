import base58
from solders.keypair import Keypair #type: ignore
from solana.rpc.async_api import AsyncClient
from solana.rpc.api import Client
from solders.pubkey import Pubkey  # type: ignore
import time
import os
os.system('color'); green = '\033[32m'; red = '\033[31m'; yellow = '\033[33m'; reset = '\033[0m'
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "wallets.txt")
script_filename = os.path.basename(__file__)
delay = 5
total = 0
found = 0

RPC = "https://api.mainnet-beta.solana.com" # use paid RPC for better API limits

try:
    client = Client(RPC)
    print(f"{green}Connection to RPC is OK, delay for API requests is {delay} seconds{reset}\n")
except Exception:
     print(f"{red}Can't connect to RPC, will not proceed{reset}")
     time.sleep(99999999)

def get_transaction_count(pubkey: str) -> int:
        try:
            response = client.get_signatures_for_address(pubkey)
            if response.value:
                return len(response.value)
            return 0
        except Exception as e:
            print(f"{red}An error occurred while fetching transaction count{reset}")
            time.sleep(60)
        return 0

while True:
    account = Keypair()
    privateKey = base58.b58encode(account.secret() + base58.b58decode(str(account.pubkey()))).decode('utf-8')
    walletAddress = account.pubkey()
    print(walletAddress, privateKey)
    transaction_count = get_transaction_count(walletAddress)
    total += 1

    if transaction_count > 0: 
        print(f'\n{green}Found some transactions{reset}\n')
        with open(desktop_path, 'a') as file:
            file.write(f"{walletAddress} - {privateKey}\n")
        print(f"Wallet saved to {desktop_path}")
        found += 1

    print(f"> {transaction_count} transactions [ {found}/{total} ] {script_filename}\n")
    time.sleep(delay)
