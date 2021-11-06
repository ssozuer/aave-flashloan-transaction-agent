AAVE_V2_DATA_PROVIDER_ADDRESS = '0x057835Ad21a177dbdd3090bB1CAE03EaCF78Fc6d'
USDT_ADDRESS = '0xdAC17F958D2ee523a2206206994597C13D831ec7'

FLASH_LOAN_ALERT_AMOUNT = 10000000 # 30M USD

def get_price_in_usdt(priceOracle, ethAmount):
    one_usdt_in_eth = priceOracle.functions.getAssetPrice(USDT_ADDRESS).call()  / 10**18
    amount_in_usdt = ethAmount / one_usdt_in_eth
    return amount_in_usdt

