from PyInquirer import prompt

def play(cardnames, text):
    
    cardSelection = {'type' : 'list'}
    cardSelection['name'] = 'user_option'
    cardSelection['message'] = text
    cardSelection['choices'] = cardnames
        
    selectedCard = prompt(cardSelection)
    return selectedCard['user_option']

    