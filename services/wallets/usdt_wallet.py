from __future__ import annotations

from typing import Dict, Any, Tuple, Optional

import asyncio
import aiohttp
import logging
from eth_account import Account
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider
from tronpy.contract import Contract


ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"},
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
    },
]

TRC20_ABI = [
    {
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function"
    }
]


class BEP20Wallet:
    """Простой помощник для работы с USDT в сети BSC."""

    USDT_CONTRACT = "0x55d398326f99059fF775485246999027B3197955"

    def __init__(self, rpc_url: str = "https://bsc-dataseed.binance.org/", api_key: str | None = None):
        """Создаёт объект для работы с сетью BSC."""
        logging.debug("Инициализация BEP20Wallet: %s", rpc_url)
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        # BSC работает в режиме POA, подключаем соответствующую middleware
        self.w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        self.api_key = api_key
        self.usdt = self.w3.eth.contract(
            address=Web3.to_checksum_address(self.USDT_CONTRACT),
            abi=ERC20_ABI,
        )
        logging.info("BEP20Wallet успешно инициализирован")

    @staticmethod
    async def create_wallet() -> Dict[str, str]:
        """Создаёт случайный кошелёк и возвращает адрес и приватный ключ."""
        account = Account.create()
        wallet = {
            "address": account.address,
            "private_key": account.key.hex(),
        }
        logging.info("Создан новый BSC кошелёк: %s", wallet["address"])
        return wallet

    async def _get_last_tx(self, address: str) -> Optional[Dict[str, Any]]:
        """Возвращает последнюю USDT-транзакцию адреса через API BscScan."""
        params = {
            "module": "account",
            "action": "tokentx",
            "contractaddress": self.USDT_CONTRACT,
            "address": address,
            "page": 1,
            "offset": 1,
            "sort": "desc",
            "apikey": self.api_key or "",
        }
        try:
            logging.debug("Запрашиваем последнюю транзакцию BSC для %s", address)
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://api.bscscan.com/api", params=params, timeout=10
                ) as resp:
                    data = await resp.json()
        except aiohttp.ClientError as e:
            logging.error("Ошибка запроса BscScan: %s", e)
            return None

        result = data.get("result")
        if isinstance(result, list) and result:
            logging.debug("Последняя транзакция найдена")
            return result[0]
        return None

    async def check_payment(self, address: str, subscription_price: float) -> Dict[str, Any]:
        """Проверяет, была ли произведена оплата подписки."""
        tx = await self._get_last_tx(address)
        if not tx:
            logging.debug("Транзакции для %s не найдены", address)
            return {"status": "not_found"}

        amount = int(tx.get("value", 0)) / 10 ** int(tx.get("tokenDecimal", 18))
        threshold = max(subscription_price - 0.5, 0)
        confirmations = int(tx.get("confirmations", 0))
        info: Dict[str, Any] = {
            "tx_hash": tx.get("hash"),
            "amount": amount,
        }
        if confirmations == 0:
            info["status"] = "pending_confirmation"
            logging.debug("Транзакция %s ожидает подтверждения", info["tx_hash"])
        elif amount >= threshold:
            info["status"] = "success"
            logging.info("Оплата успешно обнаружена: %s USDT", amount)
        else:
            info["status"] = "insufficient"
            info["missing"] = max(threshold - amount, 0)
            logging.info("Недостаточная оплата: %s USDT, не хватает %s", amount, info["missing"])
        return info

    async def get_balance(self, address: str, subscription_price: float) -> Dict[str, Any]:
        """
        Возвращает баланс USDT (BEP20) и BNB на кошельке.
        Статус: 'success', если хватает для подписки, иначе 'checking_balance'.
        """
        logging.debug("Получаем баланс BSC кошелька %s", address)
        try:
            checksummed = Web3.to_checksum_address(address)

            # Получаем баланс USDT
            usdt_balance = await asyncio.to_thread(
                self.usdt.functions.balanceOf(checksummed).call
            )
            decimals = await asyncio.to_thread(self.usdt.functions.decimals().call)
            usdt = usdt_balance / (10 ** decimals)

            # Получаем баланс BNB
            bnb_wei = await asyncio.to_thread(
                self.w3.eth.get_balance, checksummed
            )
            bnb = self.w3.from_wei(bnb_wei, "ether")

            usdt = round(float(usdt), 2)
            bnb = round(float(bnb), 6)

            if usdt >= subscription_price:
                return {
                    "status": "success",
                    "current_balance": (usdt, bnb),
                    "missing": 0.0
                }
            else:
                missing = round(subscription_price - usdt, 2)
                return {
                    "status": "checking_balance",
                    "current_balance": (usdt, bnb),
                    "missing": missing
                }

        except Exception as e:
            logging.error("Ошибка при получении баланса BSC кошелька: %s", e)
            return {
                "status": "error",
                "message": str(e),
                "current_balance": (0.0, 0.0),
                "missing": subscription_price
            }

    async def withdraw(self, private_key: str, to_address: str, amount: float, min_bnb: float = 0.001) -> str:
        """Отправляет USDT на другой адрес, проверяя остаток BNB."""
        account = self.w3.eth.account.from_key(private_key)
        from_address = account.address
        bnb_balance_wei = await asyncio.to_thread(self.w3.eth.get_balance, from_address)
        bnb_balance = self.w3.from_wei(bnb_balance_wei, "ether")
        if bnb_balance < min_bnb:
            logging.error("Недостаточно BNB для отправки: %s", bnb_balance)
            raise RuntimeError("Not enough BNB for gas")
        decimals = await asyncio.to_thread(self.usdt.functions.decimals().call)
        amount_wei = int(amount * 10 ** decimals)
        nonce = await asyncio.to_thread(self.w3.eth.get_transaction_count, from_address)
        txn = self.usdt.functions.transfer(
            Web3.to_checksum_address(to_address), amount_wei
        ).build_transaction(
            {
                "from": from_address,
                "nonce": nonce,
                "gas": 100000,
                "gasPrice": self.w3.to_wei(5, "gwei"),
                "chainId": 56,
            }
        )
        signed = self.w3.eth.account.sign_transaction(txn, private_key)
        tx_hash = await asyncio.to_thread(
            self.w3.eth.send_raw_transaction, signed.rawTransaction
        )
        logging.info("USDT отправлены. Хэш транзакции: %s", tx_hash.hex())
        return tx_hash.hex()


class TRC20Wallet:
    """Простой помощник для работы с USDT в сети Tron."""

    USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
    API_KEY = "c5238211-ea5d-4030-946a-7e3ee90a6192"
    TRONSCAN_API = "0c5ea96d-6d46-46e4-8172-6cfb7ff010b3"

    def __init__(self, node_url: str = "https://api.trongrid.io"):
        logging.debug("Инициализация TRC20Wallet: %s", node_url)
        # Tron.client принимает провайдер HTTPProvider, который отвечает за
        # соединение с выбранным узлом сети.
        self.client = Tron(provider=HTTPProvider(node_url, api_key=self.API_KEY))
        logging.info("TRC20Wallet успешно инициализирован")

    @staticmethod
    async def create_wallet() -> Dict[str, str]:
        """Создаёт кошелёк Tron и возвращает адрес и приватный ключ."""
        key = PrivateKey.random()
        wallet = {
            "address": key.public_key.to_base58check_address(),
            "private_key": key.hex(),
        }
        logging.info("Создан новый Tron кошелёк: %s", wallet["address"])
        return wallet

    async def _get_last_tx(self, address: str, only_confirmed: str) -> Optional[Dict[str, Any]]:
        """Получает последнюю USDT-транзакцию адреса через TronGrid."""
        params = {
            "limit": 1,
            "only_confirmed": "false",
            "contract_address": self.USDT_CONTRACT,
            "order_by": "block_timestamp,desc",
        }
        url = f"https://api.trongrid.io/v1/accounts/{address}/transactions/trc20"
        try:
            logging.debug("Запрашиваем последнюю транзакцию Tron для %s", address)
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=10) as resp:
                    data = await resp.json()
                    logging.debug("DATA Получаем последнюю транзакцию Tron: %s", data)
        except aiohttp.ClientError as e:
            logging.error("Ошибка запроса TronGrid: %s", e)
            return None
        txs = data.get("data")
        if isinstance(txs, list) and txs:
            logging.debug("Последняя транзакция Tron найдена")
            logging.debug("Транзакция: %s", txs[0])
            return txs[0]
        return None

    async def is_transaction_confirmed(self, address: str, subscription_price: float) -> Dict[str, Any]:
        """Проверяет оплату подписки для сети Tron."""
        tx = await self._get_last_tx(address, only_confirmed="true")
        if not tx:
            logging.debug("Транзакции в Tron для %s не найдены", address)
            return {"status": "not_found"}
        value = int(tx.get("value", "0"))
        decimals = int(tx.get("tokenInfo", {}).get("tokenDecimal", 6))
        amount = value / 10 ** decimals
        threshold = max(subscription_price - 0.5, 0)

        info: Dict[str, Any] = {
            "tx_hash": tx.get("transaction_id"),
            "amount": amount,
        }

        if amount >= threshold:
            info["status"] = "success"
            logging.info("Оплата в Tron успешно обнаружена: %s USDT", amount)
        else:
            info["status"] = "insufficient"
            info["missing"] = max(threshold - amount, 0)
            logging.info("Недостаточная оплата в Tron: %s USDT, не хватает %s", amount, info["missing"])
        return info

    async def check_payment(self, address: str, subscription_price: float) -> Dict[str, Any]:
        """Проверяет оплату подписки для сети Tron."""
        tx = await self._get_last_tx(address, only_confirmed="false")
        if not tx:
            logging.debug("Транзакции в Tron для %s не найдены", address)
            return {"status": "not_found"}
        value = int(tx.get("value", "0"))
        decimals = int(tx.get("tokenInfo", {}).get("tokenDecimal", 6))
        amount = value / 10 ** decimals
        threshold = max(subscription_price - 0.5, 0)
        confirmed = tx.get("confirmed", False)
        info: Dict[str, Any] = {
            "tx_hash": tx.get("transaction_id"),
            "amount": amount,
        }
        if not confirmed:
            info["status"] = "pending_confirmation"
            logging.debug("Tron транзакция %s ожидает подтверждения", info["tx_hash"])
        return info

    async def get_balance(self, address: str, subscription_price: float) -> Dict[str, Any]:
        """
        Получает баланс USDT (TRC20) и TRX через Tronscan API /account/tokens.
        Возвращает статус 'success' или 'checking_balance' и недостающую сумму при необходимости.
        """
        logging.debug("Получаем баланс Tron кошелька %s через /account/tokens", address)
        url = "https://apilist.tronscanapi.com/api/account/tokens"
        params = {
            "address": address,
            "start": 0,
            "limit": 100,
            "hidden": 0,
            "show": 0,
            "sortType": 0,
            "sortBy": 0
        }

        headers = {}
        if self.API_KEY:
            headers["TRON-PRO-API-KEY"] = self.TRONSCAN_API

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=headers, timeout=10) as resp:
                    data = await resp.json()
                    logging.debug("Ответ TronScan tokens: %s", data)

                    trx = 0.0
                    usdt = 0.0

                    for token in data.get("data", []):
                        token_id = token.get("tokenId")
                        decimals = int(token.get("tokenDecimal", 6))
                        raw_balance = int(token.get("balance", 0))

                        if token_id == "_":
                            trx = raw_balance / (10 ** decimals)
                        elif token_id == self.USDT_CONTRACT:
                            usdt = raw_balance / (10 ** decimals)

                    usdt = round(usdt, 2)
                    trx = round(trx, 2)

                    if usdt >= subscription_price:
                        return {
                            "status": "success",
                            "current_balance": (usdt, trx),
                            "missing": 0.0
                        }
                    else:
                        missing = round(subscription_price - usdt, 2)
                        return {
                            "status": "checking_balance",
                            "current_balance": (usdt, trx),
                            "missing": missing
                        }

        except Exception as e:
            logging.error("Ошибка при получении баланса Tron через /account/tokens: %s", e)
            return {
                "status": "error",
                "message": str(e),
                "current_balance": (0.0, 0.0),
                "missing": subscription_price
            }

    async def withdraw(self, private_key: str, to_address: str, amount: float, min_trx: float = 5.0) -> str:
        """Отправляет USDT, проверяя остаток TRX для комиссии."""
        key = PrivateKey(bytes.fromhex(private_key))
        from_address = key.public_key.to_base58check_address()
        tron_balance = await asyncio.to_thread(
            self.client.get_account_balance, from_address
        )
        if tron_balance < min_trx:
            logging.error("Недостаточно TRX для отправки: %s", tron_balance)
            raise RuntimeError("Not enough TRX for fees")
        usdt_contract = self.client.get_contract(self.USDT_CONTRACT, abi=TRC20_ABI)
        decimals = usdt_contract.functions.decimals()
        txn = (
            usdt_contract.functions.transfer(to_address, int(amount * 10 ** decimals))
            .with_owner(from_address)
            .build()
            .sign(key)
            .broadcast()
        )
        logging.info("USDT в сети Tron отправлены. Хэш транзакции: %s", txn["txid"])
        return txn["txid"]