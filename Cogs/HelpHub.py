import discord
from discord.ext import commands


class HelpHub:
    """Cog that contains a custom help command that
       provides specific information on every command
       that is currently supported"""

    # Initializer
    def __init__(self, client):
        self.client = client

    '''Custom help command that displays detailed information on the arguments of each command and the return value
       which is displayed through a direct message from the bot to the user who called the help command'''
    @commands.command(pass_context=True)
    async def help(self, ctx):
        author = ctx.message.author

        embed = discord.Embed(
            colour=discord.Colour.darker_grey()
        )

        embed.set_author(name="Big Brain Bot Command Information")
        embed.add_field(name="~calc <num1> <+ - / *> <num2>", value="Returns result of inputted operators and operand",
                        inline=False)
        embed.add_field(name="~clear <number>", value="Clears last <number> messages from current channel",
                        inline=False)
        embed.add_field(name="~cointoss", value="Returns Heads or Tails", inline=False)
        embed.add_field(name="~info <@user>", value="Returns user information", inline=False)
        embed.add_field(name="~Random <Lower Bound> <Upper Bound>",
                        value="Returns random number in range [Lower bound, Upper Bound]", inline=False)
        embed.add_field(name="~patch", value="Returns current League of Legends patch", inline=False)
        embed.add_field(name="~leagueinfo <ign> <region>", value="Returns league user information", inline=False)
        embed.add_field(name="~mastery <ign> <region>", value="Returns champion mastery info", inline=False)
        embed.add_field(name="~livegame <ign> <region>", value="Returns live game information", inline=False)
        embed.add_field(name="~play <youtubeURL> <Volume=50>", value="Plays linked song in current VC and clears queue",
                        inline=False)
        embed.add_field(name="~queue <youtubeURL> <Volume=50>", value="Adds linked song to queue", inline=False)
        embed.add_field(name="~pause", value="Pause current song", inline=False)
        embed.add_field(name="~resume", value="Resume playing current song", inline=False)
        embed.add_field(name="~skip", value="Skip to next song in queue", inline=False)
        embed.add_field(name="~disconnect", value="Terminates music bot", inline=False)
        embed.add_field(name="~bank", value="Display your current balance", inline=False)
        embed.add_field(name="~level", value="Display your current level", inline=False)
        embed.add_field(name="~buycompliment", value="Purchase a random compliment for $100", inline=False)

        await self.client.send_message(author, embed=embed)


def setup(client):
    client.add_cog(HelpHub(client))
