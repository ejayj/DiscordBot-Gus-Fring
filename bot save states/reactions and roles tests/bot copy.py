import asyncio
import discord
import responses
from discord import SelectOption, app_commands
from discord.ext import commands
from discord.utils import get
from discord.ui import Select, View

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
        
    # #sync command
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
    
    #***************
    #REACTION ROLES
    #***************
    REACTION_CHANNEL_ID=1200237595217641563
    
    #creates the reaction message and adds emoji.
    #i could also transfer this into a command to trigger this message
    
    # @client.event
    # async def on_ready():
    #     Channel = client.get_channel(REACTION_CHANNEL_ID)
    #     Text= "YOUR_MESSAGE_HERE"
    #     Moji = await Channel.send(Text)
    #     await Moji.add_reaction('🏃')
    
    #*************************************
    
    #detects all reactions on the server in specified, reaction channel id
    #to have multiple reaction channels, i would add a tuple of channel ids in the reaction_channel_id
    
    # @client.event    
    # async def on_reaction_add(user, reaction: discord.Reaction):
    #     reaction_emoji=""
    #     #these variables are switches for some reason, but 'user' MUST come firest
    #     username=reaction #tempvar
    #     reaction=user
    #     user=username 
        
    #     #check if reaction was in the right channel. i would like this to be apart of the initial message however.
    #     if reaction.message.channel.id != REACTION_CHANNEL_ID:
    #         print("wrong channel")
    #         return
        
    #     #check if reaction was from bot (ignore)
    #     if client.user == user:
    #         print("this was from bot")
    #         return
        
    #     print(f'User {user} added reaction {reaction} in channel')
    #     # bot_channel = discord.Client.get_channel(self, REACTION_CHANNEL_ID)
    #     # await bot_channel.send(content=f"A rating of {reaction} was placed in {reaction.message.channel} for link {reaction.message.content}")
    
    @client.tree.command()  
    async def roll(interaction: discord.Integration):
        # def check(reaction,user):  # Our check for the reaction
        #     return user == interaction.user  # We check that only the authors reaction counts

        # message = await interaction.response.send_message("Please react to the message!")  # Message to react to ; ephemeral=True
        # await message.add_reaction('👍')

        Channel = client.get_channel(REACTION_CHANNEL_ID)
        message = await Channel.send('Are you enjoying this bot? \n :thumbsup: :-1: ')
        await message.add_reaction('👍')
        
        # reaction = await client.wait_for("reaction_add", check=check)  # Wait for a reaction
        
        # await interaction.response.send_message(f"You reacted with: {reaction[0]}")  # With [0] we only display the emoji
        
        
        def check(reaction, user):
            # if client.user == user:
            #       print("this was from bot")
            #       return
            #print(reaction.emoji)
            return user == interaction.user #and str(reaction.emoji) == '👍'
        
        def reaction_response(reaction):
            if reaction=='👍':
                print("Yes!")
                return True           
            return False

        #receive reaction
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            print('exception:')
            reaction_response(reaction)
        else:
            print('no exceptions')
            
        if reaction_response(reaction.emoji):
            print("we reach heere")
            #server = client.get_guild(1075832475223330936)
            member = interaction.user
            #role = get(interaction.guild.roles)
            #role = discord.utils.get(server.roles, palworld_role)
            #role = server.get_role(palworld_role)
            role = get(member.guild.roles, name="Red")
            await member.add_roles(role)
            

        #message = await interaction.response.send_message('Are you enjoying this bot? \n :thumbsup: :-1: ')
#name='feedback', help='Ask person for feedback'

        # thumb_up = '👍'
        # thumb_down = '👎'
        
        # Channel = client.get_channel(REACTION_CHANNEL_ID)
        # message = await Channel.send('Are you enjoying this bot? \n :thumbsup: :-1: ')
        # #await message.add_reaction('🏃')

        # await message.add_reaction(thumb_up)
        # await message.add_reaction(thumb_down)
        
        #********

        # def check(reaction, user):
        #     return user == interaction.user and str(
        #         reaction.emoji) in [thumb_up, thumb_down]

        # reaction = await client.wait_for("reaction_add", timeout=10.0, check=check)
        
        # if str(reaction.emoji) == thumb_up:
        #             await interaction.response.send_message('Thank you for your feedback')
        # # while True:
        # #     print("we reach here")
        # #     try:
        # #         reaction = await client.wait_for("reaction_add", timeout=10.0, check=check)

        # #         if str(reaction.emoji) == thumb_up:
        # #             await interaction.response.send_message('Thank you for your feedback')


        # #         if str(reaction.emoji) == thumb_down:
        # #             await interaction.response.send_message('Sorry you feel that way')
        # #     except:
        # #         pass
        
        
        
        #TWO TYPES OF REACTION MESSAGES:
        #Ephemeral if i can
        #public, for all to see, such as in rules. I can also check what pluretha of reactions were done. i want it to only check a specific channel for these interactions though.
            
    #*************
    #DEV COMMANDS
    #************
    @client.tree.command()
    async def sync(interaction: discord.Integration):
        """Sync commands!"""
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)!")
        await interaction.response.send_message(f"Synced {len(synced)} command(s)!", ephemeral=True)
        
    @client.tree.command()
    async def syncguild(interaction: discord.Integration):
        """Sync commands to this guild only!"""
        client.tree.copy_global_to(guild =discord.Object(id = 1075832475223330936))
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s) to dev guild!")
        await interaction.response.send_message(f"Synced {len(synced)} command(s) to dev guild!", ephemeral=True)
        
        
    #*************
    #TEST COMMANDS
    #************
    
    @client.tree.command()
    async def test(interaction: discord.Integration):
        """Testing: Role Declination!"""
        if palworld_role in [roles.id for roles in interaction.user.roles]:
            await interaction.response.send_message(f"Hello {interaction.user}! You have the red role!", ephemeral=True)
            
            channel = client.get_channel(1075832478582976614)
            await channel.send('hello')
        else:
            await interaction.response.send_message(f"Sorry, you do not have the correct role!", ephemeral=True)
            
    #serverinfo [what server? categories using tuples]
    #returns "running", "stopped", "closed", and runtime if applicable
    #posts in chat
    
    #start server -> specify what server. role locked; if another server is running, and we're at server max (2), then you cant start one and need to request a server to be oepened
    
    #stop a server -> specify what server [make sure its on]; role locked
    
    #i can only run pal world or minecraft, or 2 minecraft severs.
    
    #requestserver
    #sends DM to modlog with ping @ejay to start a server.
    
    #modhelp:
    #choose from list issue category, who its with (n/a for none),  specify issue/outcome desired
    #let them know their request has been receieved! and they will get a DM with the status of the issue
    #SEND DM: "Your request: 'issue category' is [STATUS]
    #Statuses: PENDING -> RECEIVED/REJECTED [REASON] -> UNDER REVIEW -> ANSWERED [answer]/WAITING RESPONSE/CLOSED
    #these will get saved in a json on local host machine
    
    #in a separate channel, I will get the request. I can answer each request via ID using json. /respond [ID] [Status] [Message]
    #for statuses like rejected, or answered/more info needed, the message will be sent to the user
    
    #categories in tuple: [has to be a number]
    #1. Role request
    #2. Server issue
    #3. Discord issue
    #4. Player issue
    #5. Other
    
    #****************
    #SERVER COMMANDS
    #****************
    
    @client.tree.command()
    async def startserver(interaction: discord.Integration):
        """Start a server"""
        await interaction.response.send_message(f"Server Started")
        print(f"Started [SERVER]")
        #message: too many servers started! use /requeststart server
    
    @client.tree.command()    
    async def stopserver(interaction: discord.Integration):
        """Stop a server"""
        await interaction.response.send_message(f"Server Stopped")
        print(f"Stopped [SERVER]")
    
    @client.tree.command()
    async def serverinfo(interaction: discord.Integration):
        """Request info on a server!"""
        await interaction.response.send_message(f"Server info:", ephemeral=True)
        print(f"Info on: [SERVER]")
    
    @client.tree.command()
    async def requeststartserver(interaction: discord.Integration):
        """Request a server to be started!"""
        await interaction.response.send_message(f"Server Stopped")
        print(f"Info on: [SERVER]")
    
    @client.tree.command()   
    async def modhelp(interaction: discord.Integration):
        """Request help from a mod!"""
        await interaction.response.send_message(f"Check your DMs!")
        
    @client.tree.command()
    async def helpi(interaction: discord.Integration):
        embed = discord.Embed(title="Help panel!", description="Your Desc")
        select = Select(
            placeholder="Select something",
            options=[
                SelectOption(label="😆 - Fun", value="1", description="Get all commands according to \"Fun\""),
                SelectOption(label="🪛 - Utility", value="2", description="Get all commands according to \"Utility\""),
                SelectOption(label="❓ - Info", value="3", description="Get all commands according to \"Info\""),
                SelectOption(label="🎭 - Roleplay", value="4", description="Get all commands according to \"Roleplay\""),
                SelectOption(label="🪙 - Economy", value="5", description="Get all commands according to \"Economy\""),
                SelectOption(label="🛑 - Cancel", value="Cancel", description="Cancel this interaction.")
            ]
        )
        async def callback(interaction):
            if select.values[0] == "1":
                await interaction.response.send_message("Test")
            elif select.values[0] == "2":
                await interaction.response.send_message("Test")
            elif select.values[0] == "3":
                await interaction.response.send_message("Test")
            elif select.values[0] == "4":
                await interaction.response.send_message("Test")
            elif select.values[0] == "5":
                await interaction.response.send_message("Test")
        select.callback = callback
        view = View()
        view.add_item(select)
        await interaction.response.send_message("ABC", embed=embed, view=view)
    
    #*************
    #STOCK COMMANDS
    #*************
    
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
