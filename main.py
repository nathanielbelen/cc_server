# main.py
import asyncio
from src.server import start_server

if __name__ == "__main__":
    asyncio.run(start_server())