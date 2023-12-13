import json
import random

from locust import HttpUser, task, between

from utils import eth_balance_command, eth_transfer_command
from setup import create_wallets_with_money_for_zksync_stack

# Setup wallets from config
config_file_path = 'config.json'
with open(config_file_path, 'r') as file:
    data = json.load(file)
should_fund_wallets = data["fund_wallets"] == "True"
amount_of_wallets = int(data["amount_of_wallets"])

wallets_with_money = create_wallets_with_money_for_zksync_stack(with_transfer=should_fund_wallets, quantity=amount_of_wallets)


class ZkSyncWalletUser(HttpUser):
    wait_time = between(1, 5)

    host = "http://127.0.0.1:5000" #local flask server

    failed_wallets = {}

    #@task
    def check_balance(self):
        wallet = random.choice(wallets_with_money)
        self.client.post("/run", json={"command": eth_balance_command(wallet["address"])}, name="ETH Balance")

    @task
    def transfer_eth(self):
        from_wallet, to_wallet = random.sample(wallets_with_money, 2)
        post_response = self.client.post("/run", json={"command": eth_transfer_command(from_wallet["privateKey"],
                                                                                       to_wallet["address"], 1)}, name="ETH Transfer")


# class ZkSyncContractUser(HttpUser):
#    wait_time = between(1, 5)
#    host = "http://127.0.0.1:5000"
#
#   @task
#    def check_erc20_token_balance(self):
#        self.client.post("/run", json={"command": erc20_contract_balance_command}, name="ERC20 Balance")
#
#    @task
#    def erc20_token_transfer(self):
#        self.client.post("/run", json={"command": erc20_contract_transfer_command}, name="ERC20 Transfer")
