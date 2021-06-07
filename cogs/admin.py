
import asyncio
import typing
from discord.ext import commands
from discord.ext.commands.converter import Greedy
from discord.member import Member
from discord.ext.commands.core import bot_has_permissions


class AdminCog(commands.Cog, name = "Admin"):
    """This is the admin cog.
    In this place you'll find various commands that require admin privileges to run.
    There will also be some commands that only the server admin can run, because these can brake the functionality of bot if overused.
    """

    def __init__(self, bot):
        self.bot = bot
        self.tasks = []

    # Can add words or sentences into a black list, which the bot monitors and deletes.
    @commands.command(name = "black_list_words", help = "If you want for me to delete specific words, you can view and add them here.")
    @commands.has_role(770042216751955999)
    async def black_words(self, ctx, *, message = None):
        if message != None:
            with open("banned_words.txt", "a") as f:
                f.write(message + "\n")
            await ctx.send(f"Successfully added `{message}` to my watchout list 0_0", delete_after = 5)
        else:
            await ctx.send("Banned words are: ")
            with open("banned_words.txt", "r") as f:
                await ctx.send("```" + f.read() + "```")


    @commands.command(   name = "delete_messages", 
                    help = "I'm going to quickly delete specified number of messages from speicified user (optional). Default number of messages is 1." 
    )
    @bot_has_permissions(manage_messages = True, read_message_history = True)   # Checks if bot has permissions
    @commands.has_permissions(manage_messages = True, read_message_history = True)  # Checks if user has permissions
    async def purge_messages(self, ctx, users: Greedy[Member], number: int = 1):
        """Delete specified amount of messages from specified member.
        If the number isn't specified, the bot will delete 1 message by default.
        If the user isn't specified, the bot will take into account every message.
        By default, calling command with no options, bot will delete last message.
        """
        # Check if the author isn't the bot it self.
        if ctx.author == self:
            return

        # Returns true if no users are entered and true if message author is the specified user.
        def _check(message):
            return not len(users) or message.author in users    

        # Check for not doing infinite ammounts of deletions.
        if 0 < number <= 50:
            await ctx.channel.purge(limit=number, check = _check)
        elif number == 0:
            await ctx.message.delete()
            await ctx.send("I can't delete 0 messages >:(", delete_after = 3)
        elif number < 0:
            await ctx.message.delete()
            await ctx.send("Are you trying something fishy here :face_with_monocle:", delete_after = 3)
        elif number > 50:
            await ctx.message.delete()
            await ctx.send("Fuck you, that's too much :(", delete_after = 3)


    @commands.command(name = "mute", help = "I will keep that chad muted for specified reason and amount of time (seconds).", pass_context = True)
    @commands.has_permissions(kick_members = True)
    async def mute(self, ctx, user: Member, time: typing.Optional[int], *, reason: str = None):
        # Check if the author isn't the bot it self.
        if ctx.author == self:
            return
        elif not user:
            await ctx.send("JAJAJAJ you need to specify who to mute!")
            return
        mute_role = ctx.guild.get_role(849722695066976276)
        
        if mute_role in user.roles:
            # Checks if user already has muted role
            # Maybe do unmute in future?
            await user.remove_roles(mute_role, reason = "Well, I guess everyone gets better... You can speak freely!")
            await ctx.send(f"Well, I guess everyone gets better... You can speak freely {user.mention}!")
            try:
                for task in self.tasks:
                    if str(user) == task.get_name():
                        task.cancel()                    
            except Exception as ex:
                print(ex)
            return
        elif self == user:
            await ctx.send("Shut yo bitch ass up! I'm more powerful than you and you cannot mute me!")
        else:
            try:
                await user.add_roles(mute_role, reason = reason)
            except Exception as e:
                print(e)
            await ctx.send(f"{user.mention} has been muted by {ctx.author.mention} for: *{reason}*")

        self.tasks.append(asyncio.create_task(timeout(time, user, mute_role, ctx), name = str(user)))
        lll = asyncio.gather(*self.tasks, return_exceptions = True)
        try:
            for task in self.tasks:
                print(task.get_name())
        except Exception as ex:
            print(ex)
        # print(asyncio.Task.print_stack)
        # asyncio.Task.print_stack
        # [*map(asyncio.Task.print_stack, asyncio.Task.all_tasks())]
        # if time > 0:
        #     await asyncio.sleep(time)
        #     for user in users:
        #         try:
        #             await user.remove_roles(mute_role, reason = "That's all for today, you are free to go!")
        #             await ctx.send(f"That's all for today, you are free to go {user.mention}!")
        #         except Exception as e:
        #             print(e)
                
        


        

        

########################################COG RELATED COMMANDS, ONLY FOR ADMIN################################

    
    @commands.command(name = "load_cog", help = "Loads selected cog.")
    @commands.is_owner()
    async def load(self, ctx, extension: str):
        if extension.lower() == "games":
            extension = "user"
        elif extension.lower() == "monitoring":
            await ctx.send("Oh no buddy you're going to brake me :pleading_face:", delete_after = 5)
            return
        else:
            await ctx.send("Sorry, but I can't find this module :pensive:", delete_after = 5)
            return
        
        self.bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"Damn nice, I found {extension} and loaded it.", delete_after = 5)

    @commands.command(name = "unload_cog", help = "Unloads selected cog.")
    @commands.is_owner()
    async def unload(self, ctx, extension: str):
        if extension.lower() == "games":
            extension = "user"
        elif extension.lower() == "monitoring":
            await ctx.send("Oh no buddy you're going to brake me :pleading_face:", delete_after = 5)
            return
        else:
            await ctx.send("Nah my G, stop comming up wit these stoopid names :triumph:", delete_after = 5)
            return
        
        self.bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f"Successfully took off {extension} of my shoulders!", delete_after = 5)


    @commands.command(name = "reload_cog", help = "Reloads selected cog.")
    @commands.is_owner()
    async def reload(self, ctx, extension: str):
        if extension.lower() == "games":
            extension = "user"
        elif extension.lower() == "monitoring":
            await ctx.send("Hmmm, I think we can try this... What's the worst thing that could happen? :thinking:", delete_after = 5)
        elif extension == "":
            await ctx.send("C'mon guy, please provide me something to reload!", delete_after = 5)
            return 

        try:
            found = chk_extension(self, extension)
        except Exception as e:
            print(e)
        if not found:
            await ctx.send("Bruv, I can't reload something that I don't have :angry:", delete_after = 5)


        try:
            self.bot.reload_extension(f"cogs.{extension}")
            await ctx.send(f"Nice I think I got it unloaded, loaded, unloaded and loaded. I just did it like 30 times...", delete_after = 5)  #Idea to add how many times bot reloaded cogs
        except Exception as e:
            ctx.send(e)

    
async def chk_extension(bot, extension) -> bool:
    check = False
    for extensions in bot.cogs:
        if (extension == extensions.lower()):
            check = True
            break
    return check

async def timeout(time, user, mute_role, ctx):
    if time > 0:
            await asyncio.sleep(time)
            try:
                await user.remove_roles(mute_role, reason = "That's all for today, you are free to go!")
                await ctx.send(f"That's all for today, you are free to go {user.mention}!")
            except Exception as e:
                print(e)

def setup(bot):
    bot.add_cog(AdminCog(bot))