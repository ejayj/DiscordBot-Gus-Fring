import asyncio
import unicodedata
import discord
import responses
from discord import SelectOption, app_commands
from discord.ext import commands
from discord.utils import get
from discord.ui import Select, View
import json
from pathlib import Path



#TODO: UTILIZING BOT
#add rules channel to reaction message/id. if someone removes or adds ANY emoji, i want it to supply or remove a role
#change mature member to regular member in the add/remove_role function

#next, i want to make a role: server starter. People can start/stop servers with this role, and people will know. 

#next, supply simple help commands. Additionally, i want to hide admin commands if possible.


#VARIABLES!!!
palworld_role = 1075832475395297398 #the role id for palworld players
role_request_channel = "" #the channel id for the role requests to be sent to

REACTION_CHANNEL_ID = set() #set of reaction channel ids
REACTION_MESSAGE = set() #set of reaction message ids
MODHELP_TICKET_IDS = set() #a set of ticket ids
TICKETS = dict #blank dict of current tickets and their info
ROLES = dict # a blank dict of role ids  we want to have saved

#Starts up bot config
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
    
#official start bot  
def run_discord_bot():

    #bot start info and important on ready commands
    TOKEN = 'MTIwMDAwNDY1NzUyNzkyNjc4NQ.G-eP1v.IDqLoYRXFHh6Wiz7EOFoXeHJOXIyLub9lUnW6o'
    
    client = MyClient()
    
    @client.event
    async def on_ready():
        await create_json_if_dne()
        print(f'{client.user} is now running!')
        
    
    
    #NEXT TODO:
    #1: get all members of desired role
    #2: get list of members who reacted to a certain message
    #3: if they are on roles list, but not reacted, remove roles
    
    #when someone reacts to the message automatically, they will recieve role
    #see below for that functionality
    
    #B. Clean up Variables
    
    #C. Begin working on server-functions; runtime will count by itself via bot and from /startserver function -> add ping info?
    
    #D. Eventually, transfer over to PC so we can test the file opening functions
    
    #E. Fix permission of chicken bot - it may need to have certain perms to add roles (or be above it in heirarchy)
    
    #F. Send out chicken bto for official production and put it on my resume!


    
      
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
        
    #****************
    #SUPPORT COMMANDS
    #*****************
    async def add_role(member): #we could add name=role variable. DEV NOTE:  mature member will eventually just be member in official production
        #member = interaction.user
        role = get(member.guild.roles, name="Mature Member")
        await member.add_roles(role)

    async def remove_role(member):
        #member = interaction.user
        role = get(member.guild.roles, name="Mature Member")
        await member.remove_roles(role)        
        
    #*************
    #SERVER COMMANDS INFO/IDEAS
    #************
    #make all command: /serveruptime or /servers running or /palworld
    #make a method that launches the palworld server and stops the palworld server from this little lines of code
    #message bot for roles! or for help
    
    #serverinfo [what server? categories using tuples]
    #returns "running", "stopped", "closed", and runtime if applicable
    #posts in chat
    
    #start server -> specify what server. role locked; if another server is running, and we're at server max (2), then you cant start one and need to request a server to be oepened; ONLY perople with a certain role should be able to do this; if already running, it should not spam the file multiple times
    
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
    
    
    #Sstop all servers upon bot start
    
    #categories in tuple: [has to be a number]
    #1. Role request
    #2. Server issue
    #3. Discord issue
    #4. Player issue
    #5. Other
    
    #createfunction where you got o reaction channel and just type /reactionc hannel
    #and it iwll save to tuple
    #****************
    #SERVER COMMANDS - TBD
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
        
    #**********************************************************************************
    #private messaging
    #**********************************************************************************
    
    #sends message in private when called
    async def send_message(message, user_message, is_private): #async function for  gathering messages and returning correct response
        try:
            response = responses.get_response(user_message)
            await message.author.send(response) if is_private else await message.channel.   send(response)
        except Exception as e:
            print(e)
        
        
    #reads all messages, prints/logs it in console. can respond
    @client.event
    async def on_message(message): #captures channel logs
        if message.author == client.user:
            return
        
        username = str(message.author)#whoever is writing
        user_message = str(message.content) #gets message content
        channel = str(message.channel)
        
        print(f'{username} said: "{user_message}" ({channel})')
        
        #edit this to allow bot to response. Can response in private (edit in response.py)
        if user_message[0] == '$' and user_message[1] == '!': #if user types ? before a message, bot will interact
            user_message = user_message[2:] #this removes the '?' and processes message as normal
            await send_message(message, user_message, is_private=True)
        elif (message.guild): #makes sures message is sent via DM
            return
        else: #if message isnt $! and isnt sent in a guild, read and respond to message (basially DMS only)
            await send_message(message, user_message, is_private=True)
    
    #******************************************************************************
    #DETECT REACTIONS
    #*******************************************************************************
     
    #************************
    #Create Reaction 
    #************************

    #A Command to show reaction roles -> lock this command to admins.
    @client.tree.command()
    @app_commands.describe(message_input="Enter Message Here", emoji="Enter Standard Emoji Here")
    async def create_reaction(interaction: discord.Integration, message_input: str, emoji: str):
        """Create a reaction message here!"""
        #This message will be sent to whatever slash-command the channel was done in
        Channel = interaction.channel
        message = await Channel.send(f'{message_input}')

        try:
            await message.add_reaction(emoji)
        except Exception as e:
            print(f'ERROR: INVALID EMOJI FROM {interaction.user}')
            await message.delete()
            await interaction.response.send_message("Invaid emoji! Please try again!", ephemeral=True)
            
        #add reactions to json saveto trigger and event
        REACTION_MESSAGE.add(message.id)
        REACTION_CHANNEL_ID.add(Channel.id)
        save_to_json()
        
    #***************
    #DETECT ADD REACTIONS
    #***************
    
    #detects all reactions on the server, does something if in specified, reaction channel/message id
    @client.event    
    async def on_raw_reaction_add(reaction: discord.Reaction):
        global REACTION_CHANNEL_ID, REACTION_MESSAGE
        reaction_emoji=reaction.emoji #the reacted emoji
        user=await client.fetch_user(reaction.user_id) #the user who reacted
        channel = client.get_channel(reaction.channel_id) #channel name
        print(f'User {user} added reaction {reaction_emoji} in channel {channel}')
        
        if await check_reaction(reaction,user):
            #depending on what message id, it will trigger different events
            if reaction.message_id==1201423318960574464: #the rules message
                await add_role(user) #gives member role
                return
            else:
                print('this reaction could trigger something')
        #i could also write a switch statement here. If reaction = a certain emoji, execute this particular function e.g. give role
        
    #***************
    #DETECT REMOVE REACTIONS
    #***************
    @client.event
    async def on_raw_reaction_remove(reaction: discord.Reaction):
        global REACTION_CHANNEL_ID, REACTION_MESSAGE
        reaction_emoji=reaction.emoji #or reaction.emoji
        user=await client.fetch_user(reaction.user_id) #i can also see channel_id and message_id
        channel = client.get_channel(reaction.channel_id) #channel name
        
        print(f'User {user} removed reaction {reaction_emoji} in channel {channel}')
        
        if await check_reaction(reaction,user):
            #depending on what message id, it will trigger different events
            if reaction.message_id==1201423318960574464: #the rules message
                await add_role(user) #takes away member role
                return
            else:
                print('this reaction could trigger something')
    
    #***************
    #GENERIC CHECK FOR REACTIONS
    #***************   
    
    #checks if a reaction is something we need to act on    
    async def check_reaction(reaction, user):
        
        #check if reaction was from bot (ignore)
        if client.user == user:
            #print("this reaction was from this bot")
            return False
        
        #check if reaction was in the right channel.
        for channel in REACTION_CHANNEL_ID:
            if reaction.channel_id == channel:
                break
        else:
            #print("Reaction not in correct channel")
            return False
    
        #check if reaction was to the right message
        for message in REACTION_MESSAGE: #really we just need its id
            if message == reaction.message_id: #if a reaction message, continue
                break
        else: #if the reacted-to message id wasnt in our reaction message sets, return
            #print("Reaction not on right message")
            return False
        
        return True #if all else is okay, reaction check is true -> we do soemthing here
    
    #**********************************************************************************
    #STOCK EXAMPLE COMMANDS 
    #**********************************************************************************
    
    #*************
    #BASIC RESPONSE
    #*************
    @client.tree.command()
    async def basicresponse(interaction: discord.Integration):
        """Say Hello!"""
        await interaction.response.send_message(f"Hello!")
        
    #*************
    #BASIC RESPONSE W/NAME, HIDDEN
    #*************
    @client.tree.command()
    async def basicresponsehidden(interaction: discord.Integration):
        """Say Hello!"""
        await interaction.response.send_message(f"Hello {interaction.user}", ephemeral=True)
    
    #*************
    #BASIC RESPONSE W/ INPUT
    #*************
    @client.tree.command()
    @app_commands.describe(message="What should I say?")
    async def say(interaction: discord.Integration, message: str): #for an ephemeral message so only the user sees it, we can do:
        """Tell me what to say"""
        await interaction.response.send_message(f"Hello {message}!", ephemeral=True)

    #*************
    #BASIC MULTI-INPUT COMMAND
    #*************
    @client.tree.command()
    @app_commands.describe(first='The first number to add', second='The second number to add')
    async def add_example(
        interaction: discord.Interaction,
        # This makes it so the first parameter can only be between 0 to 100.
        first: app_commands.Range[int, 0, 100],
        # This makes it so the second parameter must be over 0, with no maximum limit.
        second: app_commands.Range[int, 0, None],
    ):
        """Adds two numbers together"""
        await interaction.response.send_message(f'{first} + {second}  = {first + second}', ephemeral=True)
    
    #*************
    #PRIV CHAT TRIGGER COMMANDS
    #*************
    @client.tree.command()
    async def privatechat(interaction: discord.Integration): #await interaction.response.send_message(f"Hello {name}!") #for an ephemeral message so only the user sees it, we can do:
        """Request a private chat!"""
        #await interaction.response.send_message(f"Hello! This isa private chat!", ephemeral=True)
        #or
        await client.send_message(interaction.user, "Hello! This isa private chat!")
        
    #*************
    #MENU OPTION COMMANDS
    #*************
    
    @client.tree.command()
    async def menuoptions(interaction: discord.Integration):
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
        
    #***********************
    #BASIC ROLE-LOCKED COMMMAND
    #***********************
        
    @client.tree.command()
    async def testrolelock(interaction: discord.Integration):
        """Testing: Role Locks!"""
        if palworld_role in [roles.id for roles in interaction.user.roles]:
            await interaction.response.send_message(f"Hello {interaction.user}!You have the red role!", ephemeral=True)
            #triggers message sent to other channel
            #channel = client.get_channel(1075832478582976614)
            #await channel.send('hello')
        else:
            await interaction.response.send_message(f"Sorry, you do not have the  correct role!", ephemeral=True)
        #i could easily use get role, and have the name on ready here as a var:
        #member = interaction.user
        #role = get(member.guild.roles, name="Red")
        #I can then simply say you don thave the role {role} or {role.name}
        #i can also set the role using the roleid in the role = get() func
        
        
    
        
        
    #************************
    #REACTION ROLE ON -SLASH COMMAND
    #************************

    #A Command to show reaction roles
    @client.tree.command()  
    async def addreactionrolestest(interaction: discord.Integration):

        #This message will be sent to whatever slash-command the channel was done in
        await interaction.response.send_message("Please react to the message!")
        #ephemeral=True) #Ephemeral doesnt work w this 
        message = await interaction.original_response()
        await message.add_reaction('👍')

        #OR WE CAN DO:

        #This message will be sent to a specific channel, and add a reaction
            
        # Channel = client.get_channel(REACTION_CHANNEL_ID)
        # message = await Channel.send('Are you enjoying this bot? \n :thumbsup: :-1: ')
        # await message.add_reaction('👍')


        #receive reaction
        def check(reaction, user):
            return user == interaction.user #and str(reaction.emoji) == '👍'

        #check if reaction = what we're lookjing for
        def reaction_response(reaction):
            if reaction=='👍':
                print("Yes!")
                return True           
            return False

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0,    check=check)
        except asyncio.TimeoutError:
            pass
        else:
            pass

        #if correct emoji, you get "red" role. if not, it removes it. can add else if statements for more versatility.
        if reaction_response(reaction.emoji):
            member = interaction.user
            role = get(member.guild.roles, name="Red")
            await member.add_roles(role)
        else:
            #remove roll if not thumbs up
            member = interaction.user
            role = get(member.guild.roles, name="Red")
            await member.remove_roles(role)
            
    #***********************
    #READ WHO REACTED TO A MESSAGE + REMOVE ROLE ()
    #***********************
    channel_id = 1200237595217641563  # Replace with channel id
    message_id = 1201104168178430012  # Note these are ints, not strings

    @client.tree.command()
    async def listreactors1(interaction: discord.Integration):
        channel = client.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        users = set()
        for reaction in message.reactions:
            async for user in reaction.users():
                users.add(user)
        await interaction.response.send_message(f"users: {', '.join(user.name for user in users)}")

        # #to remove roles from pepeople
        # for user in users:
        #     print(user.name)
        #     #remove role
        #     member = interaction.user
        #     role = get(member.guild.roles, name="Red")
        #     await member.remove_roles(role)
        # #it should remove users NOT in role... 
               
               
    #***********************
    #SEND MESSAGE W EMOJI ON READY(AUTO)
    #***********************
    #Sends message and reaction emoji on ready
    #@client.event
    #async def on_ready():
    #     Channel = client.get_channel(REACTION_CHANNEL_ID)
    #     Text= "YOUR_MESSAGE_HERE"
    #     Moji = await Channel.send(Text)
    #     await Moji.add_reaction('🏃')
    
    
                
    client.run(TOKEN) #official 'start bot' command

#**********************************************************************************
#JSON FUNCTION CALLS
#**********************************************************************************

#create json save file upon startup
async def create_json_if_dne():
    my_file = Path("./botjson.json")
    if my_file.exists():
        print('File "botjson.json exits.')
        await load_json_data()
        return
    
    print('File "botjson.json" file does not exit. Creating new.')
    
    #if i wanted to, i could make the dictionary a tuple of dictionarys with guild_id as header. 
    #each guild dict would have a list of its own role ids and etc. for rxn roles
    stock_dict = {
    "REACTION_MESSAGES": [],
    "REACTION_CHANNELS": [],
    "ROLES": [{}],
    "MODHELP_TICKET_IDS": [0],
    "TICKETS": [{ 
                    "TICKET_ID": 0,
                    "USER": "USER_NAME",
                    "USER_ID": 0,
                    "CATEGORY": "5. Other",
                    "STATUS": "CLOSED",
                    "MESSAGE": "PLAYER MESSAGE HERE"
    }]
    }
    
    # Serializing json
    json_object = json.dumps(stock_dict, indent=4)
    
    # Writing to botjson.json
    with open("botjson.json", "w") as outfile:
        outfile.write(json_object)
    
    print('Create file "botjson.json" with stock data.')

#load json data upon startup if it exits (called from create_json_if_dne function)
async def load_json_data():
    print('Loading JSON DATA')
    with open("botjson.json", "r") as infile:
        loaded_dict= json.load(infile)
    
    print('Setting JSON Data to Variables')
    #print(loaded_dict)
    
    for x in range(0,3):
        print()
    
    #converts data to vars and back into sets
    global REACTION_MESSAGE
    REACTION_MESSAGE=set(loaded_dict["REACTION_MESSAGES"])
    print("Reaction Message IDS:")
    print(REACTION_MESSAGE)
    for x in range(0,2): print()
    
    global REACTION_CHANNEL_ID
    REACTION_CHANNEL_ID=set(loaded_dict["REACTION_CHANNELS"])
    print("Reaction Channel IDS:")
    print(REACTION_CHANNEL_ID)
    for x in range(0,2): print()
    
    global ROLES
    ROLES=loaded_dict["ROLES"]
    print("Saved Role IDs:")
    print(ROLES)
    print()
    
    global MODHELP_TICKET_IDS
    MODHELP_TICKET_IDS=set(loaded_dict["MODHELP_TICKET_IDS"])
    print("Modhelp Ticket Ids:")
    print(MODHELP_TICKET_IDS)
    for x in range(0,2): print()
    
    global TICKETS
    TICKETS=loaded_dict["TICKETS"]
    print("Modhelp Tickets:")
    print(TICKETS)
    print()

#saves all variables to json
async def save_to_json():
    
    #load dict data
    print('Saving....Loading JSON DATA')
    with open("botjson.json", "r") as infile:
        loaded_dict= json.load(infile)
    
    print('Setting Variables to JSON DATA')
    #print(loaded_dict)
    
    for x in range(0,3):
        print()
    
    #converts data to vars and back into sets
    global REACTION_MESSAGE
    loaded_dict["REACTION_MESSAGES"]=tuple(REACTION_MESSAGE)
    print("Reaction Message IDS:")
    print(REACTION_MESSAGE)
    for x in range(0,2): print()
    
    global REACTION_CHANNEL_ID
    loaded_dict["REACTION_CHANNELS"]=tuple(REACTION_CHANNEL_ID)
    print("Reaction Channel IDS:")
    print(REACTION_CHANNEL_ID)
    for x in range(0,2): print()
    
    global ROLES
    loaded_dict["ROLES"]=ROLES #may need dict(ROLES)
    print("Saved Role IDs:")
    print(ROLES)
    print()
    
    global MODHELP_TICKET_IDS
    loaded_dict["MODHELP_TICKET_IDS"]=tuple(MODHELP_TICKET_IDS)
    print("Modhelp Ticket Ids:")
    print(MODHELP_TICKET_IDS)
    for x in range(0,2): print()
    
    global TICKETS
    loaded_dict["TICKETS"]=TICKETS #may need dict(TICKETS)
    print("Modhelp Tickets:")
    print(TICKETS)
    print()
    
    # Serializing json
    print('DUMPING TO JSON....')
    json_object = json.dumps(loaded_dict, indent=4)
    
    # Writing to botjson.json
    with open("botjson.json", "w") as outfile:
        outfile.write(json_object)
    
    print('SUCCESS. DATA SAVED.')

#Future ideas:
#poll bot functionality, eventually?
#change bot description to show what server is runing