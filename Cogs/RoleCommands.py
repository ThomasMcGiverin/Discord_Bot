import discord


class RoleCommands:
    """Cog for server role related commands
       and functionality"""

    # Initializer
    def __init__(self, client):
        self.client = client

    # When a new member joins the server automatically give them a server role and greet them
    async def on_member_join(self, member):
        role = discord.utils.get(member.server.roles, name="Knight")
        await self.client.add_roles(member, role)
        await self.client.say("Welcome To My Server!")


def setup(client):
    client.add_cog(RoleCommands(client))
