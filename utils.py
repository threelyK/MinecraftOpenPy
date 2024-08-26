
import os
import pathlib
from dotenv import load_dotenv


load_dotenv("./.env")
BOT_TOKEN= os.getenv("BOT_TOKEN")
AUTHORISED_SERVER_IDS=os.getenv("AUTHORISED_SERVER_IDS").strip("'[]").split(", ")
OPSYSTEM=os.name

ALLOWED_SERVER_IDS = list(map(int, AUTHORISED_SERVER_IDS))

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


# Server related variables

SERVER_INFO_PATH = pathlib.Path("server_info.json")

serverInfo = {
    "current_player_count": 0,
    "server_state": 0
}

