import asyncio
from client import Wallet
from web3 import AsyncWeb3, AsyncHTTPProvider, Web3
from web3.exceptions import TransactionNotFound
from aiohttp import ClientSession
from aiohttp_socks import ProxyConnector  # Для работы с прокси
import json
import time
import random

datas = []
goodos = []

what_gas = 50   #Максимальный газ в эфире, при работе не с ЕТХ сетью, похуй какой


print("""Укажите сеть для свопа. Введите просто номер нужной сети:
      1. ARB
      2. OP
      3. ETH
      4. BASE
""")
chain = int(input())
if chain == 1:
    exp = "https://arbiscan.io/tx/"
    rpc = "https://arb1.arbitrum.io/rpc"
    print("""Укажите токен с которого будет сделан своп. Введите просто номер нужного токена:
          1. ETH
          2. USDC
          3. USDT
          4. Мой токен.
    """)
    tin = int(input())
    if tin == 1:
        token_it = "0x0000000000000000000000000000000000000000"
    if tin == 2:
        token_it = "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"
        contract_address = "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"#юдс арба
        aprove = "0xe298b93ffB5eA1FB628e0C0D55A43aeaC268e347" #контрак апрува для арбы
    if tin == 3:
        token_it = "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9"
        contract_address = "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9"#юдт арба
        aprove = "0xe298b93ffB5eA1FB628e0C0D55A43aeaC268e347" #контрак апрува для арбы
    if tin == 4:
        print("Введите контракт токена:")
        input_contr = input().strip()
        if not input_contr.startswith("0x") or len(input_contr) != 42:
            raise ValueError("Введён некорректный адрес контракта токена.")
        token_it = input_contr
        contract_address = input_contr
        aprove = "0xe298b93ffB5eA1FB628e0C0D55A43aeaC268e347" #контрак апрува для арбы

    print("""Укажите токен на который будет сделан своп. Введите просто номер нужного токена:
          1. ETH
          2. USDC
          3. USDT
          4. Мой токен.
    """)
    tout = int(input())
    if tout == 1:
        token_out = "0x0000000000000000000000000000000000000000"
        if tin == 1:
            print("Как я тебе свопну эфир на эфир?")
            exit()
    if tout == 2:
        token_out = "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"
        contract_address = "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"#юдс арба
        aprove = "0xe298b93ffB5eA1FB628e0C0D55A43aeaC268e347" #контрак апрува для арбы
    if tout == 3:
        token_out = "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9"
        contract_address = "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9"#юдт арба
        aprove = "0xe298b93ffB5eA1FB628e0C0D55A43aeaC268e347" #контрак апрува для арбы
    if tout == 4:
        print("Введите контракт токена:")
        input_contr = input().strip()
        if not input_contr.startswith("0x") or len(input_contr) != 42:
            raise ValueError("Введён некорректный адрес контракта токена.")
        token_it = input_contr
        contract_address = input_contr
        aprove = "0xCa423977156BB05b13A2BA3b76Bc5419E2fE9680"  # контрак апрува для op

if chain == 2:
    exp = "https://optimistic.etherscan.io/tx/"
    rpc = "https://rpc.ankr.com/optimism"
    print("""Укажите токен с которого будет сделан своп. Введите просто номер нужного токена:
          1. ETH
          2. USDC
          3. USDT
          4. Мой токен.
    """)
    tin = int(input())
    if tin == 1:
        token_it = "0x0000000000000000000000000000000000000000"
    if tin == 2:
        token_it = "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85"
        contract_address = "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85"#юдс op
        aprove = "0xCa423977156BB05b13A2BA3b76Bc5419E2fE9680" #контрак апрува для op
    if tin == 3:
        token_it = "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58"
        contract_address = "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58"#юдт op
        aprove = "0xCa423977156BB05b13A2BA3b76Bc5419E2fE9680" #контрак апрува для op
    if tin == 4:
        print("Введите контракт токена:")
        input_contr = input().strip()
        if not input_contr.startswith("0x") or len(input_contr) != 42:
            raise ValueError("Введён некорректный адрес контракта токена.")
        token_it = input_contr
        contract_address = input_contr
        aprove = "0xCa423977156BB05b13A2BA3b76Bc5419E2fE9680" #контрак апрува для op

    print("""Укажите токен на который будет сделан своп. Введите просто номер нужного токена:
            1. ETH
            2. USDC
            3. USDT
            4. Мой токен.
    """)
    tout = int(input())
    if tout == 1:
        token_out = "0x0000000000000000000000000000000000000000"
        if tin == 1:
            print("Как я тебе свопну эфир на эфир?")
            exit()
    if tout == 2:
        token_out = "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85"
        contract_address = "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85"#юдс op
        aprove = "0xCa423977156BB05b13A2BA3b76Bc5419E2fE9680" #контрак апрува для op
    if tout == 3:
        token_out = "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58"
        contract_address = "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58"#юдт op
        aprove = "0xCa423977156BB05b13A2BA3b76Bc5419E2fE9680" #контрак апрува для op
    if tout == 4:
        print("Введите контракт токена:")
        input_contr = input().strip()
        if not input_contr.startswith("0x") or len(input_contr) != 42:
            raise ValueError("Введён некорректный адрес контракта токена.")
        token_it = input_contr
        contract_address = input_contr
        aprove = "0xCa423977156BB05b13A2BA3b76Bc5419E2fE9680"  # контрак апрува для op
if chain == 3:
    exp = "https://etherscan.io/tx/"
    rpc = "https://ethereum-rpc.publicnode.com"
    print("""Укажите токен с которого будет сделан своп. Введите просто номер нужного токена:
          1. ETH
          2. USDC
          3. USDT
          4. Мой токен.
    """)
    tin = int(input())
    if tin == 1:
        token_it = "0x0000000000000000000000000000000000000000"
    if tin == 2:
        token_it = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
        contract_address = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"#юдс eth
        aprove = "0xCf5540fFFCdC3d510B18bFcA6d2b9987b0772559" #контрак апрува для eth
    if tin == 3:
        token_it = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
        contract_address = "0xdAC17F958D2ee523a2206206994597C13D831ec7"#юдт eth
        aprove = "0xCf5540fFFCdC3d510B18bFcA6d2b9987b0772559" #контрак апрува для eth
    if tin == 4:
        print("Введите контракт токена:")
        input_contr = input().strip()
        if not input_contr.startswith("0x") or len(input_contr) != 42:
            raise ValueError("Введён некорректный адрес контракта токена.")
        token_it = input_contr
        contract_address = input_contr
        aprove = "0xCf5540fFFCdC3d510B18bFcA6d2b9987b0772559" #контрак апрува для eth

    print("""Укажите токен на который будет сделан своп. Введите просто номер нужного токена:
            1. ETH
            2. USDC
            3. USDT
            4. Мой токен.
    """)
    tout = int(input())
    if tout == 1:
        token_out = "0x0000000000000000000000000000000000000000"
        if tin == 1:
            print("Как я тебе свопну эфир на эфир?")
            exit()
    if tout == 2:
        token_out = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
        contract_address = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"#юдс eth
        aprove = "0xCf5540fFFCdC3d510B18bFcA6d2b9987b0772559" #контрак апрува для eth
    if tout == 3:
        token_out = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
        contract_address = "0xdAC17F958D2ee523a2206206994597C13D831ec7"#юдт eth
        aprove = "0xCf5540fFFCdC3d510B18bFcA6d2b9987b0772559" #контрак апрува для eth
    if tout == 4:
        print("Введите контракт токена:")
        input_contr = input().strip()
        if not input_contr.startswith("0x") or len(input_contr) != 42:
            raise ValueError("Введён некорректный адрес контракта токена.")
        token_it = input_contr
        contract_address = input_contr
        aprove = "0xCf5540fFFCdC3d510B18bFcA6d2b9987b0772559" #контрак апрува для eth
if chain == 4:
    exp = "https://basescan.org/tx/"
    rpc = "https://mainnet.base.org"
    print("""Укажите токен с которого будет сделан своп. Введите просто номер нужного токена:
          1. ETH
          2. USDC
          3. DAI
          4. Мой токен.
    """)
    tin = int(input())
    if tin == 1:
        token_it = "0x0000000000000000000000000000000000000000"
    if tin == 2:
        token_it = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
        contract_address = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"#юдс base
        aprove = "0x19cEeAd7105607Cd444F5ad10dd51356436095a1" #контрак апрува для base
    if tin == 3:
        token_it = "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb"
        contract_address = "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb"#dai base
        aprove = "0x19cEeAd7105607Cd444F5ad10dd51356436095a1" #контрак апрува для base
    if tin == 4:
        print("Введите контракт токена:")
        input_contr = input().strip()
        if not input_contr.startswith("0x") or len(input_contr) != 42:
            raise ValueError("Введён некорректный адрес контракта токена.")
        token_it = input_contr
        contract_address = input_contr
        aprove = "0x19cEeAd7105607Cd444F5ad10dd51356436095a1" #контрак апрува для base

    print("""Укажите токен на который будет сделан своп. Введите просто номер нужного токена:
            1. ETH
            2. USDC
            3. DAI
            4. Мой токен.
    """)
    tout = int(input())
    if tout == 1:
        token_out = "0x0000000000000000000000000000000000000000"
        if tin == 1:
            print("Как я тебе свопну эфир на эфир?")
            exit()
    if tout == 2:
        token_out = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
        contract_address = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"#юдс base
        aprove = "0x19cEeAd7105607Cd444F5ad10dd51356436095a1" #контрак апрува для base
    if tout == 3:
        token_out = "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb"
        contract_address = "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb"#dai base
        aprove = "0x19cEeAd7105607Cd444F5ad10dd51356436095a1" #контрак апрува для base
    print("Введите контракт токена:")
    input_contr = input().strip()
    if not input_contr.startswith("0x") or len(input_contr) != 42:
        raise ValueError("Введён некорректный адрес контракта токена.")
    token_it = input_contr
    contract_address = input_contr
    aprove = "0x19cEeAd7105607Cd444F5ad10dd51356436095a1"  # контрак апрува для base


private_key = ""  # приватный ключ


w3_async = AsyncWeb3(AsyncHTTPProvider(f"{rpc}"))  # РПС сети
getadres = w3_async.eth.account.from_key(private_key).address


print("Свопать будем весь баланс или конкретную сумму?  1-Весь 2-Конкретную сумму")
bal = int(input())
if bal ==1:
    if tin == 1:
        print("Я не могу свопнуть весь баланс эфира, проверь данные и начни сначала")
        exit()
    async def get_balanses():
        with open("abi.json", 'r') as abi_file:
            abi = json.load(abi_file)
        contract = w3_async.eth.contract(address=contract_address, abi=abi)
        balance_contract = await contract.functions.balanceOf(getadres).call()
        decimals = await contract.functions.decimals().call()
        readable_value = balance_contract / (10 ** decimals)
        return readable_value
    value= asyncio.run(get_balanses())
    if value >= 10 ** 18:
        unit = 'wei'
    elif value >= 10 ** 9:
        unit = 'gwei'
    elif value >= 1:
        unit = 'ether'
    else:
        unit = 'mwei'
if bal ==2:
    if tin == 1:
        print("Укажите сумму свопа")
        value = float(input()) #Сумма свопа
        unit = 'ether'
    else:
        print("Укажите сумму свопа")
        value = float(input()) #Сумма свопа
        if value >= 10 ** 18:
            unit = 'wei'
        elif value >= 10 ** 9:
            unit = 'gwei'
        elif value >= 1:
            unit = 'ether'
        else:
            unit = 'mwei'






async def load_abi(filename):
    with open(filename, 'r') as abi_file:
        abi = json.load(abi_file)
    return abi

async def check_balance_value():
    a = await load_abi("abi.json")
    contract = w3_async.eth.contract(address=contract_address, abi=a)
    address = f"{getadres}"
    if tin == 1:
        checksum_address = w3_async.to_checksum_address(address)
        balance = await w3_async.eth.get_balance(checksum_address)
        ether_balance = w3_async.from_wei(balance, 'ether')
        if float(value) - float(ether_balance) <= 0:
            print("Недостаточно эфира для свопа")
            exit()
    if tin != 1:
        balance_contract = await contract.functions.balanceOf(getadres).call()
        decimals = await contract.functions.decimals().call()
        readable_value = balance_contract / (10 ** decimals)
        if float(value) - float(readable_value) <= 0:
            print("Недостаточно cредств для свопа")
            exit()


async def check_balance():
    a = await load_abi("abi.json")
    contract = w3_async.eth.contract(address=contract_address, abi=a)
    address = f"{getadres}"
    checksum_address = w3_async.to_checksum_address(address)
    balance = await w3_async.eth.get_balance(checksum_address)
    ether_balance = w3_async.from_wei(balance, 'ether')
    print(f"Баланс кошелька {checksum_address}: {ether_balance} ETH")

    # ПОЛУЧЕАМ ИНФОРМАЦИЮ О БАЛАНСЕ ТОКЕНА ЕРС20
    balance_contract = await contract.functions.balanceOf(getadres).call()
    decimals = await contract.functions.decimals().call()
    readable_value = balance_contract / (10 ** decimals)

    print(f"Баланс {await contract.functions.symbol().call()}: {readable_value}")
    print()

async def wait_gas():
    w3_async_eth = AsyncWeb3(AsyncHTTPProvider('https://eth.meowrpc.com'))
    gas = await w3_async_eth.eth.gas_price
    gas = w3_async_eth.from_wei(gas, 'gwei')
    print(f"Текущий газ {gas}")
    print()
    while gas > what_gas:
        print(f"Текущий газ {gas}, ожидаю снижение")
        await asyncio.sleep(20)
        if gas < what_gas:
            break


async def send_approve():
    await wait_gas()
    # Создаём транзакцию для вызова approve
    a = await load_abi("abi.json")
    contract = w3_async.eth.contract(address=contract_address, abi=a)
    approve_tx = await contract.functions.approve(
        aprove, 9999999999999999999999999999
    ).build_transaction({
        'from': Web3.to_checksum_address(getadres),
        'nonce': await w3_async.eth.get_transaction_count(getadres),
        'maxPriorityFeePerGas': await w3_async.eth.max_priority_fee,
        'maxFeePerGas': int(await w3_async.eth.gas_price * 1.25 + await w3_async.eth.max_priority_fee),
        'chainId': await w3_async.eth.chain_id
    })

    # Оценка газа
    approve_tx['gas'] = int((await w3_async.eth.estimate_gas(approve_tx)) * 1.5)

    # Подписываем транзакцию
    signed_tx = w3_async.eth.account.sign_transaction(approve_tx, private_key)

    # Отправляем транзакцию
    tx_hash = await w3_async.eth.send_raw_transaction(signed_tx.rawTransaction)
    print("Апрув ушел")
    print(f"Transaction hash: {exp}{tx_hash.hex()}")


async def pathId(value):
    if tin > 1:
        await send_approve()
    await check_balance()
    proxy_connector = ProxyConnector.from_url("http://iJEDJZpL:8BTRYSv1@154.218.18.29:64754")
    async with ClientSession(connector=proxy_connector) as session:
        url = "https://api.odos.xyz/sor/quote/v2"
        json_payload = {
            "chainId": int(await w3_async.eth.chain_id),
            "inputTokens": [
                {
                    "amount": f"{w3_async.to_wei(value, unit)}",
                    "tokenAddress": Web3.to_checksum_address(f"{token_it}")
                }
            ],
            "outputTokens": [
                {
                    "proportion": 1,
                    "tokenAddress": Web3.to_checksum_address(f"{token_out}")
                }
            ],
            "referralCode": 0,
            "slippageLimitPercent": 1,
            "sourceBlacklist": [],
            "sourceWhitelist": [],
            "userAddr": getadres
        }
        headers = {
            "Content-Type": "application/json"
        }
        async with session.post(url=url, json=json_payload, headers=headers) as response:
            data = await response.json()
            datas.append(data)


async def data_transaction():
    proxy_connector = ProxyConnector.from_url("http://iJEDJZpL:8BTRYSv1@154.218.18.29:64754")
    async with ClientSession(connector=proxy_connector) as session:
        url = "https://api.odos.xyz/sor/assemble"
        json_payload = {
            "userAddr": getadres,
            "pathId": datas[0]["pathId"],
            "simulate": False
        }
        headers = {"Content-Type": "application/json"}
        async with session.post(url=url, json=json_payload, headers=headers) as response:
            data = await response.json()
            goodos.append(data)


async def send_transaction():
    await check_balance_value()
    await wait_gas()
    await pathId(value)
    await data_transaction()
    transaction = goodos[0]["transaction"]
    transaction["value"] = int(transaction["value"])

    signed_tx = w3_async.eth.account.sign_transaction(transaction, private_key)
    tx_hash = await w3_async.eth.send_raw_transaction(signed_tx.rawTransaction)
    print("SWAP DONE")

    print(f"Сылка на транзу свопа {exp}{tx_hash.hex()}")
    print("Балансы после свопа")
    await asyncio.sleep(random.randint(1, 3))
    await check_balance()


asyncio.run(send_transaction())
