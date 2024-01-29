#python to .jar or terminal starter
import subprocess


def open_jar():
    subprocess.call(['java', '-jar', 'Blender.jar'])
    pass


#i can also try 
#import os
#os.system("java -jar FULL_PATH\RR.jar")
#