
import os
from dotenv import load_dotenv


load_dotenv("./.env")
BOT_TOKEN= os.getenv("BOT_TOKEN")
AUTHORISED_SERVER_IDS=os.getenv("AUTHORISED_SERVER_IDS")
OPSYSTEM=os.name

# Server state tracker function
# 0 = Off, 1 = On
def get_server_state() -> int:
    with open("./SERVER_STATE", "r") as serverStateFile:
        return int(serverStateFile.read())


def get_player_count() -> int:
    with open("./PLAYER_COUNT", "r") as plrCountFile:
        return int(plrCountFile.read())


def run_script(fileDirectory: str):
    os.system(fileDirectory)