
import discord
from discord.ext import commands
from utils import OPSYSTEM, AUTHORISED_SERVER_IDS, get_server_state, get_player_count, run_script
SERVER_START_SCRIPT="~/scripts/start-server.sh"
SERVER_STOP_SCRIPT="~/scripts/log-check.sh"
SERVER_PLAYER_COUNT_SCRIPT="~/scripts/who-online.sh"


class Scommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot



    @discord.slash_command(
            name="test",
            description="Used for testing! 👽",
            guild_ids=AUTHORISED_SERVER_IDS
    )
    @commands.cooldown(rate=1, per=5*60) # WIP
    async def test(self, ctx: discord.ApplicationContext):
        await ctx.respond("Test success! 💪")

    @test.error
    async def test_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("Command is on cooldown! 💂‍♂️")
        else:
            raise error


    # Only after completing the server start procedure should we send
    # a followup response saying: "Server is up!"
    @discord.slash_command(
        name="server_start",
        description="Start up the server",
        guild_ids=AUTHORISED_SERVER_IDS
    )
    async def server_start(self, ctx: discord.ApplicationContext):
        # THIS defer method SAVED my life
        # For an app cmd it must return a response within 3 seconds of it being executed
        # If not, discord will say "unknown integration". Which is why we use defer to tell discord to wait
        await ctx.defer()
        if OPSYSTEM == "posix":
            if get_server_state() == 1:
                # Whenever a defer is called, it must be followed up with a send_followup method
                await ctx.send_followup(f"{ctx.author.mention} Server is already ONLINE")
            else:
                run_script(SERVER_START_SCRIPT)
                # Bash scripts are handling server state changes when related scripts are run
                # echo 1 > SERVER_STATE
                await ctx.send_followup("Booting up the server")
        else:
            await ctx.send_followup("💩 **ERROR:** MinecraftOpen is running on the wrong OS")


    @discord.slash_command(
        name="server_stop",
        description="Begins 10 minute countdown to stop the server. ALL players must be OFFLINE",
        guild_ids=AUTHORISED_SERVER_IDS
    )
    async def server_stop(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        run_script(SERVER_PLAYER_COUNT_SCRIPT)
        if get_player_count() > 0:
            await ctx.send_followup(f"⚠ **ERROR:** Player ONLINE {ctx.author.mention}")
            return 0
        if OPSYSTEM == "posix":
            if get_server_state() == 1:
                run_script(SERVER_STOP_SCRIPT)
                await ctx.send_followup("Starting 10 Min countdown\nWILL abort if player joins during countdown!")
            else:
                await ctx.send_followup(f"{ctx.author.mention} Server is already OFFLINE")
        else:
            await ctx.send_followup("💩 **ERROR:** MinecraftOpen is running on the wrong OS")


    # If u use the BOOT COMMAND + LIST COMMAND
    # within a short period of each other, the bot will CRASH!
    @discord.slash_command(
        name="server_list_number",
        description="Lists number of players currently on the server",
        guild_ids=AUTHORISED_SERVER_IDS
    )
    async def server_list_number(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        run_script(SERVER_PLAYER_COUNT_SCRIPT)
        numberOnline = get_player_count()
        await ctx.send_followup(f"Current players online: {numberOnline}")




def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Scommands(bot)) # add the cog to the bot