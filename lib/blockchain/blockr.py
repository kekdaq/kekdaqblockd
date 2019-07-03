'''
blockr.io
'''
import logging

from lib import config, util, util_bitcoin

def get_host():
    if config.BLOCKCHAIN_SERVICE_CONNECT:
        return config.BLOCKCHAIN_SERVICE_CONNECT
    else:
        return 'http://tbtc.blockr.io' if config.TESTNET else 'http://btc.blockr.io'

def check():
    pass

def getinfo():
    result = util.get_url(get_host() + '/api/v1/coin/info', abort_on_error=True)
    if 'status' in result and result['status'] == 'success':
        return {
            "info": {
                "blocks": result['data']['last_block']['nb']
            }
        }
    
    return None

def listunspent(address):
    result = util.get_url(get_host() + '/api/v1/address/unspent/{}/'.format(address), abort_on_error=True)
    if 'status' in result and result['status'] == 'success':
        utxo = []
        for txo in result['data']['unspent']:
            newtxo = {
                'address': address,
                'txid': txo['tx'],
                'vout': txo['n'],
                'ts': 0,
                'scriptPubKey': txo['script'],
                'amount': float(txo['amount']),
                'confirmations': txo['confirmations'],
                'confirmationsFromCache': False
            }
            utxo.append(newtxo)
        return utxo
    
    return None

def getaddressinfo(address):
    infos = util.get_url(get_host() + '/api/v1/address/info/{}'.format(address), abort_on_error=True)
    if 'status' in infos and infos['status'] == 'success':
        txs = util.get_url(get_host() + '/api/v1/address/txs/{}'.format(address), abort_on_error=True)
        if 'status' in txs and txs['status'] == 'success':
            transactions = []
            for tx in txs['data']['txs']:
                transactions.append(tx['tx'])
            return {
                'addrStr': address,
                'balance': infos['data']['balance'],
                'balanceSat': infos['data']['balance'] * config.UNIT,
                'totalReceived': infos['data']['totalreceived'],
                'totalReceivedSat': infos['data']['totalreceived'] * config.UNIT,
                'unconfirmedBalance': 0,
                'unconfirmedBalanceSat': 0,
                'unconfirmedTxApperances': 0,
                'txApperances': txs['data']['nb_txs'],
                'transactions': transactions
            }
    
    return None

def gettransaction(tx_hash):
    # tx = util.get_url(get_host() + '/api/v1/tx/raw/{}'.format(tx_hash), abort_on_error=True)
    #
    # Handle missing transactions properly
    
    url = get_host() + '/api/v1/tx/raw/{}'.format(tx_hash)
    tx = util.get_url(url, abort_on_error=False)
    if tx and tx.get('code') == 404:
        return None

    if 'status' in tx and tx['status'] == 'success':
        valueOut = 0
        for vout in tx['data']['tx']['vout']:
            valueOut += vout['value']
        return {
            'txid': tx_hash,
            'version': tx['data']['tx']['version'],
            'locktime': tx['data']['tx']['locktime'],
            'blockhash': tx['data']['tx'].get('blockhash', None), #will be None if not confirmed yet...
            'confirmations': tx['data']['tx'].get('confirmations', None),
            'time': tx['data']['tx'].get('time', None),
            'blocktime': tx['data']['tx'].get('blocktime', None),
            'valueOut': valueOut,
            'vin': tx['data']['tx']['vin'],
            'vout': tx['data']['tx']['vout']
        }

    return None

def get_pubkey_for_address(address):
    #first, get a list of transactions for the address
    address_info = getaddressinfo(address)

    #if no transactions, we can't get the pubkey
    if not address_info['transactions']:
        return None
    
    #for each transaction we got back, extract the vin, pubkey, go through, convert it to binary, and see if it reduces down to the given address
    for tx_id in address_info['transactions']:
        #parse the pubkey out of the first sent transaction
        tx = gettransaction(tx_id)
        pubkey_hex = tx['vin'][0]['scriptSig']['asm'].split(' ')[1]
        if util_bitcoin.pubkey_to_address(pubkey_hex) == address:
            return pubkey_hex
    return None