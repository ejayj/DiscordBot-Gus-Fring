import discord
from discord import app_commands


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            #await tree.sync(guild =discord.Object(id = 1075832475223330936))
            self.synced = True
        print(f"We have logged in as {self.user}.")
        
client=aclient()
tree = app_commands.CommandTree(client)

@tree.command(name = "test", description = "testing")
async def self(interaction: discord.Integration, name: str):
    #await interaction.response.send_message(f"Hello {name}!")
    #for an ephemeral message so only the user sees it, we can do:
    await interaction.response.send_message(f"Hello {name}!", ephemeral=True)

TOKEN = 'MTIwMDAwNDY1NzUyNzkyNjc4NQ.G-eP1v.IDqLoYRXFHh6Wiz7EOFoXeHJOXIyLub9lUnW6o'
client.run(TOKEN)
