from forta_agent import Finding, FindingType, FindingSeverity, get_web3_provider, Web3
from .utils import get_price_in_usdt, AAVE_V2_DATA_PROVIDER_ADDRESS, FLASH_LOAN_ALERT_AMOUNT
from .abis import AAVE_V2_DATA_PROVIDER_ABI, AAVE_V2_LENDING_POOL_ADDRESSES_PROVIDER_ABI, AAVE_V2_PRICE_ORACLE_ABI, AAVE_V2_FLASHLOAN_FUNCTION_ABI

def provide_handle_transaction(price_oracle, lending_pool_addr):
    def handle_transaction(transaction_event):
        findings = []

        flash_loan_invocations = transaction_event.filter_function(AAVE_V2_FLASHLOAN_FUNCTION_ABI, lending_pool_addr)
        for invocation in flash_loan_invocations:
            args = invocation[1]
            assets = args['assets']
            amounts = args['amounts']

            total_asset_amount_in_eth = 0
            for i in range(len(assets)):
                total_asset_amount_in_eth += price_oracle.functions.getAssetPrice(assets[i]).call() * amounts[i] / 10 ** 18

            # transform values to human readable format
            total_asset_amount_in_eth = total_asset_amount_in_eth / 10 ** 18
            total_asset_amount_in_usd = get_price_in_usdt(price_oracle, total_asset_amount_in_eth)

            if total_asset_amount_in_usd >= FLASH_LOAN_ALERT_AMOUNT:
                print("Foundddd: ", transaction_event.hash)
                findings.append(Finding({
                    'name': 'AAVE Flash Loan Transaction Agent',
                    'description': f'The flash loan transaction value ${total_asset_amount_in_usd} >= ${FLASH_LOAN_ALERT_AMOUNT}($10M)',
                    'alert_id': 'AAVE-4',
                    'type': FindingType.Suspicious,
                    'severity': FindingSeverity.High,
                    'metadata': {
                        'transaction_amount_in_eth': total_asset_amount_in_eth,
                        'transaction_amount_in_usd': total_asset_amount_in_usd
                    }
                }))
                exit()
            
        return findings
    return handle_transaction


# create Aave data provider
w3 = get_web3_provider()
aave_data_provider = w3.eth.contract(address=Web3.toChecksumAddress(AAVE_V2_DATA_PROVIDER_ADDRESS), abi=AAVE_V2_DATA_PROVIDER_ABI)

# create Aave lending pool address provider
lendig_pool_addresses_provider_addr = aave_data_provider.functions.ADDRESSES_PROVIDER().call()
lending_pool_addresses_provider = w3.eth.contract(address=Web3.toChecksumAddress(lendig_pool_addresses_provider_addr), abi=AAVE_V2_LENDING_POOL_ADDRESSES_PROVIDER_ABI)

# get Aave lending pool address
lending_pool_addr = lending_pool_addresses_provider.functions.getLendingPool().call()

# create Aave price oracle
price_oracle_addr = lending_pool_addresses_provider.functions.getPriceOracle().call()
price_oracle = w3.eth.contract(address=Web3.toChecksumAddress(price_oracle_addr), abi=AAVE_V2_PRICE_ORACLE_ABI)

# init provider function
init_handle_transaction = provide_handle_transaction(price_oracle, lending_pool_addr)

# return handle transaction implementation
def handle_transaction(transaction_event):
    return  init_handle_transaction(transaction_event)



