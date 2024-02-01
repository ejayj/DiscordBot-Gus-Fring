import os
import subprocess
from subprocess import Popen, PIPE, STDOUT
import psutil


print('HELLOOOOOOOOO')
servers=3 #amount of servers available
max_servers=2 #server limit
online_servers= {"TITAN"} #current running servers
command_locked=bool #if the start/stop commands are locked

def on_startup():
    #get how many servers are online; automatically changes global values
    result = check_all_servers_running() 
    
    #TODO: make this actually help me with the server's bot's 'on_ready' command. finish if not result funct if even needed?
    if not result: #if there are too many servers running or we're capped, notifies me.
        pass


def int_to_server(server_int: int): #returns name, exe, and lnk names. 
    
    if server_int not in range(1,servers+1): #check if its integer is in the appropriate range. servers+1 allows for atual range
        raise ValueError(f"Invalid value for server int. Value: {server_int} was given.")
    
    #TODO: #Change to actual files
    if server_int==1:
        program="Palworld"
        #program_exe="PalServer.exe"
        #program_exe="PalServer-Win64-Test-Cmd."
        program_lnk="TITAN.lnk"
        #program_dir=f"D:\SteamLibrary\steamapps\common\PalServer"
        program_exe="PalServer-Win64-Test-Cmd.exe"
        program_dir="D:\SteamLibrary\steamapps\common\PalServer\Pal\Binaries\Win64"
        return program,program_exe,program_dir,program_lnk
    elif server_int==2:
        program="PaperMC"
        #program_exe="ServerStarterNoGui.bat"
        #program_exe="java -jar paper.jar"
        program_exe="javaw.exe"
        program_lnk="paper.lnK"
        program_dir=f"C:\\Users\ejayj\Desktop\minecraft stuffs\minecraft server\paper server"
        #"C:\Users\ejayj\Desktop\minecraft stuffs\minecraft server\paper server"
        return program,program_exe,program_dir,program_lnk
    elif server_int==3:
        program="TITAN"
        program_exe="TITAN.exe"
        #program_lnk="TITAN.lnk"
        program_dir=f"C:\Program Files (x86)\Steam\steamapps\common\Titan Souls"
        return program,program_exe,program_dir,program_lnk
    else:
        print('Error: Wrong Int Given For Server!')
        return False

#checks if a specific server is running; 
def is_running(server: int): #can also do tasklist -f PROCESSNAME.exe
    global online_servers
    program, program_exe, program_dir,program_lnk = int_to_server(server) #will throw error if not given int or valid range

    #TODO:
    running = "" #CHANGE ME HERE!!! put as(?): f"{process}" in (i.name() for i in psutil.process_iter())
    
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
def check_all_servers_running():
    
    print('CHECKING RUNNING SERVERS.....')
    global online_servers, servers
    
    x=1
    while(x <= servers):
        is_running(x) #automatically adds running servers to online servers set
        x=x+1
    
    print(f'There are {len(online_servers)} servers running: [{online_servers}]')
    return check_servers_cap()

#check if running servers doesnt go over max servers allowed
def check_servers_cap():
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
def startserver_error_prechecks(server: int):
    
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
def stopserver_error_checks(server: int):
    
     #check if server is already running, and verifies int
    if not is_running(server):
        print('ERROR: Cannot stop server. Server already OFFLINE!')
        return False
    return False



#*****BOOK MARK CHECK POINT******* 
# TODO: finish is_running(), on_start, and below as well as the things marked 

# TODO: then, test start/stop features here for every server. then w bot. then test individually and then w multiple at same time.

#starts server
def start_server(server: int):
    
    #NOTE: once command issued, do not allow it to be spammed. rate limit a command?
    #check for any errors; also prints error message
    
    if not startserver_error_prechecks(server):
        return False 
    
    program,program_exe,program_dir,program_lnk=int_to_server(server)
    
    if server in range(2,4): #if process is a minecraft server, run lnk file, not the exe. mc servers are 2 and 3
        program_exe=program_lnk #im lazy and dont want to re-write exes as lnk
    
    #start program from lnks
    print(f"ATTEMPTING TO OPEN: {program_exe}")
    #subprocess.Popen(f"{program_lnk}") #opening the lnk
    
    #test
    # success = "" #we dont use os.system bc it doesnt allow async process os.system("TITAN.lnk" )#subprocess.Popen(f"{program_lnk}")
    # print('was it success?')
    # print(success)
    
    #or attempt this: where dir can be a var passed from int_to_server(server): program_dir
    
    if server in range(2,4): #if process is a minecraft server or lnk file (servers 2-3), run program in shell
        success=subprocess.Popen(f"{program_exe}", shell=True, stdout=PIPE, stderr=STDOUT)
        print("this is the new success message:")
        print(success.stdout)
        print("DONE")
    else: #open from deeper directory
        inkscape_dir=f"{program_dir}"
        os.path.isdir(inkscape_dir)
        os.chdir(inkscape_dir)
        success=subprocess.Popen(f"{program_exe}")
    
    #check if process was sucessful
    if 'returncode: None' in str(success): #the message on success we get is:  <Popen: returncode: None args: 'TITAN.exe'>
        success=True
    
    #how cani check for success message? check is running? or does subprocess return TRUE or success as in the console? maybe success = is_running(server) #or from subprocess
    if success:
        print(f"Successfully Started Server: [{program}]")
        #online_servers.add(program) #not needed if i get success from is_running, as it does this automatically
        return True
    elif not success:
        #if fail, pass error message to logs and let command caller know that ive been notified
        print(f"FAILED TO OPEN: {program_exe}")
        return False


#TODO:
def stop_server(server: int):
    #same thing as start server
    
    #check for any errors; also prints error message
    if stopserver_error_checks(server):
        return False
    
    program,program_exe,program_dir,program_lnk=int_to_server(server)
    
    #check if successful
    success=os.system(f"taskkill -f -im {program_exe}") #retuns 0 if successful, 128 unsuccessful

    if success==0: #the success message is: SUCCESS: The process "TITAN.exe" with PID 12784 has been terminated.
        success=True
    #how to check upon success? what if  taskkill freezes?will bot freeze? should i make it a subprocess? os.system(f"taskkill -f -im {program_exe}")
    #success = not is_running(server) #or from os.system?:
    
    #return result
    if success:
        print(f"Successfully STOPPED Server: [{program}]")
        #online_servers.remove(program) #not needed if i get success from is_running, as it does this automatically
        return True
    elif not success:
        #if fail, pass error message to logs and let command caller know that ive been notified; lock start/stop server functions
        print(f"FAILED TO SHUTDOWN SERVER: {program_exe}")
        return False


#change server runnings int
        

#functions to be used: is_running(int), int_to_server(int), and on_startup to check all servers upon start.
#methods that need finishing: on start, and is_running #server info
#test these out before placing them in discord bot (server 1 2 and 3)

#need to make a rate limit or lock upon bot issue

#this is a command to unlock the start/stop commands: founder online (or dev)
def unlock_commands():
    pass

#logic for starting allowed servers is done

#other tries
#***********************************************

start_server(2)
#stop_server(2)
#subprocess.Popen(f"paper.ex")
#os.system("paper.lnk")


# inkscape_dir=f"{program_dir}"
#     os.path.isdir(inkscape_dir)
#     os.chdir(inkscape_dir)
#     success=subprocess.Popen(f"{program_exe}")
#program_dir=f"C:\\Users\ejayj\Desktop\minecraft stuffs\minecraft server\paper server"
#subprocess.run("java -jar paper.jar")

# result=subprocess.Popen("paper.lnk", shell=True)
# print(f"result = {result}")
# print("hi i stll run!!!!")
#new command to check if all servers are running




#TODO:
#need to work on codes by taking what the input from command prompt is