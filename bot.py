#Connection script
##################
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


#This library is handy for working with .env files. 
#load_dotenv() loads environment variables from a .env file into your shell’s environment variables so that you can use them in your code.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#https://stackoverflow.com/questions/64231025/discord-py-bot-cant-see-members
intents = discord.Intents.default()
intents.members = True
intents.presences = True

# A Bot is a subclass of Client that adds a little bit of extra functionality that is useful when you’re creating bot users. 
# For example, a Bot can handle events and commands, invoke validation checks, and more.
bot = commands.Bot(command_prefix = '.', intents=intents)


#on_ready() will be called (and your message will be printed) once client is ready for further action.
@bot.event
async def on_ready():
    # find() takes a function, called a predicate, which identifies some characteristic of the element in the iterable that you’re looking for. 
    # Here, you used a particular type of anonymous function, called a lambda, as the predicate.
    guild = discord.utils.get(bot.guilds, name=GUILD)   
    members = '\n - '.join([member.name for member in guild.members])
    print(
            f'{bot.user} has connected to {guild.name} id: {guild.id} successfully!\n'
            f'Guild Members:\n - {members}'
        )

    # Counting active users and setting that number as activity
    number_of_users = sum(member.status != discord.Status.offline and not member.bot for member in guild.members)
    await bot.change_presence(activity=discord.Activity(name = f'{number_of_users} users. Use .help', type=3)) 


#bot.run() runs your Client using your bot’s token.
bot.load_extension("cogs.monitoring")
bot.load_extension("cogs.user")
bot.load_extension("cogs.admin")
bot.load_extension("cogs.events")
bot.run(TOKEN)
    