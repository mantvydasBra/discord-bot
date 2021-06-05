import re

import discord
from discord.errors import Forbidden
from discord.ext import commands


class MonitoringCog(commands.Cog, name = "Monitoring"):
    """A main cog for monitoring activities, chat and server overall."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(invoke_without_command = True, hidden = True)
    async def help(self, ctx, *input):
        """The main place where you can get information about my powers!
        So yea... Just type .help for to see all the modules and .help <module> to find information about its commands!
        """

        # Just getting owner name, nothing special
        owner = await self.bot.fetch_user(177677230091141121)
        
        if not input:
            embed = discord.Embed(title = "Here are all the modules", colour = discord.Color.orange(),
                                            description = f"The main place where you can get information about my powers!\n \
                                                            So yea... Just type `.help` to see all the modules and `.help [module]` to find information about its commands! \
                                                            :chart_with_upwards_trend:\n")
            
            # This will search for commands in all of the cogs
            for cog in self.bot.cogs:
                if cog.lower() != "monitoring":
                    embed.add_field(name = cog, value = self.bot.cogs[cog].__doc__, inline = False)

            # This will search for commands that aren't in any cog or hidden
            commands = ''
            for command in self.bot.walk_commands():
                if not command.cog_name and not command.hidden:
                    embed.add_field(name = "Not in any module", value = commands.name, inline = False)

            embed.add_field(name="About", value=f"The Bots is developed by ₚₚ ᵉⁿᵉʳᶢ ꙷ#8097 and is based on discord.py.\n\
                                            This version of it is maintained by {owner}\n\
                                            Please visit https://pornhub.com to submit ideas or bugs.")
            embed.set_footer(text=f"Bot is running a spicy v6.9 :sunglasses:")            
        
        elif len(input) == 1:
            # Prints information about all commands in a selected module
            for cog in self.bot.cogs:
                if cog.lower() == input[0].lower():
                    embed = discord.Embed(title=f'{cog} - Commands', description=self.bot.cogs[cog].__doc__,
                                            color=discord.Color.green())

                    for command in self.bot.get_cog(cog).get_commands():
                        if not command.hidden:
                            embed.add_field(name=f"`.{command.name}`", value=command.help, inline=False)

                    break
                # If there is no such module
                else:
                    embed = discord.Embed(title="What the fuck are you looking for!?",
                                        description=f"You being a bitch :100: I've never heard of `{input[0]}` before :triumph:",
                                        color=discord.Color.red())
                    

        elif len(input) > 1:
            await ctx.send("Nah mate, that's too much! Give me less work :triumph:")
            return

        else:
            await ctx.send("You trying something fishy :face_with_monocle:\nI understand you :nerd:")
            return


        try:
            # Trying to send whole embeded help command (just to make it more beautiful)
            await ctx.send(embed = embed)
        except Forbidden:
            # If the bot couldn't send the command, he will try to inform that he doesn't have enough permissions
            try:
                await ctx.send("I can't send embeds. Check the permissions.")
            except Forbidden:
                await ctx.author.send(
                    f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                    f"May you inform that server's maintainer {owner} about this issue? :slight_smile: ", embed=embed)


    
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Monitor messages

        React to messages such as hey bot, beep and i love you.
        Check if a message is not in black list, otherwise delete it.
        """

        if message.author == self:
            return
        
        with open("banned_words.txt") as f:
            black_words = f.read().split('\n')

        if re.search("^([hH]ey bot)", message.content):
            response = f"Hello @{message.author.mention}! I'm just chilling... :)"
            await message.channel.send(response)
        elif message.content == "beep":
            response = f"boop"
            await message.channel.send(response)
        elif message.content == "i love you":
            response = f"I love you too!!! :***"
            await message.channel.send(response)
        elif any(word in message.content.split() for word in black_words):
            await message.delete()
            await message.channel.send(f"No blacklisted words >:(", delete_after = 3)
        elif message.content == "raise-exception":
            raise discord.DiscordException


        # Overriding the default provided on_message forbids any extra commands from running. 
        # To fix this, add a bot.process_commands(message) line at the end of your on_message
        #await self.process_commands(message)

    @commands.Cog.listener()
    async def on_member_join(member):
        # Send a direct message to a user who just joined the server.
        await member.create_dm()
        await member.dm_channel.send(f'Hello {member.name}! Welcome to the club, you fucking faggot')


def setup(bot):
    # Setup the bot
    bot.remove_command("help")
    bot.add_cog(MonitoringCog(bot))