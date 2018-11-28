from discord.ext import commands
import json
import os

# File to be used to store user data
os.chdir(r"File_Path_Here")
users_file = "users.json"


class LevelAndCurrency:
    """Cog that contains level and currency
       based commands and functionality"""

    # Initializer
    def __init__(self, client):
        self.client = client

    # When a new member joins the server, add their data to the users.json file
    async def on_member_join(self, member):
        with open(users_file, "r") as file:
            users = json.load(file)

        await self.update_data(users, member)

        with open(users_file, "w") as file:
            json.dump(users, file)

    # When a user sends a message in the server, increase their experience and currency total and check for level up
    async def on_message(self, message):
        with open(users_file, "r") as file:
            users = json.load(file)

        await self.update_data(users, message.author)
        await self.add_experience(users, message.author, 5)
        await self.add_currency(users, message.author, 10)
        await self.level_up(users, message.author, message.channel)

        with open(users_file, "w") as file:
            json.dump(users, file)

    '''If a user is not currently in the users.json file when they send a message or join the server then initialize 
       their experience, level, and currency'''
    async def update_data(self, users, user):
        if not user.id in users:
            users[user.id] = {}
            users[user.id]["experience"] = 0
            users[user.id]["level"] = 1
            users[user.id]["currency"] = 0

    # Function to add a specified amount of experience to a specified user
    async def add_experience(self, users, user, exp):
        users[user.id]["experience"] += exp

    # Function to add a specified amount of currency to a specified user
    async def add_currency(self, users, user, currency):
        users[user.id]["currency"] += currency

    # Function that calculates if a user should level up based on their current experience points total and level
    async def level_up(self, users, user, channel):
        experience = users[user.id]["experience"]
        level_start = users[user.id]["level"]
        level_end = int(experience ** (1/4))

        if level_start < level_end:
            await self.client.send_message(channel, "{} has leveled up to level {}".format(user.mention, level_end))
            users[user.id]["level"] = level_end

    # Command that outputs the total currency for whomever entered the command
    @commands.command(pass_context=True)
    async def bank(self, ctx):
        with open(users_file, "r") as file:
            users = json.load(file)

        for user in users:
            if user == ctx.message.author.id:
                await self.client.say("{} you have ${}".format("<@" + user + ">", users[user]["currency"]))

    # Command that outputs the current level for whomever entered the command
    @commands.command(pass_context=True)
    async def level(self, ctx):
        with open(users_file, "r") as file:
            users = json.load(file)

        for user in users:
            if user == ctx.message.author.id:
                await self.client.say("{} you are level {}".format("<@" + user + ">", users[user]["level"]))

    # Command that allowed a specified user to gift currency to another user
    @commands.command(pass_context=True)
    async def gift(self, ctx, identity, money):
        if ctx.message.author.id == "Server_owner_id_here":
            with open(users_file, "r") as file:
                users = json.load(file)

            for user in users:
                if user == identity:
                    await self.client.say("{} you have been gifted ${}".format("<@" + user + ">", money))
                    users[user]["currency"] += int(money)

            with open(users_file, "w") as file:
                json.dump(users, file)
        else:
            await self.client.say("You don't have permissions todo that")

    '''Command that displays all users in the server through the users.json file and all of their respective level and
       currency totals'''
    @commands.command(pass_context=True)
    async def leaderboard(self):
        with open(users_file, "r") as file:
            users = json.load(file)

        for user in users:
            name = "<@" + user + ">"
            await self.client.say("%s is level %s and has $%d" % (name, users[user]["level"], users[user]["currency"]))


def setup(client):
    client.add_cog(LevelAndCurrency(client))
