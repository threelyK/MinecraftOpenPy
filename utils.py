
import os, subprocess
from dotenv import load_dotenv


load_dotenv("./.env")
BOT_TOKEN= os.getenv("BOT_TOKEN")
AUTHORISED_SERVER_IDS=os.getenv("AUTHORISED_SERVER_IDS").strip("'[]").split(", ")
OPSYSTEM=os.name

ALLOWED_SERVER_IDS = list(map(int, AUTHORISED_SERVER_IDS))

def run_script(fileDirectory: str):
    command = "sh " + fileDirectory
    subprocess.run(command, shell=True)


def update_info(infoVar: str, state: int):
    parameter = "python infoManager.py --update " + infoVar+"/"+str(state)
    subprocess.run(parameter, shell=True)
