from discord.ext import commands
from discord.ext.commands.errors import MissingAnyRole, MissingPermissions


class EventLoggingCog(commands.Cog, name = "Events"):
    """This cog contains functions to log suspicious events"""

    def __init__(self, bot):
        self.bot = bot

    # To check for errors and log them
    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        with open("err.log", 'a') as f:
            if event == "on_message":
                f.write(f"Unhandled message: {args[0].content.encode('utf-8')}\n")
            else:
                # Print last received exception in the console.
                raise

    # Send command errors to the discord channel
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(error, delete_after = 5)
        elif isinstance(error, MissingPermissions):
            await ctx.send("Wooow bud, stop right there. You don't have enough permissions! :skull:", delete_after = 5)
        elif isinstance(error, MissingAnyRole):
            await ctx.send("Ey bud, you are not admin, wake up!", delete_after = 5)


def setup(bot):
    bot.add_cog(EventLoggingCog(bot))