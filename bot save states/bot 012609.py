import discord
import responses
from discord import app_commands
from discord.ext import commands
from discord.utils import get

#VARIABLES!!!
palworld_role = 1075832475395297398 #the role id for palworld players
role_request_channel = "" #the channel id for the role requests to be sent to

#NEXT TODO:
#Make it to where only people with a certain role ID can do a command
#Then, make a command where you can set server status
#make all command: /serveruptime or /servers running or /palworld

#make a method that launches the palworld server and stops the palworld server from this little lines of code

#only activates for those with a specific role

#message the bot for the role!


class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

#we've learned not to sync on start up so this is out
    async def setup_hook(self):
        #self.tree.copy_global_to(guild =discord.Object(id = 1075832475223330936))
        synced = await self.tree.sync()
        print(f"Synced {len(synced)} command(s)")

#logs messages sent in channel.
async def send_message(message, user_message, is_private): #async function for gathering messages and returning correct response
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
        
def run_discord_bot():
    #********************
    #Bot Start Commands
    #********************
    
    TOKEN = 'MTIwMDAwNDY1NzUyNzkyNjc4NQ.G-eP1v.IDqLoYRXFHh6Wiz7EOFoXeHJOXIyLub9lUnW6o'
    
    client = MyClient()
    
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        
    #*************
    #TEST COMMANDS
    #************
        
    @client.tree.command()
    async def hello(interaction: discord.Integration):
        """Say Hello!"""
        await interaction.response.send_message(f"Hello {interaction.user} and!", ephemeral=True)
    
    @client.tree.command()
    @app_commands.describe(message="What should I say?")
    async def say(interaction: discord.Integration, message: str): #for an ephemeral message so only the user sees it, we can do:
        """Tell me what to say"""
        await interaction.response.send_message(f"Hello {message}!", ephemeral=True)
    
    @client.tree.command()
    async def test(interaction: discord.Integration):
        """Testing: Role Declination!"""
        if palworld_role in [roles.id for roles in interaction.user.roles]:
            await interaction.response.send_message(f"Hello {interaction.user}! You have the red role!", ephemeral=True)
            
            # channel = client.get_channel(1075832478582976614)
            # await channel.send('hello')
        else:
            await interaction.response.send_message(f"Sorry, you do not have the correct role!", ephemeral=True)
        
        await interaction.response.send_message(f"Hello {interaction.user}! You have the red role!", ephemeral=True)
        
    
    @client.tree.command()
    @app_commands.describe(first='The first number to add', second='The second number to add')
    async def add(
        interaction: discord.Interaction,
        # This makes it so the first parameter can only be between 0 to 100.
        first: app_commands.Range[int, 0, 100],
        # This makes it so the second parameter must be over 0, with no maximum limit.
        second: app_commands.Range[int, 0, None],
    ):
        """Adds two numbers together"""
        await interaction.response.send_message(f'{first} + {second}  = {first + second}', ephemeral=True)
        
    @client.tree.command()
    async def privatechat(interaction: discord.Integration): #await interaction.response.send_message(f"Hello {name}!") #for an ephemeral message so only the user sees it, we can do:
        """Request a private chat!"""
        await interaction.response.send_message(f"Hello! To start a private chat, type '$!help'", ephemeral=True)
        
        
    #****************
    #private messaging
    #*****************
    
    @client.event
    async def on_message(message): #captures channel logs
        if message.author == client.user:
            return
        
        username = str(message.author)#whoever is writing
        user_message = str(message.content) #gets message content
        channel = str(message.channel)
        
        print(f'{username} said: "{user_message}" ({channel})')
        
        if user_message[0] == '$' and user_message[1] == '!': #if user types ? before a message, bot will interact
            user_message = user_message[2:] #this removes the '?' and processes message as normal
            await send_message(message, user_message, is_private=True)
        elif (message.guild): #makes sures message is sent via DM
            return
        else: #if message isnt $! and isnt sent in a guild, read and respond to message (basially DMS only)
            await send_message(message, user_message, is_private=True)
            
    client.run(TOKEN)
