from requests.auth import HTTPBasicAuth
from web3 import Web3
import requests
from datetime import datetime


def get_current_price(proxy=False):
    if proxy is False:
        url = "https://aws.okex.com/api/spot/v3/instruments/eth-usdt/ticker"
        r = requests.get(url, verify=False)
        return r.json()
    else:
        res = requests.get("http://ss1.jie8.cc/payment/eth/price")
        body = res.json()
        return body



def call_api(method, params=None, network="main", infura_project_id=None, infura_project_secret=None):
    # network: main | ropsten
    if params is None:
        params = []
    url = "https://{}.infura.io/v3/{}".format(network, infura_project_id)
    auth = HTTPBasicAuth('', infura_project_secret)
    payload = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": 1,
    }
    response = requests.post(url, auth=auth, json=payload)
    return response.json()


def getBlockByNumber(blockNumber):
    print("getBlockByNumber", blockNumber)
    r = call_api("eth_getBlockByNumber", [Web3.toHex(blockNumber), False])
    result = r['result']
    if "timestamp" in result:
        result["created_at"] = datetime.utcfromtimestamp(Web3.toInt(hexstr=result['timestamp']))
    return result


def getBalance(addr):
    r = call_api("eth_getBalance", [addr, "latest"])
    # web3.utils.unitMap
    return Web3.fromWei(Web3.toInt(hexstr=r['result']), "ether")


def getTransactionByHash(tx):
    r = call_api("eth_getTransactionByHash", [tx])
    result = r['result']
    result['blockNumber'] = Web3.toInt(hexstr=result['blockNumber']) if result['blockNumber'] is not None else 0
    result['gas'] = Web3.fromWei(Web3.toInt(hexstr=result['gas']), "Gwei")
    result['gasPrice'] = Web3.fromWei(Web3.toInt(hexstr=result['gasPrice']), "Gwei")
    result['value'] = Web3.fromWei(Web3.toInt(hexstr=result['value']), "ether")
    return result


def getAddrFromEtherscan(addr, network="main", path="address"):
    return getTransactionsFromEtherscan(addr, network, path)


def getTxFromEtherscan(addr, network="main", path="tx"):
    return getTransactionsFromEtherscan(addr, network, path)


def getTransactionsFromEtherscan(addr, network="main", path="address"):
    if network != "main":
        network = network + "."
    else:
        network = ""
    url = "https://{}etherscan.io/{}/{}".format(network, path, addr)
    headers = dict()
    headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8," \
                        "application/signed-exchange;v=b3;q=0.9 "
    headers["user-agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) " \
                            "Chrome/80.0.3987.149 Safari/537.36 "
    r = requests.get(url, verify=False, headers=headers)
    return r.text
