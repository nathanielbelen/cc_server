# websocket server class
# invoke in main
# respond to queries with keystate

from src.modules.key_state import Key_State
from src.common.keyboard_dict import keyboard_dict
from config import PI_IP_ADDRESS, PI_PORT
import asyncio
import time
import random
import websockets

key_state = Key_State()

async def server(websocket):
    try:
        async for command in websocket:
            action, key = parse_input(command)
            if action == "down" or action == "up" or action == "quick" or action == "direction":
                if key in keyboard_dict:
                    if action == "down":
                        key_state.key_down(key)
                    elif action == "up":
                        key_state.key_up(key)
                    elif action == "quick":
                        # is this blocking behavior bad?
                        key_state.key_down(key)
                        time.sleep(random.uniform(0.075, 0.85))
                        key_state.key_up(key)
                    elif action == "direction":
                        key_state.direction(key)
                else:
                    print("Invalid key")
            elif action == "release":
                key_state.key_release_all()
            else:
                print("Invalid command")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed with error: {e}")
    except ConnectionResetError as e:
        print(f"Connection reset by peer: {e}")

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
    elif action == "quick" and len(words) > 1:
        key = words[1]
    elif action == "direction" and len(words) > 1:
        key = words[1]
    elif action != "release":
        return "Invalid", None

    return action, key