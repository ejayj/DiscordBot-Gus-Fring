import asyncio
import os
import random
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
from typing import Optional

#reaction roles reacts to rules channel id and message
#lock commands to founder: sync, synctoguild, add role auth, add channel auth, create rules reaction
#lock to staff: create reaction messages
#lock commands to server starter: start server, stop server [make server starter role; to request role use modmail]

#TODO: UTILIZING BOT [ON LAUNCH]
#Announce server start roles; input the ids into the json;


#NOTE: For hiding dev commands, go to integrations, specific command, and hide from everyone. COMMANDS TO BE HIDDEN:
#Sync, Sync to guild, and server starter commands


 #add server timer to server starter or just save server time starter
#NEXT TODO:
    #create server start time timer, finish mod mail
    
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
MEMBER_RANK_NAME = "Member" #this is only var not in json!. EDIT ME!
MOD_CHANNEL = 1075832483557408902 #Mod channel ID for comms with mods
SERVER_STARTER_ROLE="ServerStarter" #Role for server starter ping - upon request server start
SERVER_STARTER_CHANNEL= 1075832483876180088 #channel for server starters #currently this channel is set to #trusted
GUILD_ID = 1075832482110373949 #paste id of guild here


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
        await on_startup()
        print(f'{client.user} is now running!')
        
    #*************
    #DEV COMMANDS
    #************
    
    @client.tree.command()
    async def sync(interaction: discord.Integration):
        """Sync commands!"""
        #command lock
        allowed = True#await lock_command(interaction.user, "Admin")
        if not allowed:
            await interaction.response.send_message(f"Command not allowed!", ephemeral=True) 
            return
        
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)!")
        await interaction.response.send_message(f"Synced {len(synced)} command(s)!", ephemeral=True)
    
    @sync.error
    async def sync(interaction: discord.Integration, error):
        await interaction.response.send_message(f"An Error has occured!: {error}", ephemeral=True)
            
    @client.tree.command()
    #@commands.has_permissions(administrator=True) #doesnt work
    async def syncguild(interaction: discord.Integration):
        """Sync commands to this guild only!"""
        #command lock
        # allowed = await lock_command(interaction.user, "Red") #this can be doen by discord integrations
        # if not allowed:
        #     await interaction.response.send_message(f"Command not allowed!", ephemeral=True) 
        #     return
        client.tree.copy_global_to(guild =discord.Object(id = GUILD_ID))
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s) to dev guild!")
        await interaction.response.send_message(f"Synced {len(synced)} command(s) to dev guild!", ephemeral=True)
    
    @syncguild.error
    async def syncguild(interaction: discord.Integration, error):
        await interaction.response.send_message(f"An Error has occured!: {error}", ephemeral=True)
    
    #add a role to authorized server starterss   
    @client.tree.command()
    @app_commands.describe(role="Mention a role here")
    async def add_role_auth(interaction: discord.Integration, role: discord.Role):
        """Add a role to authorized server starters"""
        await interaction.response.send_message(f"Added {role} to authorized roles!", ephemeral=True)
        
        global ROLES
        newrole={"Name": f"{role}", "ID": role.id}
        ROLES.append(newrole)
        await save_to_json() #save to json
        print(f'{interaction.user} Added new role: ({role}) to authorized users!')
    
    @add_role_auth.error
    async def add_role_auth(interaction: discord.Integration, error):
        await interaction.response.send_message(f"An Error has occured!: {error}", ephemeral=True)
    
    #add a reaction channel to json; may want to have names with channel ids
    @client.tree.command()
    @app_commands.describe(channel="Insert Channel ID Here!")
    async def add_reaction_channel(interaction: discord.Integration, channel: str):
        """Add a role to authorized server starters"""
        await interaction.response.send_message(f"Added {channel} to reaction channels!", ephemeral=True)
        
        REACTION_CHANNEL_ID.add(channel)
        await save_to_json()
        print('saved new channel id!')
    
    @add_reaction_channel.error
    async def add_reaction_channel(interaction: discord.Integration, error):
        await interaction.response.send_message(f"An Error has occured!: {error}", ephemeral=True)
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
    async def check_role_priv(user): #level 1 is regular member, level 2 is mod, level 3 is server role
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
        result = await check_all_servers_running() 
        
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
            program_lnk="paper.lnk"
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
        program, program_exe, program_dir,program_lnk = await int_to_server(server) #will throw error if not given int or valid range
            
        if f"{program_exe}" in (i.name() for i in psutil.process_iter()):#replace this with the actual check if a program is running
            if program not in online_servers: #if not in online server set, add it
                online_servers.add(program)
                await client.change_presence(activity=discord.Game(name=f"{program}"))
            print(f'Server: [{program}] is currently running!')
            return True
        else:
            if program in online_servers: #remove from online server 
                online_servers.remove(program)
                await client.change_presence(activity=None)
            print(f'Server: [{program}] is OFFLINE.')
            return False
                
    #check all servers to see if running
    async def check_all_servers_running():
        
        print('CHECKING RUNNING SERVERS.....')
        global online_servers, servers
        
        x=1
        while(x <= servers):
            await is_running(x) #automatically adds running servers to online servers set
            x=x+1
        
        print(f'There are {len(online_servers)} servers running: [{online_servers}]')
        return await check_servers_cap()

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
        if await is_running(server):
            print('ERROR: Cannot start server. Server already running!')
            return False
        
        #check if server cap limit reached
        if not await check_servers_cap():
            print('ERROR: Cannot start server. Server limit reached!')
            return False
        
        #if successful, and we pass all error checks
        return True

    #pre-check for stopping server command
    async def stopserver_error_checks(server: int):
        
        #check if server is already running, and verifies int
        if not await is_running(server):
            print('ERROR: Cannot stop server. Server already OFFLINE!')
            return False
        return False
        
    #starts server
    async def start_server(server: int):
        
        if not await startserver_error_prechecks(server):
            return False 
        
        program,program_exe,program_dir,program_lnk= await int_to_server(server)
        
        #start program from lnks
        print(f"ATTEMPTING TO OPEN: {program_exe}")
        
        if server in range(2,4): #if process is a minecraft server or lnk file (servers 2-3), run program in shell; run lnk file, not the exe. mc servers are 2 and 3
            program_exe=program_lnk
            success=subprocess.Popen("start {}".format(f"{program_exe}"), shell=True)
        else: #open from deeper directory
            inkscape_dir=f"{program_dir}"
            os.path.isdir(inkscape_dir)
            os.chdir(inkscape_dir)
            success=subprocess.Popen("start {}".format(f"{program_exe}"), shell=True)#subprocess.Popen(f"{program_exe}", shell=True)
        
        #check if process was sucessful
        if 'returncode: None' in str(success):
            success=True
        if success:
            print(f"Successfully Started Server: [{program}]")
            online_servers.add(program)
            await check_all_servers_running()
            await client.change_presence(activity=discord.Game(name=f"{program}"))
            return True
        elif not success:
            print(f"FAILED TO OPEN: {program_exe}")
            await client.change_presence(activity=None)
            return False

    #stop server function
    async def stop_server(server: int):
        #same thing as start server
        
        #check for any errors; also prints error message
        if await stopserver_error_checks(server):
            return False
        
        program,program_exe,program_dir,program_lnk= await int_to_server(server)
        
        #check if successful
        success=os.system(f"taskkill -f -im {program_exe}") #retuns 0 if successful, 128 unsuccessful

        if success==0: #the success message is: SUCCESS: The process "TITAN.exe" with PID 12784 has been terminated.
            success=True
        
        #return result
        if success:
            print(f"Successfully STOPPED Server: [{program}]")
            online_servers.remove(program)
            #online_servers.remove(program) #not needed if i get success from is_running, as it does this automatically
            await check_all_servers_running()
            await client.change_presence(activity=None)
            return True
        elif not success:
            #if fail, pass error message to logs and let command caller know that ive been notified; lock start/stop server functions
            print(f"FAILED TO SHUTDOWN SERVER: {program_exe}")
            return False

    #returns if server is running, and uptime; and maybe other info like version info and etc.
    async def server_info(server: int):
        running= await is_running(server)
        program,program_exe,program_dir,program_lnk=int_to_server(server)
        uptime=None #eventually, a server_time(server: int) function
        
        if running:
            return f"Server [{program}] is running. Uptime: {uptime}"
        else:
            return f"Server [{program}] is not running."

    #TODO:
    #this is a command to unlock the start/stop commands: founder online (or dev)
    async def unlock_commands():
        pass

    #TODO: NEXT
    # implemenet these server commands with the front end bot, see below's note for more info
    
    #NOTE: remmeber, input for start server is INT. In the discord command itself, i will need to convert text ot int. maybe ill use a menu
    
    #Functions that will be called explicitly:
    # server info, int_to_server(int), and start/stop serrver, and on_startup to check all servers upon start.
    
    #TODO:things i want to do eventually
        #need to work on codes by taking what the input from command prompt is
    
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
    
    #role lock these commands
    @client.tree.command()
    @app_commands.describe(server="Input Integer: 1=Palworld, 2=VanillaMC, or 3=ModdedMC")
    async def startserver(interaction: discord.Integration, server: int):
        """Start a server"""
        global servers
        priv = await check_role_priv(interaction.user)
        program,program_exe,program_dir,program_lnk=await int_to_server(server)
        if priv:
            #str_check = await check_server_name(server)
            if server not in range(1,servers+1):#str_check: #check if server name passed is valid
                await interaction.response.send_message(f"Invalid Server Name, try again!", ephemeral=True)
                return
            await interaction.response.send_message(f"Server: {program} Starting...")
            print(f"Attempting to start server: [{program}]")
            success = await start_server(server)
            
            if success:
                print(f"Server starting success!")
                Channel = interaction.channel
                await Channel.send(f'Server starting success!')
                #send response?
            else:
                print(f"ERROR: Failed to start server!")
                Channel = interaction.channel
                await Channel.send(f'Server failed to start! Please use /requeststartserver. Do not run this command again!')
                #send response?
                
        else:
            await interaction.response.send_message(f"Sorry, you can't run that command!", ephemeral=True)
            print(f'User {interaction.user} tried to use "/startserver"!')
        #message: too many servers started! use /requeststart server
    
    @startserver.error
    async def startserver(interaction: discord.Integration, error):
        await interaction.response.send_message(f"An Error has occured!: {error}", ephemeral=True)
            
    #role lock these commands
    @client.tree.command()    
    @app_commands.describe(server="Input Integer: 1=Palworld, 2=VanillaMC, or 3=ModdedMC")
    async def stopserver(interaction: discord.Integration, server: int):
        """Stop a server"""
        global servers
        priv = await check_role_priv(interaction.user)
        program,program_exe,program_dir,program_lnk=await int_to_server(server)
        if priv:
            #str_check = await check_server_name(server)
            if server not in range(1,servers+1):#str_check: #check if server name passed is valid
                await interaction.response.send_message(f"Invalid Server Name, try again!", ephemeral=True)
                return
            await interaction.response.send_message(f"Server: {program} stopping...")
            print(f"Attempting to stop Server: [{program}]")
            
            success = await stop_server(server)
            if success:
                print(f"Server sucessfully stopped!")
                Channel = interaction.channel
                await Channel.send(f'Server stopped!')
                #send response?
                
                # Channel = interaction.channel
                # await Channel.send(f'Server stopped successfully!')
                # print("server stopped!")
            else:
                print(f"ERROR: Failed to stop server!")
                Channel = interaction.channel
                await Channel.send(f'Server failed to stop! Please message @Modmail about this for help. Do not run this command again!')
                #send response?
        else:
            await interaction.response.send_message(f"Sorry, you can't run that command!", ephemeral=True)
            print(f'User {interaction.user} tried to use "/stopserver"!')
        #message: too many servers started! use /requeststart server
        
        @stopserver.error
        async def stopserver(interaction: discord.Integration, error):
            await interaction.response.send_message(f"An Error has occured!: {error}", ephemeral=True)
    
    @client.tree.command()
    async def serverinfo(interaction: discord.Integration):
        """Request info on all servers!"""
        #check passed server name
        # namecheck=await check_server_name(server)
        
        serverinfo=""
        
        #check server 1: palworld
        server = await is_running(1)
        if not server:
            serverinfo=serverinfo+f"\n Server [Palworld] is OFFLINE."
        else:
            serverinfo=serverinfo+f"\n Server [Palworld] is ONLINE! IP: 71.169.9.2:8211"
            
        #check server 2: VanillaMC
        server = await is_running(2)
        if not server:
            serverinfo=serverinfo+f"\n Server [Paper Minecraft v1.20.1] is OFFLINE."
        else:
            serverinfo=serverinfo+f"\n Server [Paper Minecraft v1.20.1] is ONLINE! IP: 71.169.9.2"
            
        #check server 3: ModdedMC
        server = await is_running(3)
        if not server:
            serverinfo=serverinfo+f"\n Server [Forge Minecraft v1.20.1] is OFFLINE."
        else:
            serverinfo=serverinfo+f"\n Server [Forge Minecraft v1.20.1] is ONLINE! IP: 71.169.9.2:19132"
            
            
        await interaction.response.send_message(f"Server info: {serverinfo}")
    
    @serverinfo.error
    async def serverinfo(interaction: discord.Integration, error):
        await interaction.response.send_message(f"An Error has occured!: {error}")

    @client.tree.command()
    @app_commands.describe(server="Palworld, ModdedMC, or VanillaMC")
    async def requeststartserver(interaction: discord.Integration, server: str):
        """Request a server to be started!"""
        global MOD_CHANNEL, SERVER_STARTER_ROLE, GUILD_ID
        if server in "Palworld, ModdedMC, or VanillaMC":
            print(f"User {interaction.user} requested server: [{server}] to be started.")
            await interaction.response.send_message(f"Sent request for {server} to be started!",ephemeral=True)
            
            #send message to server starters in trusted channel
            guild = client.get_guild(GUILD_ID)
            role = get(guild.roles, name = SERVER_STARTER_ROLE)
                
            channel = client.get_channel(SERVER_STARTER_CHANNEL)
            await channel.send(f"User [{interaction.user}] has requested for server [{server}] to be started. {role.mention}")#send request
            return
        else:
            await interaction.response.send_message(f"Invalid Server Name, try again!", ephemeral=True)
            return


    
    @requeststartserver.error
    async def requeststartserver(interaction: discord.Integration, error):
        await interaction.response.send_message(f"An Error has occured!: {error}", ephemeral=True)
    
    @client.tree.command()   
    async def modhelp(interaction: discord.Integration):
        """Request help from a mod!"""

        user=interaction.user
        await user.send('Hai!')
        await user.send('Hello! This is private chat for modhelp! Message @ModMail until this gets off the ground :)')
        await interaction.response.send_message(f"Check your DMs!", ephemeral=True)
    
    @modhelp.error
    async def modhelp_error(interaction: discord.Integration, error):
        await interaction.response.send_message(f"An Error has occured!: {error}", ephemeral=True)

    #**********************************************************************************
    #MEME/OTHER COMMANDS 
    #**********************************************************************************
    
    #memer command: y r u gay
    @client.tree.command()
    #@commands.has_any_role("Red")#this command restriction doesnt work
    async def rugay(interaction: discord.Integration):
        """Y R U Gey?"""
        #allowed = await lock_command(interaction.user,"Red")
        #print(allowed)
        await interaction.response.send_message(f"Y r u gey {interaction.user}?!")

    @rugay.error
    async def rugay_error(interaction: discord.Integration, error):
        await interaction.response.send_message(f"An Error has occured!: {error}", ephemeral=True)
    #i could add these commands but if i cant hide commands yet then i'd rather do these manually
    #TBD
    
    #memer command: y r u gay
    @client.tree.command()
    async def roll(interaction: discord.Integration):
        """Roll the dice!"""
        roll = random.randint(1,6)
        await interaction.response.send_message(f"You rolled a {roll}!", ephemeral=True)
        
    @client.tree.command()
    @app_commands.describe(message="Type your message here!")
    async def say(interaction: discord.Integration, message: str):
        """Have me say somthing to the server!"""
        #allowed = await lock_command(interaction.user,"Red")
        #print(allowed)
        await interaction.response.send_message(f"{message}")

    @say.error
    async def say(interaction: discord.Integration, error):
        await interaction.response.send_message(f"An Error has occured!: {error}", ephemeral=True)
    
    @client.tree.command()
    @app_commands.describe(command="Enter a command here")
    async def help(interaction: discord.Integration, command: Optional[str]):
        """Get a list of available commands"""
        if command:
            if command=="rugay":
                await interaction.response.send_message(f"/rugay - I bet you wanna know what this command does😏", ephemeral=True)
            elif command=="roll":
                await interaction.response.send_message(f"/roll - returns a random number, 1 to 6, just like a dice!", ephemeral=True)
            elif command=="serverinfo":
                await interaction.response.send_message(f"/serverinfo - returns a list of the servers and their ips, and if they're offline.", ephemeral=True)
            elif command=="requeststartserver":
                await interaction.response.send_message(f"/requeststartserver [Server] - Sends a request to any available server manager to start a server. (Usage Example: /requeststartserver Palworld)", ephemeral=True)
            elif command=="modhelp":
                await interaction.response.send_message(f"/modhelp - Starts a modhelp ticket in your DMs to request help. Also use this for any inquiries or concerns!", ephemeral=True)
            elif command=="help":
                await interaction.response.send_message(f"Hahaaaa you're silly. Type /help [command] for information on a specific command. (Example: /help roll)", ephemeral=True)
            elif command=="startserver":
                await interaction.response.send_message(f"/startserver [server] - This starts a server of your choice. There can only be 2 servers running at a time! Stop a server not in use at your leisure with /stopserver. Type 1 for Palworld, 2 for  Minecraft, and 3 for Modded Minecraft. (Example: /startserver 1)\n \n If this command returns an error, please message @ejayj and do not run the command again!", ephemeral=True)
            elif command=="stopserver":
                await interaction.response.send_message(f"/stopserver [server] - This stops a server of your choice. Feel free to use this command when  a server is not in use. Type 1 for Palworld, 2 for  Minecraft, and 3 for Modded Minecraft. (Example: /startserver 1)\n \n If this command returns an error, please message @ejayj and do not run the command again!", ephemeral=True)
        else:
            help_message="`Gus Fring Commands: \n \n Main:\n /roll - Roll the dice for a random number!\n /rugay - It's time to find out the truth.\n /serverinfo - Displays server ips and online status.\n /requeststartserver - Request for a server to be started.\n /modhelp - Sends a help request to the mod team.\n /help - Displays this message. Also type /help [command] for more.\n \n Server Managers Only:\n /startserver - Start any server.\n /stopserver - Stop any server.\n \n For more help on a command, type /help [command]`\n"
            await interaction.response.send_message(f"{help_message}", ephemeral=True)

    @help.error
    async def help(interaction: discord.Integration, error):
        await interaction.response.send_message(f"An Error has occured!: {error}", ephemeral=True)
            
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
        await save_to_json()
        
    #A Command to create a rules reaction-> lock this command to admins.
    @client.tree.command()
    @app_commands.describe(message_input="Enter Message Here", emoji="Enter Standard Emoji Here")
    async def create_rules_reaction(interaction: discord.Integration, message_input: str, emoji: str):
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
        
        global RULES,REACTION_MESSAGE,REACTION_CHANNEL_ID
        #add reactions to json saveto trigger and event
        REACTION_MESSAGE.add(message.id)
        REACTION_CHANNEL_ID.add(Channel.id)
        RULES=message.id
        await save_to_json()
        
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
            if payload.message_id==RULES: #the rules message #1201416646699528232
                await remove_role(member) #takes away member role
                return
            else:
                print('this reaction could trigger something')
        
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