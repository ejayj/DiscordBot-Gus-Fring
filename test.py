import os
import subprocess
import psutil 

def is_running(process):
    return f"{process}" in (i.name() for i in psutil.process_iter())

def open_program(program): #1 for palworld, 2 for modded mc, 3 for regular mc
    
    #based on program number, it will select that file
    if program==1:
        program_exe="TITAN.exe"
        program_lnk="TITAN.lnk"
    elif program==2:
        program_exe="TITAN.exe"
        program_lnk="TITAN.lnk"
    elif program==3:
        program_exe="TITAN.exe"
        program_lnk="TITAN.lnk"

    if not is_running(program_exe):#if program is already running, don't open it
        print(f"ATTEMPTING TO OPEN: {program_exe}")
        subprocess.Popen("TITAN.exe")
        print("Successfully opened {program}")
    
#open_program(1)

print("opening ")
#subprocess.Popen("TITAN.lnk")

#titan 
inkscape_dir=f"C:\Program Files (x86)\Steam\steamapps\common\Titan Souls"
program_name="TITAN.exe"

#palworld
inkscape_dir1=f"D:\SteamLibrary\steamapps\common\PalServer"
program_name1="PalServer.exe"

#christmas server
inkscape_dir2="C:\Users\ejayj\Desktop\minecraft stuffs\minecraft server\christmas"
program_name2="run.bat"

#paper server
inkscape_dir3="C:\Users\ejayj\Desktop\minecraft stuffs\minecraft server\paper server"
program_name3="ServerStarterNoGui.bat"

os.path.isdir(inkscape_dir)
os.chdir(inkscape_dir)
subprocess.Popen("TITAN.exe")
print("done")



#next todo:
#switch statement for the four servers
#make sure i can start/trigger and stop all the servers
#lock - only 2 servers start at once
#if you want to starta third, ask if which server you want to close (or auto close oldest open?)
#or only allow one mc server running once

#final test:
#call one function, specify an int for a server to start [maybe an additonal statement to transfer int - to server name]
#make sure not already running, make sure two servers arent already running
#cap mc servers at only one running at a time. ask if you're sure you want to stop other mc server/palworld?
#then call function that actually starts the server, and returns true and print statemnt upon success
#if error, pass exception e as to why server couldnt start
#if server start: add servers running +1, and make timer function to keep track of server uptime

#if closing server, do the same as above, but server running -1 and stop timer

#lastly, do the server info function