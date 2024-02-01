import asyncio
import os
import subprocess
from subprocess import Popen, PIPE, STDOUT
import psutil
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

servers=3 #amount of servers available
max_servers=2 #server limit
online_servers= set() #current running servers
command_locked=bool #if the start/stop commands are locked
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
    
    #run this command when first starting the bot to check on the servers
    async def on_startup():
        #get how many servers are online; automatically changes global values
        result = check_all_servers_running() 
        
        #TODO: make this actually help me with the server's bot's 'on_ready' command. finish if not result funct if even needed?
        if not result: #if there are too many servers running or we're capped, notifies me.
            #for is running, start timer as soon as we know that the servers have already been up
            #print some kind of warning message, all servers are already running!
            #start timers, 
            # and maybe do something else....?
            pass

    
    #converts int to server name and appendages
    async def int_to_server(server_int: int): #returns name, exe, and lnk names. 
        
        if server_int not in range(1,servers+1): #check if its integer is in the appropriate range. servers+1 allows for atual range
            raise ValueError(f"Invalid value for server int. Value: {server_int} was given.")
        
        if server_int==1:
            program="Palworld"
            program_lnk="TITAN.lnk"
            program_exe="PalServer-Win64-Test-Cmd.exe"
            program_dir="D:\SteamLibrary\steamapps\common\PalServer\Pal\Binaries\Win64"
            return program,program_exe,program_dir,program_lnk
        elif server_int==2:
            program="PaperMC"
            program_exe="javaw.exe"
            program_lnk="paper.lnK"
            program_dir=f"C:\\Users\ejayj\Desktop\minecraft stuffs\minecraft server\paper server"
            return program,program_exe,program_dir,program_lnk
        elif server_int==3:
            program="ModdedMC"
            program_exe="java.exe"
            program_lnk="moddedmc.lnk"
            program_dir=f"C:\\Users\ejayj\Desktop\minecraft stuffs\minecraft server\christmas"
            return program,program_exe,program_dir,program_lnk
        else:
            print('Error: Wrong Int Given For Server!')
            return False

    #checks if a specific server is running; 
    async def is_running(server: int): #can also do tasklist -f PROCESSNAME.exe
        global online_servers
        program, program_exe, program_dir,program_lnk = int_to_server(server) #will throw error if not given int or valid range

        if server in range(2,4): #if its a minecraft server:
            program=program_exe
            
        if f"{program}" in (i.name() for i in psutil.process_iter()):#replace this with the actual check if a program is running
            if program not in online_servers: #if not in online server set, add it
                online_servers.add(program)
            print(f'Server: [{program}] is currently running!')
            return True
        else:
            if program in online_servers: #remove from online server 
                online_servers.remove(program)
            print(f'Server: [{program}] is OFFLINE.')
            return False
                
    #check all servers to see if running
    async def check_all_servers_running():
        
        print('CHECKING RUNNING SERVERS.....')
        global online_servers, servers
        
        x=1
        while(x <= servers):
            is_running(x) #automatically adds running servers to online servers set
            x=x+1
        
        print(f'There are {len(online_servers)} servers running: [{online_servers}]')
        return check_servers_cap()

    #check if running servers doesnt go over max servers allowed
    async def check_servers_cap():
        global max_servers, online_servers
        running_servers=len(online_servers)
        if running_servers == max_servers:
            print(f'There are {running_servers} out of {max_servers} allowed servers running.')
            print('You\'ve reached the server running limit!')
            return False #cannot start a new server
        
        if running_servers > max_servers:
            print(f'There are {running_servers} out of {max_servers} allowed servers running.')
            print('Too many servers are running!')
            return False #too many servers running
        
        if running_servers < max_servers:
            print(f'There are {running_servers} out of {max_servers} allowed servers running.')
            print('This is O.K.')
            return True #can start servers

    #pre-check for starting server command
    async def startserver_error_prechecks(server: int):
        
        #check if server is already running, and verifies int
        if is_running(server):
            print('ERROR: Cannot start server. Server already running!')
            return False
        
        #check if server cap limit reached
        if not check_servers_cap():
            print('ERROR: Cannot start server. Server limit reached!')
            return False
        
        #if successful, and we pass all error checks
        return True

    #pre-check for stopping server command
    async def stopserver_error_checks(server: int):
        
        #check if server is already running, and verifies int
        if not is_running(server):
            print('ERROR: Cannot stop server. Server already OFFLINE!')
            return False
        return False
        
    #starts server
    async def start_server(server: int):
        
        if not startserver_error_prechecks(server):
            return False 
        
        program,program_exe,program_dir,program_lnk=int_to_server(server)
        
        #start program from lnks
        print(f"ATTEMPTING TO OPEN: {program_exe}")
        
        if server==2: #if process is a minecraft server or lnk file (servers 2-3), run program in shell; run lnk file, not the exe. mc servers are 2 and 3
            program_exe=program_lnk 
            success=subprocess.Popen(f"{program_exe}", shell=True)#, stdout=PIPE, stderr=STDOUT)
        elif server==3:
            program_exe=program_lnk
            success=subprocess.Popen("start {}".format(f"{program_exe}"), shell=True)
        else: #open from deeper directory
            inkscape_dir=f"{program_dir}"
            os.path.isdir(inkscape_dir)
            os.chdir(inkscape_dir)
            success=subprocess.Popen(f"{program_exe}")
        
        #check if process was sucessful
        if 'returncode: None' in str(success):
            success=True
        if success:
            print(f"Successfully Started Server: [{program}]")
            return True
        elif not success:
            print(f"FAILED TO OPEN: {program_exe}")
            return False

    #stop server function
    async def stop_server(server: int):
        #same thing as start server
        
        #check for any errors; also prints error message
        if stopserver_error_checks(server):
            return False
        
        program,program_exe,program_dir,program_lnk=int_to_server(server)
        
        #check if successful
        success=os.system(f"taskkill -f -im {program_exe}") #retuns 0 if successful, 128 unsuccessful

        if success==0: #the success message is: SUCCESS: The process "TITAN.exe" with PID 12784 has been terminated.
            success=True
        
        #return result
        if success:
            print(f"Successfully STOPPED Server: [{program}]")
            #online_servers.remove(program) #not needed if i get success from is_running, as it does this automatically
            return True
        elif not success:
            #if fail, pass error message to logs and let command caller know that ive been notified; lock start/stop server functions
            print(f"FAILED TO SHUTDOWN SERVER: {program_exe}")
            return False

    #returns if server is running, and uptime; and maybe other info like version info and etc.
    async def server_info(server: int):
        running=is_running(server)
        uptime="" #eventually, a server_time(server: int) function
        return running, uptime

    #TODO:
    #this is a command to unlock the start/stop commands: founder online (or dev)
    async def unlock_commands():
        pass

    #TODO: NEXT
    # implemenet these server commands with the front end bot, see below's note for more info
    
    #NOTE: remmeber, input for start server is INT. In the discord command itself, i will need to convert text ot int. maybe ill use a menu
    #Functions that will be called explicitly:
    # server info, int_to_server(int), and start/stop serrver, and on_startup to check all servers upon start.
    
    
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
                Channel = interaction.channel
                await Channel.send(f'Server starting success!')
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
            print(f"Attempting to stop Server: [{server}]")
            
            success = await stop_server(server)
            if success:
                print(f"Server sucessfully stopped!")
                Channel = interaction.channel
                await Channel.send(f'Server stopped!')
                #send response?
                
            Channel = interaction.channel
            await Channel.send(f'Server stopped successfully!')
            print("server stopped!")
            
            
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