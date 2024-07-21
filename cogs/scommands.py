
import discord
from discord.ext import commands
from utils import OPSYSTEM, SERVER_START_SCRIPT, SERVER_STOP_SCRIPT, AUTHORISED_SERVER_IDS, get_server_state, change_server_state, get_player_count, run_script

class Scommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot



    @discord.slash_command()
    async def hello(self, ctx: discord.ApplicationContext):
        await ctx.respond("Hey!")


    @discord.slash_command(
        name="server_start",
        description="Start up the server"
    )
    async def server_start(self, ctx: discord.ApplicationContext):
        # THIS defer method SAVED my life
        # For a app cmd it must return a response within 3 seconds of it being executed
        # If not, discord will say "unknown integration". Which is why we use defer to tell discord to wait
        await ctx.defer()
        if OPSYSTEM == "posix":
            if get_server_state() == 1:
                # Whenever a defer is called, it must be followed up with a send_followup method
                await ctx.send_followup(f"{ctx.author.mention} Server is already ONLINE")
            else:
                run_script(SERVER_START_SCRIPT)
                change_server_state(1)
                await ctx.send_followup("Booting up the server [WIP]")
        else:
            await ctx.send_followup(":poop: **ERROR:** MinecraftOpen is running on the wrong OS")


    @discord.slash_command(
        name="server_stop",
        description="Begins 10 minute countdown to stop the server. ALL players must be OFFLINE"
    )
    async def server_stop(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        if get_player_count() > 0:
            await ctx.send_followup("**ERROR:** Player ONLINE")
            return 0
        if OPSYSTEM == "posix":
            if get_server_state() == 1:
                run_script(SERVER_STOP_SCRIPT)
                change_server_state(0)
                await ctx.send_followup("Stopping the server [WIP]")
            else:
                await ctx.send_followup(f"{ctx.author.mention} Server is already OFFLINE")
        else:
            await ctx.send_followup(":poop: **ERROR:** MinecraftOpen is running on the wrong OS")

    @discord.slash_command(
        name="server_list",
        description="Lists all players currently on the server"
    )
    async def server_list(self, ctx: discord.ApplicationContext):
        await ctx.respond(f"Current players: [WIP]")




def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Scommands(bot)) # add the cog to the bot