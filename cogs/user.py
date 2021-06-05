
import random
from discord.activity import Game

from discord.ext import commands

class GamesCog(commands.Cog, name = "Games"):
    """A cog for games that all users can play."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "roll_dice", help = "I'm just going to roll a normal, 6 sided dice.")
    async def roll(self, ctx, number_of_dice: int):
        """A command to roll a 6 sided dice. Number of dices can be chosen by the user."""

        if 1 < number_of_dice <= 300:
            dice = [
                str(random.choice(range(1, 7)))
                for i in range(number_of_dice)
            ]
            # Sending the output to the same chat
            await ctx.send("Here are your fucking dices :dizzy_face:: " + ', '.join(dice), delete_after = 10)
        elif number_of_dice == 0:
            await ctx.send("Oh okey bud, here you go, I've rolled it 0 times! :rolling_eyes: Nice try", delete_after = 5)
        elif number_of_dice < 0:
            await ctx.send("Trying to exploit me? Not gonna happen, BITCH :sunglasses:", delete_after = 5)
        elif number_of_dice > 300:
            await ctx.send(f"Ye ye ye... I know you really want to roll {number_of_dice} times, but my Creator loves me and made it so I don't have to work past 300.\n"
                            "Not that I can't, ofcourse :eyes:", delete_after = 5)

def setup(bot):
    bot.add_cog(GamesCog(bot))