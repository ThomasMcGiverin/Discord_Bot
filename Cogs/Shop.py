from discord.ext import commands
from random import randint
import json
import os


# Specify the file where user data is held
os.chdir(r"File_Path_Here")
users_file = "users.json"

# Read the compliments file into an array
compliments = r"File_Path_Here"
f = open(compliments, 'r')
lines = f.readlines()
f.close()


class Shop:
    """Cog that contains all shop items that
       users can purchase using their currency"""

    # Initializer
    def __init__(self, client):
        self.client = client

    '''Command to buy a compliment, the outputted compliment is chosen from a large list at random
       from the compliments file'''
    @commands.command(pass_context=True)
    async def buycompliment(self, ctx):
        cost = 100
        random = randint(0, len(lines)-1)
        with open(users_file, "r") as file:
            users = json.load(file)

        for user in users:
            if user == ctx.message.author.id:
                if users[user]["currency"] < cost:
                    await self.client.say("You don't have enough money! You need ${} more!"
                                          .format(cost-users[user]["currency"]))
                    return None
                else:
                    users[user]["currency"] -= cost
                    await self.client.say("Thank you for your purchase!")
                    await self.client.say("{} {} "
                                          .format("<@" + user + ">", lines[random].strip("\n")))

        with open(users_file, "w") as file:
            json.dump(users, file)


def setup(client):
    client.add_cog(Shop(client))
