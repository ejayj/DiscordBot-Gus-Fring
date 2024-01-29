import discord
import responses
from discord import app_commands
from discord.ext import commands

async def send_message(message, user_message, is_private): #async function for gathering messages and returning correct response
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
        
def run_discord_bot():
    TOKEN = 'MTIwMDAwNDY1NzUyNzkyNjc4NQ.G-eP1v.IDqLoYRXFHh6Wiz7EOFoXeHJOXIyLub9lUnW6o'
    
    #we must set the intents for the discord bot to run
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)
    bot = commands.Bot(command_prefix='/', intents=intents)
    
    @bot.event
    async def on_ready():
        print("Bot is up and ready!")
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)
        
    @bot.tree.command(name="say")
    @app_commands.describe(arg = "What should I say?")
    async def say(interaction: discord.Interaction, arg: str):
        await interaction.response.send_message(f"{interaction.user.name} said: '{arg}'")
    
    @tree.command(name = "test", description = "testing")
    async def self(interaction: discord.Integration, name: str):
    #await interaction.response.send_message(f"Hello {name}!")
    #for an ephemeral message so only the user sees it, we can do:
        await interaction.response.send_message(f"Hello {name}!", ephemeral=True)
    
    @client.event
    async def on_ready2():
        print(f'{client.user} is now running!')
        
    @client.event #on client event, do something
    async def on_message(message): #my own function -> on message sent
        if message.author == client.user:
            return
        
        username = str(message.author)#whoever is writing
        user_message = str(message.content) #gets message content
        channel = str(message.channel)
        
        print(f'{username} said: "{user_message}" ({channel})')
        
        if user_message[0] == '?': #helps but understand the user is talking to the bot. so the first char of user message is '?' or '?help'
            user_message = user_message[1:] #this removes the '?' and processes message as normal
            await send_message(message, user_message, is_private=True)
        else:
            #user_message = user_message[1:]
            await send_message(message, user_message, is_private=False)
            
    client.run(TOKEN)
    
    
    