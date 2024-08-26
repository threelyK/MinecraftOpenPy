
import discord
from discord.ext import commands
from utils import OPSYSTEM, ALLOWED_SERVER_IDS, get_server_state, get_player_count, run_script
SERVER_START_SCRIPT="~/scripts/start-server.sh"
SERVER_STOP_SCRIPT="~/scripts/log-check.sh"
SERVER_PLAYER_COUNT_SCRIPT="~/scripts/who-online.sh"


class Scommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot



    @discord.slash_command(
            name="test",
            description="Used for testing! 👽",
            guild_ids=ALLOWED_SERVER_IDS
    )
    # @commands.cooldown(rate=1, per=5*60)
    async def test(self, ctx: discord.ApplicationContext):
        await ctx.respond("Test success! 💪")


    # Only after completing the server start procedure should we send
    # a followup response saying: "Server is up!"
    @discord.slash_command(
        name="server_start",
        description="Start up the server",
        guild_ids=ALLOWED_SERVER_IDS
    )
    @commands.cooldown(rate=1, per=5*60)
    @commands.max_concurrency(number=1, per=commands.BucketType.guild) # Limits usage to one at a time
    async def server_start(self, ctx: discord.ApplicationContext):
        # THIS defer method SAVED my life
        # For an app cmd it must return a response within 3 seconds of it being executed
        # If not, discord will say "unknown integration". Which is why we use defer to tell discord to wait
        await ctx.defer()
        if OPSYSTEM == "posix":
            if get_server_state() == 1:
                # Whenever a defer is called, it must be followed up with a send_followup method
                await ctx.send_followup(f"🛑 **ERROR:** {ctx.author.mention} Server is already ONLINE!")
            else:
                run_script(SERVER_START_SCRIPT)
                # Bash scripts are handling server state changes when related scripts are run
                # echo 1 > SERVER_STATE
                await ctx.send_followup("Booting up the server!")
        else:
            await ctx.send_followup("💩 **ERROR:** MinecraftOpen is running on the wrong OS!")

    @server_start.error
    async def server_start_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(f"🛑 **ERROR:** {ctx.author.mention} Command is on cooldown! Try again in {round(error.retry_after)} seconds. 💂‍♂️")
        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.respond(f"🛑 **ERROR:** {ctx.author.mention} Command has already been called by another! Please wait for that to complete. 📵")
        else:
            raise error


    @discord.slash_command(
        name="server_stop",
        description="Begins 10 minute countdown to stop the server. ALL players must be OFFLINE",
        guild_ids=ALLOWED_SERVER_IDS
    )
    async def server_stop(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        run_script(SERVER_PLAYER_COUNT_SCRIPT)
        if get_player_count() > 0:
            await ctx.send_followup(f"🛑 **ERROR:** {ctx.author.mention} There is a player online, unable to shutdown.")
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
        guild_ids=ALLOWED_SERVER_IDS
    )
    @commands.cooldown(rate=1, per=10)
    async def server_list_number(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        run_script(SERVER_PLAYER_COUNT_SCRIPT)
        numberOnline = get_player_count()
        await ctx.send_followup(f"Current players online: {numberOnline}")


    @discord.slash_command(
        name="server_backup",
        description="Begins a world backup if the Server is OFF",
        guild_ids=ALLOWED_SERVER_IDS
    )
    @commands.cooldown(rate=1, per=30*60)
    async def server_backup(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        if get_server_state() == 1:
            await ctx.send_followup(f"🛑 **ERROR:** Unable to produce backup, server is running! {ctx.author.mention}")
        else:
            #Backup world file
            # Send msg before backup is finished "Creating backup save!"
            ctx.send_followup(f"WIP does nothing")


    @discord.slash_command(
        name="force_server_backup",
        description="👷‍♂️ Authorised Personnel Only. Forces a world backup if the Server is OFF",
        guild_ids=ALLOWED_SERVER_IDS
    )
    async def force_server_backup(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        if get_server_state() == 1:
            await ctx.send_followup(f"🛑 **ERROR:** Unable to produce backup, server is running! {ctx.author.mention}")
        else:
            #Backup world file
            # Send msg before backup is finished "Creating backup save!"
            ctx.send_followup(f"WIP does nothing")


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Scommands(bot)) # add the cog to the bot