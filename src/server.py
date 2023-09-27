# websocket server class
# invoke in main
# respond to queries with keystate

from modules.key_state import Key_State
from src.common.keyboard_dict import keyboard_dict
from config import PI_IP_ADDRESS, PI_PORT
import asyncio
import time
import websockets

key_state = Key_State()

async def server(websocket):
    async for command in websocket:
        action, key = parse_input(command)
        if action == "down" or action == "up":
            if key in keyboard_dict:
                if action == "down":
                    key_state.key_down(key)
                else:
                    key_state.key_up(key)
            else:
                print("Invalid key")
        elif action == "release":
            key_state.key_release_all()
        else:
            print("Invalid command")

async def start_server():
    print("Running WebSocket server")
    async with websockets.serve(server, PI_IP_ADDRESS, PI_PORT):
        await asyncio.Future()  # run forever


def parse_input(input_str):
    # Split the input string into words
    words = input_str.split()

    # Check if the input contains at least one word
    if not words:
        return "Invalid", None

    # Extract the first word as the action
    action = words[0]

    # Initialize key as None
    key = None

    if action == "down" and len(words) > 1:
        key = words[1]
    elif action == "up" and len(words) > 1:
        key = words[1]
    elif action != "release":
        return "Invalid", None

    return action, key