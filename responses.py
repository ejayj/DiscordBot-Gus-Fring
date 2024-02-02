import random

def get_response(message: str) -> str:
    p_message = message.lower() 
    
    if p_message == 'hello':
        return 'Hey there!'
    
    if p_message == 'roll':
        return str(random.randint(1,6))
    
    if p_message == '!help':
        return '`This is a help message that you can modify. Currently, NULL.`'
    
    if p_message == 'help':
        return 'Hi! What can I assist you with today? Type !help for more.'
    
    if "gay" in p_message:
        return 'You are gay!'
    
    if "faggot" in p_message:
        int=random.randint(0,1)
        if int==0:
            return 'You can\'t say that! I\'m telling Daud!'
        elif int==1:
            return 'Call the cops!'
    
    return 'I didn\'t understand what you wrote. Try typing "!help".'