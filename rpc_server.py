# rpc_server.py

import os
from fastapi import FastAPI
from web3 import Web3, HTTPProvider
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Load RPC URLs from .env
RPC_URL = os.getenv("RPC_URL", "https://GBTNetwork")
FALLBACK_RPC_URL = os.getenv("FALLBACK_RPC_URL", "https://gbtnetwork-render.onrender.com")
CHAIN_ID = os.getenv("CHAIN_ID", "999")
SYMBOL = os.getenv("SYMBOL", "GBT")

def connect_to_rpc():
    for url in [RPC_URL, FALLBACK_RPC_URL]:
        try:
            web3 = Web3(HTTPProvider(url))
            if web3.isConnected():
                print(f"✅ Connected to: {url}")
                return web3
        except Exception as e:
            print(f"❌ Failed to connect to {url}: {e}")
    raise ConnectionError("Unable to connect to any configured RPC URL.")

web3 = connect_to_rpc()

@app.get("/")
def root():
    return {
        "network": "GBTNetwork Layer 1",
        "connected": web3.isConnected(),
        "rpc": web3.provider.endpoint_uri,
        "chain_id": CHAIN_ID,
        "symbol": SYMBOL
    }

@app.get("/block/latest")
def get_latest_block():
    try:
        block = web3.eth.get_block("latest")
        return {
            "number": block.number,
            "hash": block.hash.hex(),
            "timestamp": block.timestamp,
            "transactions": len(block.transactions)
        }
    except Exception as e:
        return {"error": str(e)}
