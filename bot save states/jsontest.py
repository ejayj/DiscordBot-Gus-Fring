import json
from pathlib import Path


REACTION_CHANNEL_ID = set() #set of reaction channel ids
REACTION_MESSAGE = set() #set of reaction message ids
MODHELP_TICKET_IDS = set() #a set of ticket ids
TICKETS = dict #blank dict of current tickets and their info
ROLES = dict #blank dict of role ids #{ "role name" : "id"}
RULES = "" #blank int of the rules ID
#step 1: construct json is it doesnt exist
#step 2: load json data into variables if it does exits
#step 3: create generic method for json data to be saved
def create_json_if_dne():
    my_file = Path("./botjson.json")
    if my_file.exists():
        print('File "botjson.json exits.')
        load_json_data()
        return True
    
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

def load_json_data():
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

def generic_save_to_json():
    #load dict data
    print('Loading JSON DATA')
    with open("botjson.json", "r") as infile:
        loaded_dict= json.load(infile)
        
    #add data
    #just for education
    print('original data:')
    global MODHELP_TICKET_IDS
    print(MODHELP_TICKET_IDS)
    
    #here, the data would already have been added at this point
    #MODHELP_TICKET_IDS.add(132376287)

    #append data to dictionary
    loaded_dict["MODHELP_TICKET_IDS"]=tuple(MODHELP_TICKET_IDS)
        
    # Serializing json
    json_object = json.dumps(loaded_dict, indent=4)
    
    # Writing to botjson.json
    with open("botjson.json", "w") as outfile:
        outfile.write(json_object)
        
#saves all variables to json
def save_to_json():
    
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
    
create_json_if_dne()

#save_to_json()

for role in ROLES:
    print(role["ID"])

newrole={"Name": "New Role",
        "ID": 0}
ROLES.append(newrole)
for role in ROLES:
    print(role["ID"])



# def set_to_dic(var_set):
    
#     #check if variable is a set
#     if not isinstance(var_set, set):
#         print('ERROR: Variable passed is not of type SET')
#         return
    
    
    
# str = 'message_id'
# # Converting set to dict
# #res = {element: 'message_id' for element in REACTION_MESSAGE}
# #res = dict.fromkeys(REACTION_MESSAGE)

# res = dict.fromkeys(str for x in REACTION_MESSAGE)

# res = {enumerate(REACTION_MESSAGE)}
# # for x in REACTION_MESSAGE:
# #     print(x)
    
#print(res)
    

# # Serializing json
# json_object = json.dumps(REACTION_MESSAGE, indent=4)
 
# # Writing to sample.json
# with open("sample.json", "w") as outfile:
#     outfile.write(json_object)
    
