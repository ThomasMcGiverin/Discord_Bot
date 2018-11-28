import discord
from discord.ext import commands


class GeneralCommands:
    """Cog for general purpose discord commands"""

    # Initializer
    def __init__(self, client):
        self.client = client

    # Command that displays general information about the given user
    @commands.command(pass_context=True)
    async def info(self, ctx, user: discord.Member):
        embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find.",
                              color=0x00ff00)
        embed.add_field(name="Name", value=user.name, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Status", value=user.status, inline=True)
        embed.add_field(name="Highest role", value=user.top_role)
        embed.add_field(name="Joined", value=user.joined_at)
        embed.set_thumbnail(url=user.avatar_url)
        await self.client.say(embed=embed)


def setup(client):
    client.add_cog(GeneralCommands(client))
