from discord.ext import commands


# Dictionaries to keep track of each server and their music bot instance
queues = {}
players = {}


# Check if there is a song in the queue, if so play it
def check_queues(server_id):
    if queues[server_id] != []:
        player = queues[server_id].pop(0)
        players[server_id] = player
        player.start()


class MusicCommands:
    """Cog for all music related commands
       and music player functionality"""

    # Initializer
    def __init__(self, client):
        self.client = client

    # Command to play a song given by a youtube url
    @commands.command(pass_context=True)
    async def play(self, ctx, url, volume=50.0):
        channel = ctx.message.author.voice.voice_channel
        try:
            await self.client.join_voice_channel(channel)
            server = ctx.message.server
            voice_client = self.client.voice_client_in(server)
            player = await voice_client.create_ytdl_player(url, after=lambda: check_queues(server.id))
            players[server.id] = player
            player.start()
            player.volume = float(volume)/100.0
            await self.client.say(":musical_note: `{}` Now Playing! :musical_note:".format(player.title))
        except:
            server = ctx.message.server
            voice_client = self.client.voice_client_in(server)
            await voice_client.disconnect()
            await self.client.join_voice_channel(channel)
            server = ctx.message.server
            voice_client = self.client.voice_client_in(server)
            player = await voice_client.create_ytdl_player(url, after=lambda: check_queues(server.id))
            players[server.id] = player
            player.start()
            player.volume = 0.4
            await self.client.say(":musical_note: `{}` Now Playing! :musical_note:".format(player.title))

    # Command to add a given youtube url to a queue to be played in order once the previous songs end
    @commands.command(pass_context=True)
    async def queue(self, ctx, url, volume=50.0):
        server = ctx.message.server
        voice_client = self.client.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url, after=lambda: check_queues(server.id))
        player.volume = float(volume) / 100.0

        if server.id in queues:
            queues[server.id].append(player)
        else:
            queues[server.id] = [player]
        await self.client.say(":musical_note: `{}` added to queue! :musical_note:".format(player.title))

    # Command that pauses the music
    @commands.command(pass_context=True)
    async def pause(self, ctx):
        id = ctx.message.server.id
        players[id].pause()

    # Command that skips to the next song in the queue if there is one
    @commands.command(pass_context=True)
    async def skip(self, ctx):
        id = ctx.message.server.id
        players[id].stop()

    # Command that resumes playback of a song if one is currently paused
    @commands.command(pass_context=True)
    async def resume(self, ctx):
        id = ctx.message.server.id
        players[id].resume()

    # Command that forces the music to stop playing and for the bot to disconnect from the voice channel
    @commands.command(pass_context=True)
    async def disconnect(self, ctx):
        server = ctx.message.server
        voice_client = self.client.voice_client_in(server)
        await voice_client.disconnect()


def setup(client):
    client.add_cog(MusicCommands(client))
