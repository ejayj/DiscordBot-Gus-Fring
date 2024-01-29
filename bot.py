import asyncio
import discord
import responses
from discord import SelectOption, app_commands
from discord.ext import commands
from discord.utils import get
from discord.ui import Select, View
import json
from pathlib import Path



#TODO: UTILIZING BOT [ON LAUNCH]
#Announce server start roles; input the ids into the json;
#Connect rules channel id and rules message id in json
#Lock commands in integrations: Sync, Synctoguild
#next, i want to make a role: server starter. People can start/stop servers with this role, and people will know. . Starr and Server Starter can do this

#NOTE: For hiding dev commands, go to integrations, specific command, and hide from everyone. COMMANDS TO BE HIDDEN:
#Sync, Sync to guild, and server starter commands


#NEXT TODO:
    
    #C. Begin working on server-functions; runtime will count by itself via bot and from /startserver function -> add ping info?
    #Cb. Eventually, transfer over to PC so we can test the file opening functions
    
    #D. Create Help Commands!
    
    #E. Fix permission of chicken bot - it may need to have certain perms to add roles (or be above it in heirarchy)  
    #make sure all server commands are finishedgo down the line)
    
    #F. Send out chicken bto for official production and put it on my resume!
    
    #Eventualities:
    #Mod mail capabilities
    #add polls eventually
    
#******************************************************************************
#Variables
#******************************************************************************

REACTION_CHANNEL_ID = set() #set of reaction channel ids
REACTION_MESSAGE = set() #set of reaction message ids
MODHELP_TICKET_IDS = set() #a set of ticket ids
TICKETS = dict #blank dict of current tickets and their info
ROLES = dict # a blank dict of role ids  we want to have saved
RULES = "" #a blank var for the message id of the rules
MEMBER_RANK_NAME = "Mature Member" #this is only var not in json!. EDIT ME!

#******************************************************************************

#Starts up bot config
class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
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
        
    #*************
    #DEV COMMANDS
    #************
    
    @client.tree.command()
    async def sync(interaction: discord.Integration):
        """Sync commands!"""
        #command lock
        allowed = await lock_command(interaction.user, "Admin")
        if not allowed:
            await interaction.response.send_message(f"Command not allowed!", ephemeral=True) 
            return
        
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)!")
        await interaction.response.send_message(f"Synced {len(synced)} command(s)!", ephemeral=True)
        
    @client.tree.command()
    #@commands.has_permissions(administrator=True) #doesnt work
    async def syncguild(interaction: discord.Integration):
        """Sync commands to this guild only!"""
        #command lock
        allowed = await lock_command(interaction.user, "Admin")
        if not allowed:
            await interaction.response.send_message(f"Command not allowed!", ephemeral=True) 
            return
        client.tree.copy_global_to(guild =discord.Object(id = 1075832475223330936))
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s) to dev guild!")
        await interaction.response.send_message(f"Synced {len(synced)} command(s) to dev guild!", ephemeral=True)
    
    #*******************
    
    # #add a role to authorized server starterss   
    # @client.tree.command()
    # @app_commands.describe(role="Mention a role here")
    # async def add_role_auth(interaction: discord.Integration, role: discord.Role):
    #     """Add a role to authorized server starters"""
    #     await interaction.response.send_message(f"Added {role} to authorized roles!", ephemeral=True)
        
    #     global ROLES
    #     newrole={"Name": f"{role}", "ID": role.id}
    #     ROLES.append(newrole)
    #     save_to_json() #save to json
    #     print(f'{interaction.user} Added new role: ({role}) to authorized users!')
    
    # #add a reaction channel to json; may want to have names with channel ids
    # @client.tree.command()
    # @app_commands.describe(channel="Insert Channel ID Here!")
    # async def add_reaction_channel(interaction: discord.Integration, channel: str):
    #     """Add a role to authorized server starters"""
    #     await interaction.response.send_message(f"Added {channel} to reaction channels!", ephemeral=True)
        
    #     #REACTION_CHANNEL_ID.add(channel)
    #     #save_to_json
    #     #print('saved new channel id!)
        
    # #add_reaction_message
        
    #****************
    #SUPPORT COMMANDS
    #*****************

    #adds role from member, defaults to Member rank if unspecified
    async def add_role(member,role=MEMBER_RANK_NAME): #we could add name=role variable.
        role = get(member.guild.roles, name=role)
        await member.add_roles(role)
        print(f'added {role} to {member}!')

    #removes role from member, defaults to Member rank if unspecified
    async def remove_role(member, role=MEMBER_RANK_NAME):
        #member = interaction.user
        role = get(member.guild.roles, name=role)
        await member.remove_roles(role)  
        print(f'removed {role} from {member}.')
    
    #checks if a member has appropriate rank (in roles json)  
    async def check_role_priv(user):
        global ROLES #i need to iterate through this some how
        for role in ROLES:
            if role["ID"] in [roles.id for roles in user.roles]:
                print(f'{user} has appropaite role!')
                return True
        else:
            print(f'{user} does not have appropriate role')
            return False
    
    #custom command priv lock
    async def lock_command(user,role=MEMBER_RANK_NAME):
        role = get(user.guild.roles, name=role)
        if role in [roles.id for roles in user.roles]:
            print(f'{user} has the necessary privileges ({role})!')
            return True
        else:
            print(f'{user} does not have appropriate privileges ({role})')
            return False
    
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
    
    
    #************************
    #SERVER STARTING FUNCTIONS
    #***********************
    
    #check if server name is valid
    async def check_server_name(server):
        if server=="Palworld":
            return True
        elif server=="ModdedMC":
            return True
        elif server=="VanillaMC":
            await True
        else:
            False
     
            
    #official func to start/stop servers
    async def start_server(server):
        if server=="Palworld":
            #function to start server 1
            pass
        elif server=="ModdedMC":
            #function to start server 2
            pass
        elif server=="VanillaMC":
            #function to start server 3
            pass
        else:
            print('Invalid server name!')
            return False
    
    #start palworld function
    async def start_palworld():
        pass
        #upon success, start timer for server uptime. global function for this
    
    #start moddedmc function
    async def start_moddedmc():
        pass
    
    #start vanilla mc function
    async def start_vanillamc():
        pass
    
    async def return_server_info(server):
        if server=="Palworld":
            #get Uptime timer
            #return if it is started or not [do global variables for these]
            #ping, if possible
            pass
        elif server=="ModdedMC":
            #function to start server 2
            pass
        elif server=="VanillaMC":
            #function to start server 3
            pass
        else:
            print('Invalid server name!')
            return False
        pass
    
    
    
    
    
    
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
    
    #eventually turn these into lists?
    @client.tree.command()
    @app_commands.describe(server="Palworld, ModdedMC, or VanillaMC")
    async def startserver(interaction: discord.Integration, server: str):
        """Start a server"""
        priv = await check_role_priv(interaction.user)
        if priv:
            str_check = await check_server_name(server)
            if not str_check: #check if server name passed is valid
                await interaction.response.send_message(f"Invalid Server Name, try again!", ephemeral=True)
                return
            await interaction.response.send_message(f"Server: {server} Starting...")
            print(f"Attempting to start server: [{server}]")
            success = await start_server(server)
            if success:
                print(f"Server starting success!")
                #send response?
        else:
            await interaction.response.send_message(f"Sorry, you can't run that command!", ephemeral=True)
            print(f'User {interaction.user} tried to use "/startserver"!')
        #message: too many servers started! use /requeststart server
    
    @client.tree.command()    
    @app_commands.describe(server="Palworld, ModdedMC, or VanillaMC")
    async def stopserver(interaction: discord.Integration, server: str):
        """Stop a server"""
        priv = await check_role_priv(interaction.user)
        if priv:
            str_check = await check_server_name(server)
            if not str_check: #check if server name passed is valid
                await interaction.response.send_message(f"Invalid Server Name, try again!", ephemeral=True)
                return
            await interaction.response.send_message(f"Server: {server} stopping...")
            print(f"Attempting to start Server: [{server}]")
        else:
            await interaction.response.send_message(f"Sorry, you can't run that command!", ephemeral=True)
            print(f'User {interaction.user} tried to use "/stopserver"!')
        #message: too many servers started! use /requeststart server
    
    @client.tree.command()
    @app_commands.describe(server="Palworld, ModdedMC, or VanillaMC")
    async def serverinfo(interaction: discord.Integration, server: str):
        """Request info on a server!"""
        #check passed server name
        namecheck=await check_server_name(server)
        if not namecheck:
            await interaction.response.send_message(f"Invalid server name! Try again!", ephemeral=True)
            return        
        print(f"User {interaction.user} requested info on: [{server}]")
        
        #actual request for server info
        serverinfo=await return_server_info(server)
        
        #return server info
        await interaction.response.send_message(f"Server info: {serverinfo}", ephemeral=True)

    #@client.tree.command()
    @app_commands.describe(server="Palworld, ModdedMC, or VanillaMC")
    async def requeststartserver(interaction: discord.Integration, server: str):
        """Request a server to be started!"""
        if server=="Palworld":
            await interaction.response.send_message(f"Sent request for {server} to be started!",ephemeral=True)
        elif server=="ModdedMC":
            await interaction.response.send_message(f"Sent request for {server} to be started!",ephemeral=True)
        elif server=="VanillaMC":
            await interaction.response.send_message(f"Sent request for {server} to be started!",ephemeral=True)
        else:
            await interaction.response.send_message(f"Invalid Server Name, try again!", ephemeral=True)
            return
        
        print(f"User {interaction.user} requested server: [{server}] to be started")
    
    @client.tree.command()   
    async def modhelp(interaction: discord.Integration):
        """Request help from a mod!"""
        user=interaction.user
        await user.send('Hai!')
        await user.send('Hello! This is private chat for modhelp!')
        await interaction.response.send_message(f"Check your DMs!", ephemeral=True)
        
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
    async def on_raw_reaction_add(payload):
        print(payload)
        global REACTION_CHANNEL_ID, REACTION_MESSAGE,guild
        reaction_emoji=payload.emoji #the reacted emoji
        #user=await client.fetch_user(reaction.member) #the user who reacted
        user=payload.member
        channel = client.get_channel(payload.channel_id) #channel name
        print(f'User {user} added reaction {reaction_emoji} in channel {channel}')
        
        if await check_reaction(payload,user):
            #depending on what message id, it will trigger different events
            if payload.message_id==RULES: #the rules message
                await add_role(user) #gives member role
                return
            else:
                print('this reaction could trigger something')
        #i could also write a switch statement here. If reaction = a certain emoji, execute this particular function e.g. give role
        
    #***************
    #DETECT REMOVE REACTIONS
    #***************
    @client.event
    async def on_raw_reaction_remove(payload):
        global REACTION_CHANNEL_ID, REACTION_MESSAGE
        reaction_emoji=payload.emoji #or reaction.emoji
        user=await client.fetch_user(payload.user_id) #i can also see channel_id and message_id
        #user=payload.member
        #print(payload)
        channel = client.get_channel(payload.channel_id) #channel name
        
        print(f'User {user} removed reaction {reaction_emoji} in channel {channel}')
    
        guild = client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        
        #print(member)
        if await check_reaction(payload,user):
            #depending on what message id, it will trigger different events
            if payload.message_id==RULES: #the rules message
                await remove_role(member) #takes away member role
                return
            else:
                print('this reaction could trigger something')
    
    #**********************************************************************************
    #MEME COMMANDS 
    #**********************************************************************************
    
    #memer command: y r u gay
    @client.tree.command()
    #@commands.has_any_role("Red")#this command restriction doesnt work
    async def rugay(interaction: discord.Integration):
        """Y R U Gey?"""
        allowed = await lock_command(interaction.user,"Red")
        print(allowed)
        await interaction.response.send_message(f"Y r u gey {interaction.user}?!")

    #error command:? look at later
    @rugay.error
    async def rugay_error(interaction: discord.Integration, error):
        await interaction.response.send_message(f"Not allowed!", ephemeral=True)
    #i could add these commands but if i cant hide commands yet then i'd rather do these manually
    #TBD
    
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
        
    #******************************************************            
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
    "ROLES": [{"Name": "Test",
        "ID": 0}],
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
    print("Role IDs:")
    print(ROLES)
    print()
    
    global RULES
    RULES=loaded_dict["RULES"]
    print("Rules Message ID:")
    print(RULES)
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
    
    global RULES
    loaded_dict["RULES"]=RULES #may need dict(ROLES)
    print("Saved Rules Message IDs:")
    print(RULES)
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
#change bot description to show what server is runing
#also i know how to hide commands: mee6 does it automatically in the integrations terminal of discord server settings. The question is: how?