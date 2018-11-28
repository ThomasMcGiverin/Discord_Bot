import discord
from discord.ext import commands
import cassiopeia as cass

# API token for discord and riot api
DISCORD_TOKEN = "DISCORD_TOKEN_HERE"
RIOT_TOKEN = "RIOT_TOKEN_HERE"

cass.set_riot_api_key(RIOT_TOKEN)  # Link the Riot Games API to the cassiopeia wrapper
Client = discord.Client()
client = commands.Bot(command_prefix="~")  # Set command prefix (all commands for this bot are prefixed by ~)
client.remove_command("help")  # Remove default help command to allow for a creation of a custom one (HelpHub)

# Extensions array for loading all cogs
extensions = ["LeagueCommands", "MusicCommands", "MathCommands", "ModeratorCommands", "GeneralCommands", "HelpHub",
              "RoleCommands", "LevelAndCurrency", "Shop"]


# Change bot status and print a status message when ready
@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name="Type ~help"))
    print("Bot is online and connected to Discord")


# Command that loads a specified extension(cog)
@client.command()
async def load(extension):
    for extension in extensions:
        try:
            client.load_extension(extension)
            print("Loaded {}".format(extension))
        except Exception as error:
            print("{} Cannot be loaded. [{}]".format(extension, error))


# Command that unloads a specified extension(cog)
@client.command()
async def unload(extension):
    for extension in extensions:
        try:
            client.unload_extension(extension)
            print("Unloaded {}".format(extension))
        except Exception as error:
            print("{} Cannot be unloaded. [{}]".format(extension, error))


# Load all extensions when the bot is initialized
if __name__ == "__main__":
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as error:
            print("{} Cannot be loaded. [{}]".format(extension, error))
    client.run(DISCORD_TOKEN)
