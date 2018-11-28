import discord
from discord.ext import commands


# List of words to be banned by the chat filter and the bypass list to exempt specific users from the filter
chat_filter = ["Banned_Word1", "Banned_Word2", "Banned_Word3"]
bypass_list = []


class ModeratorCommands:
    """Cog for commands based around server moderation"""

    # Initializer
    def __init__(self, client):
        self.client = client

    # Chat filter functionality that deletes any message that contains any of the chat_filter words
    async def on_message(self, message):
        contents = message.content.split(" ")
        for words in contents:
            if words.upper() in chat_filter:
                if not message.author.id in bypass_list:
                    try:
                        await self.client.delete_message(message)
                        await self.client.send_message(message.channel, "You arent allowed to use that word here!")
                    except discord.errors.NotFound:
                        return

    # Command that deletes the 'x' most recent chat messages where x is the amount specified by the user
    @commands.command(pass_context=True)
    async def clear(self, ctx, amount=10):
        if ctx.message.author.id == "Server_owner_id_here":
            channel = ctx.message.channel
            messages = []
            async for message in self.client.logs_from(channel, limit=int(amount)):
                messages.append(message)
            await self.client.delete_messages(messages)
        else:
            await self.client.say("You do not have permissions for this!")


def setup(client):
    client.add_cog(ModeratorCommands(client))
