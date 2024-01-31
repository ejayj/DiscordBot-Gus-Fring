import os
import subprocess


print('HELLOOOOOOOOO')
max_servers=2 #server limit
online_servers=[] #current running servers

def on_startup():
    #get how many servers are online
    #code here
    
    global online_servers
    online_servers=""#however many servers there are
    
    #if more than 2 servers online, and max servers is 2,
    #stop one server [probably modded mc]
    #send notification to servers channel
    #notify founder

def int_to_server(server_int):
    if server_int==1:
        program_exe="TITAN.exe"
        program_lnk="TITAN.lnk"
        return program_exe,program_lnk
    elif server_int==2:
        program_exe="TITAN.exe"
        program_lnk="TITAN.lnk"
        return program_exe,program_lnk
    elif server_int==3:
        program_exe="TITAN.exe"
        program_lnk="TITAN.lnk"
        return program_exe,program_lnk
    else:
        print('Error: Wrong Int Given For Server!')
        return False

def is_running(server: int): #checks if a server is running; will throw error if not given int
    #server number to name method
    return

def check_all_servers_running():
    #checks what servers are running
    global online_servers
    running_servers=len(online_servers)
    if is_running(1):
        return
    return
def check_servers():
    global max_servers, online_servers
    running_servers=len(online_servers)
    if running_servers == max_servers:
        print(f'There are {running_servers} out of {max_servers} running.')
        print('You\'ve reached the server runnign limit!')
        return False #cannot start a new server
    
    if running_servers > max_servers:
        print(f'There are {running_servers} out of {max_servers} running.')
        print('Too many servers are running!')
        return False #too many servers running
    
    if running_servers < max_servers:
        print(f'There are {running_servers} out of {max_servers} running.')
        print('This is O.K.')
        return True #can start servers
        
print(int_to_server(1))