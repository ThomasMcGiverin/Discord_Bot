import discord
from discord.ext import commands
import cassiopeia as cass
from cassiopeia import Summoner


class LeagueCommands:
    """Cog for League of Legends related commands that
       utilize the Riot Games API"""

    # Initializer
    def __init__(self, client):
        self.client = client

    # Command that displays the current League of Legends patch
    @commands.command(pass_context=True)
    async def patch(self):
        version = cass.get_version(region="NA")
        await self.client.say("Current LoL patch: " + version.strip(".1"))

    # Command that displays general league of legends related information on a specified username and region
    @commands.command(pass_context=True)
    async def leagueinfo(self, ctx, name, reg):

        try:
            status = "Currently Ingame"
            summoner = Summoner(name=name, region=reg.upper())
            summonername = summoner.name
            previousrank = summoner.rank_last_season
            iconinfo = cass.ProfileIcon(id=summoner.profile_icon.id, region=reg.upper())

            embed = discord.Embed(title="{}'s info".format(summonername), description="Here's what I could find.",
                                  color=0x07419e)
            embed.add_field(name="Name", value=summonername, inline=True)
            try:
                cass.core.spectator.CurrentMatch(summoner=name, region=reg.upper())
            except:
                status = "Not Ingame"
            embed.add_field(name="Status", value=status, inline=True)
            embed.add_field(name="Previous Season Rank", value=previousrank)
            embed.add_field(name="Region", value=reg.upper())
            embed.set_thumbnail(url=iconinfo.url)
            await self.client.say(embed=embed)
        except:
            await self.client.say("Error: Invalid name or region.")
            return None

    # Command that displays champion mastery information for a specified username and region
    @commands.command(pass_context=True)
    async def mastery(self, ctx, name, reg):
        summoner = Summoner(name=name, region=reg.upper())
        try:
            champ_name = summoner.champion_masteries[0].champion.name
        except:
            await self.client.say("This summoner doesn't exist!")
            return None

        embed = discord.Embed(title="{}'s Top 5 Mastery".format(name), color=0x07419e)

        for i in range(0, 5):
            champ_name = summoner.champion_masteries[i].champion.name
            mastery_points = cass.ChampionMastery(summoner="Venerated", region="NA", champion=champ_name).points
            embed.add_field(name=champ_name, value=str(mastery_points), inline=False)
        await self.client.say(embed=embed)

    # Command that displays live game information for a specified username and region
    @commands.command(pass_context=True)
    async def livegame(self, ctx, name, reg):
        try:
            match = cass.core.spectator.CurrentMatch(summoner=name, region=reg.upper())
            embed = discord.Embed(title="{}'s Current Game. {}".format(name, match.duration),
                                  description="Live game data", color=0x07419e)

            blueteam = []
            redteam = []

            for i in range(0, 5):
                blueteam.append(match.participants[i].summoner.name)
            for i in range(5, 10):
                redteam.append(match.participants[i].summoner.name)

            embed.add_field(name="BLUE TEAM", value=blueteam[0] + "\n" + blueteam[1] + "\n" + blueteam[2] + "\n" +
                                                    blueteam[3] + "\n" + blueteam[4])
            embed.add_field(name="RED TEAM", value=redteam[0] + "\n" + redteam[1] + "\n" + redteam[2] + "\n" +
                                                   redteam[3] + "\n" + redteam[4])
            await self.client.say(embed=embed)
        except:
            await self.client.say("{} is not current ingame!".format(name))
            return None


def setup(client):
    client.add_cog(LeagueCommands(client))
