# -*- coding: utf-8 -*-
VERSION = "1.4.0" #should keep up with the counterwallet version it works with (for now at least)

DB_VERSION = 22 #a db version increment will cause counterblockd to rebuild its database off of counterpartyd 

CAUGHT_UP = False #atomic state variable, set to True when counterpartyd AND counterblockd are caught up

UNIT = 100000000

SUBDIR_ASSET_IMAGES = "asset_img" #goes under the data dir and stores retrieved asset images
SUBDIR_FEED_IMAGES = "feed_img" #goes under the data dir and stores retrieved feed images

MARKET_PRICE_DERIVE_NUM_POINTS = 8 #number of last trades over which to derive the market price (via WVAP)

# FROM counterpartyd
# NOTE: These constants must match those in counterpartyd/lib/config.py
REGULAR_DUST_SIZE = 0.0001 * UNIT
MULTISIG_DUST_SIZE = 0.0001 * UNIT * 2
ORDER_BTC_DUST_LIMIT_CUTOFF = MULTISIG_DUST_SIZE

mongo_db = None #will be set on server init

BTC = 'PEPE'
XCP = 'KDAQ'

MAX_REORG_NUM_BLOCKS = 30 #max reorg we'd likely ever see

ARMORY_UTXSVR_ENABLE = false
ARMORY_UTXSVR_PORT_MAINNET = 6590
ARMORY_UTXSVR_PORT_TESTNET = 6591
