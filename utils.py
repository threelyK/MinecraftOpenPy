
import os
# Look into using "subprocess" module instead of os
from dotenv import load_dotenv


load_dotenv("./.env")
BOT_TOKEN= os.getenv("BOT_TOKEN")
AUTHORISED_SERVER_IDS=os.getenv("AUTHORISED_SERVER_IDS").strip("'[]").split(", ")
OPSYSTEM=os.name

ALLOWED_SERVER_IDS = list(map(int, AUTHORISED_SERVER_IDS))

def run_script(fileDirectory: str):
    os.system(fileDirectory)


def update_info(infoVar, state):
    os.system(f"python3 infoManager.py --update {infoVar+"/"+state}")