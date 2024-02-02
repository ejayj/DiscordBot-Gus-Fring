import random

def get_response(message: str) -> str:
    p_message = message.lower() 
    
    if p_message == 'hello':
        return 'Hey there!'
    
    if p_message == 'roll':
        return str(random.randint(1,6))
    
    if p_message == '!help':
        return '`For help with a specific command, type /help on my Los Pollos Hermanos server. For modhelp, use @ModMail. To start a server, use /requeststartserver in the Los Pollos Hermanos server.\n For suggests, type in the #requesthelp channel on the server. \n For server technical problems, message @ejayj directly!`'
    
    if p_message == 'help':
        return 'Hi! What can I assist you with today? Type !help for more.'
    
    if "gay" in p_message:
        return 'You are gay!'
    
    if "faggot" in p_message:
        int=random.randint(0,3)
        if int==0:
            return 'You can\'t say that! I\'m telling Daud!'
        elif int==1:
            return 'Call the cops!'
        elif int==3:
            return 'That\'s mean! :('
        elif int==4:
            return 'Bend over rn'
    
    return 'I didn\'t understand what you wrote. Try typing "!help".'