
import discord, time
from discord.ext import commands
from infoManager import load_server_info
from utils import OPSYSTEM, ALLOWED_SERVER_IDS, run_script, update_info
SERVER_START_SCRIPT="~/scripts/start-server.sh"
SERVER_STOP_SCRIPT="~/scripts/stop-server.sh"
BACKUP_SCRIPT="~/scripts/backup.sh"
SERVER_PLAYER_COUNT_SCRIPT="~/scripts/playerCount.sh"

# Any serverInfo variables should be changed within commands when possible.
# Avoid changing those variables outside of python files if able.


def isRunningLinux() -> bool:
    # posix = Linux
    if OPSYSTEM == "posix":
        return True
    else:
        return False


class Scommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @discord.slash_command(
            name="test",
            description="Used for testing! 👽",
            guild_ids=ALLOWED_SERVER_IDS,
    )
    async def test(self, ctx: discord.ApplicationContext):
        await ctx.respond("Test success! 💪")


    # Only after completing the server start procedure should we send
    # a followup response saying: "Server is up!"
    @discord.slash_command(
        name="server_start",
        description="Start up the server",
        guild_ids=ALLOWED_SERVER_IDS,
    )
    @commands.cooldown(rate=1, per=5*60)
    @commands.max_concurrency(number=1, per=commands.BucketType.guild) # Limits usage to one at a time
    async def server_start(self, ctx: discord.ApplicationContext):
        # THIS defer method SAVED my life
        # For an app cmd it must return a response within 3 seconds of it being executed
        # If not, discord will say "unknown integration". Which is why we use defer to tell discord to wait
        await ctx.defer()
        if isRunningLinux():
            serverInfo = load_server_info()
            if serverInfo.get('server_state') == 1:
                # Whenever a defer is called, it must be followed up with a send_followup method
                await ctx.send_followup(f"🛑 **ERROR:** {ctx.author.mention} Server is already ONLINE!")
            else:
                run_script(SERVER_START_SCRIPT)
                await ctx.send_followup("Booting up the server!")
                update_info("server_state", 1)
                time.sleep(5*60)
                await ctx.delete()
                await ctx.send_followup(f"{ctx.author.mention} Server is now Online! 🔛")
        else:
            await ctx.send_followup("💩 **ERROR:** MinecraftOpen is running on the wrong OS!")
            discord.ApplicationCommand.reset_cooldown(self.server_start, ctx)

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
        description="Stops the server only if ALL players are OFFLINE",
        guild_ids=ALLOWED_SERVER_IDS
    )
    @commands.cooldown(rate=1, per=10*60)
    @commands.max_concurrency(number=1, per=commands.BucketType.guild)
    async def server_stop(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        run_script(SERVER_PLAYER_COUNT_SCRIPT)
        serverInfo = load_server_info()
        if serverInfo.get('player_count') > 0:
            await ctx.send_followup(f"🛑 **ERROR:** {ctx.author.mention} There is a player online, unable to shutdown.")
            discord.ApplicationCommand.reset_cooldown(self.server_stop, ctx)
            return 0
        if isRunningLinux():
            if serverInfo.get('server_state') == 1:
                run_script(SERVER_STOP_SCRIPT)
                update_info("server_state", 0)
                await ctx.send_followup("Starting shutdown! 💤")
            else:
                await ctx.send_followup(f"{ctx.author.mention} Server is already OFFLINE")
                discord.ApplicationCommand.reset_cooldown(self.server_stop, ctx)
        else:
            await ctx.send_followup("💩 **ERROR:** MinecraftOpen is running on the wrong OS")
            discord.ApplicationCommand.reset_cooldown(self.server_stop, ctx)

    @server_stop.error
    async def server_stop_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(f"🛑 **ERROR:** {ctx.author.mention} Command is on cooldown! Try again in {round(error.retry_after)} seconds. 💂‍♂️")
        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.respond(f"🛑 **ERROR:** {ctx.author.mention} Command has already been called by another! Please wait for that to complete. 📵")
        else:
            raise error


    @discord.slash_command(
        name="server_list_number",
        description="Lists the number of players currently on the server",
        guild_ids=ALLOWED_SERVER_IDS
    )
    @commands.cooldown(rate=1, per=10)
    async def server_list_number(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        serverInfo = load_server_info()
        await ctx.send_followup(f"Current players online: {serverInfo.get('player_count')}")

    @server_list_number.error
    async def server_list_number_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(f"🛑 **ERROR:** {ctx.author.mention} Command is on cooldown! Try again in {round(error.retry_after)} seconds. 💂‍♂️")
        else:
            raise error


    @discord.slash_command(
        name="server_backup",
        description="Begins a world backup if the Server is OFF",
        guild_ids=ALLOWED_SERVER_IDS
    )
    @commands.cooldown(rate=1, per=30*60)
    @commands.max_concurrency(number=1, per=commands.BucketType.guild)
    async def server_backup(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        if isRunningLinux():
            serverInfo = load_server_info()
            if serverInfo.get('server_state') == 1:
                await ctx.send_followup(f"🛑 **ERROR:** Unable to produce backup, server is running! {ctx.author.mention}")
            else:
                await ctx.send_followup(f"Creating backup...")
                run_script(BACKUP_SCRIPT)
                time.sleep(2*60)
                await ctx.delete()
                await ctx.send_followup(f"Backup save created!")
        else:
            await ctx.send_followup("💩 **ERROR:** MinecraftOpen is running on the wrong OS")

    @server_backup.error
    async def server_backup_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(f"🛑 **ERROR:** {ctx.author.mention} Command is on cooldown! Try again in {round(error.retry_after)} seconds. 💂‍♂️")
        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.respond(f"🛑 **ERROR:** {ctx.author.mention} Command has already been called by another! Please wait for that to complete. 📵")
        else:
            raise error


    @discord.slash_command(
        name="force_server_backup",
        description="🦺 Authorised Personnel Only. Forces a world backup if the Server is OFF",
        guild_ids=ALLOWED_SERVER_IDS
    )
    @commands.check_any(commands.is_owner())
    async def force_server_backup(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        if isRunningLinux():
            serverInfo = load_server_info()
            if serverInfo.get("server_state") == 1:
                await ctx.send_followup(f"🛑 **ERROR:** Unable to produce backup, server is running! {ctx.author.mention}")
            else:
                await ctx.send_followup(f"Creating backup...")
                run_script(BACKUP_SCRIPT)
                time.sleep(2*60)
                await ctx.delete()
                await ctx.send_followup(f"Backup save created!")
        else:
            await ctx.send_followup("💩 **ERROR:** MinecraftOpen is running on the wrong OS")


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Scommands(bot)) # add the cog to the bot