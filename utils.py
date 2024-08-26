
import os
from dotenv import load_dotenv
from infoManager import get_server_info


load_dotenv("./.env")
BOT_TOKEN= os.getenv("BOT_TOKEN")
AUTHORISED_SERVER_IDS=os.getenv("AUTHORISED_SERVER_IDS").strip("'[]").split(", ")
OPSYSTEM=os.name

ALLOWED_SERVER_IDS = list(map(int, AUTHORISED_SERVER_IDS))

# Server state tracker function
# 0 = Off, 1 = On
def get_server_state() -> int:
    return get_server_info("server_state")

# Player count getter
def get_player_count() -> int:
    return get_server_info("player_count")
    


def run_script(fileDirectory: str):
    os.system(fileDirectory)