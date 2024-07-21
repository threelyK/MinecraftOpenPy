
import discord
import logging
from utils import BOT_TOKEN


# ------ LOGGER ------

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# ------ APP ------

bot = discord.Bot()
bot.load_extension('cogs.scommands')

@bot.event
async def on_ready():
    print(f"{bot.user} is operational!")


# ------ COMMANDS ------



bot.run(BOT_TOKEN)