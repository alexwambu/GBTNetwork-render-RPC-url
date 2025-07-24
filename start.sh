#!/bin/bash
uvicorn rpc_server:app --host 0.0.0.0 --port 10000
