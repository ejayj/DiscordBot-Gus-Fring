import discord
from discord import app_commands
from discord.ext import commands


# intents = discord.Intents.default()
# intents.message_content = True
# client = discord.Client(intents=intents)

intents = discord.Intents.default()
intents.message_content = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents) #or .all

#so maybe

@bot.event
async def on_ready():
    print("Bot is up and ready!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="hello")
async def hello(interaction: discord.Integration):
    await interaction.response.send_message(f"Hello {interaction.user.mention}!", ephemeral=True)

    #interaction.response.send_message(f"Hello {interaction.user.mention}!", ephemeral=True)
    
@bot.tree.command(name='say')
#@bot.command(name='say') #this works?
@app_commands.describe(arg = "What should I say?")
async def say(interaction: discord.Interaction, arg: str):
    await interaction.response.send_message(f"{interaction.user.name} said: '{arg}'")

TOKEN = 'MTIwMDAwNDY1NzUyNzkyNjc4NQ.G-eP1v.IDqLoYRXFHh6Wiz7EOFoXeHJOXIyLub9lUnW6o'

bot.run(TOKEN)

# intents = discord.Intents.default()
#     intents.message_content = True
#     client = discord.Client(intents=intents)

