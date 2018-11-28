from discord.ext import commands
from random import randint
import random as rand


class MathCommands:
    """Cog for all mathematics related commands"""

    # Initializer
    def __init__(self, client):
        self.client = client

    # Command that outputs a pseudo random number in a specified range
    @commands.command(pass_context=True)
    async def random(self, ctx, x, y):
        if x < y:
            await self.client.say("Your random number from {} to {} is : {}".format(x, y, randint(int(x), int(y))))
        else:
            await self.client.say("Invalid range")

    # Command that uses a pseudo random number that is either 0 or 1 to simulate a coin toss
    @commands.command(pass_context=True)
    async def cointoss(self):
        toss = rand.randint(0,1)
        if toss == 0:
            await self.client.say("Heads!")
        else:
            await self.client.say("Tails!")

    # Command to utilize a simple calculator that takes two operands and applies one of the four possible operators
    @commands.command(pass_context=True)
    async def calc(self, ctx, operand1, operator, operand2):
        if operator == '+':
            await self.client.say(float(operand1) + float(operand2))
        elif operator == "-":
            await self.client.say(float(operand1) - float(operand2))
        elif operator == "/":
            await self.client.say(float(operand1) / float(operand2))
        elif operator == "*":
            await self.client.say(float(operand1) * float(operand2))
        else:
            await self.client.say("Error")


def setup(client):
    client.add_cog(MathCommands(client))
