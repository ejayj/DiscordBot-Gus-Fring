import os
import subprocess
from subprocess import Popen, PIPE, STDOUT
import psutil


print('HELLOOOOOOOOO')
servers=3 #amount of servers available
max_servers=2 #server limit
online_servers= set() #current running servers
command_locked=bool #if the start/stop commands are locked

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
#need to work on codes by taking what the input from command prompt is

#*****BOOK MARK CHECK POINT******* 

#this is a command to unlock the start/stop commands: founder online (or dev)
async def unlock_commands():
    pass





# implement basic slash commands with no safety features (no command lock function or time out)
# once these basic commands work(try multiple servers at a time), and the server cap, and any possible errors-> then implement time out or command lock uponissues



#TODO: Server info, command rate limit, command lock upon issue

#implementation NOTE:
#functions to be used: is_running(int), int_to_server(int), and on_startup to check all servers upon start.


#make am essage when youve reached your server limit