#python to .jar or terminal starter
import subprocess
import os
import time
# import module 
import psutil 
  
def open_jar():
    subprocess.call(['java', '-jar', 'Blender.jar'])
    pass

def open_jar_os():
    os.system("java -jar c:\Program Files (x86)\Steam\steamapps\common\Titan Souls\TITAN.exe")

def open_new():
    os.system("TITAN.lnk")

def close():
    os.system("taskkill -f -im TITAN.exe")
    print("closing")

def is_running2(process):
    return os.system(f"tasklist") #returns entire lsit of processes
    #subprocess.call([f'tasklist'])
# open_new()
# time.sleep(1) # Sleep for 3 seconds
# 
# 
#close()

tasklist = is_running2("TITAN")

print("i did this here")
print(tasklist)

# for tasks in tasklist:
#     print(tasks)
#     print('i did this here')


print("if true:?")
# check if chrome is open 
print("TITAN.exe" in (i.name() for i in psutil.process_iter())) #returns true or false

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

    if not is_running(program):#if program is already running, don't open it
        print(f"ATTEMPTING TO OPEN: {program}")
        os.system(f"{program_lnk}")
    

