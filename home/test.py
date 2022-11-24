import random, time

def draw(playerNum, drawNum):
    if not deckStatus():
        return
    for i in range(drawNum):
        cardType = random.randint(0, 4)
        cardDraw = random.randint(0, len(deck[cardType]) - 1)
        while deck[cardType][cardDraw] == []:
            cardType = random.randint(0, 4)
            cardDraw = random.randint(0, len(deck[cardType]) - 1)
        hand[playerNum].append(f'{deckType[cardType]} {deck[cardType][cardDraw][0]}')
        deck[cardType][cardDraw].remove(deck[cardType][cardDraw][0])
    return

def winner():
    for i in range(NumOfPlayer):
        if hand[i] == []:
            return i
    return False

def choice():
    if not inhand():
        print(f'Player {turn + 1} has no cards with same colour or number or function cards')
        draw(turn, 1)
        time.sleep(1)
        return False
    print(lastCard)
    print(hand[turn])
    choose = input('Play or Draw: ')
    if choose == str(1):
        play = input('Enter number of the card you wish to play: ')
        while not play.isdecimal():
            play = input('Enter number of the card you wish to play (A NUMBER !!!):')
        play = int(play)
        if play > 0:
            play -= 1
        if hand[turn][play][0] == lastCard[0] or hand[turn][play][-1] == lastCard[-1] or hand[turn][play][0:3] == 'Fun':
            lastcard = hand[turn][play]
            print(f'{hand[turn][play]}')
            hand[turn].remove(hand[turn][play])
            time.sleep(1)
            if len(hand[turn]) == 1:
                if not hand[turn][0][-1].isdecimal():
                    print('The last card cannot be a function card. You have to draw another card')
                    time.sleep(1)
                    draw(turn, 1)
            return lastcard
        else:
            print('You cannot play this card, please enter another card to play')
            time.sleep(1)
            return choice()
    elif choose == str(2):
        time.sleep(1)
        print(f'Player {turn + 1} chooses to draw a card')
        draw(turn, 1)
        return False
    else:
        print('Please enter 1 for Play or 2 for Draw')
        time.sleep(1)
        return choice()

def skip():
    if lastCard[-3:-1] == 'ki':
        print('Skip the turn')
        return True
    else:
        return False

def drawtwo():
    if lastCard[-3:-1] == 'tw':
        print('Skip the turn')
        return True
    else:
        return False

def reverse():
    if lastCard[-3:-1] == 'rs':
        return True
    else:
        return False

def wild():
    if lastCard[-3:-1] == 'il':
        return True
    else:
        return False

def wildDrawFour():
    if lastCard[-3:-1] == 'ou':
        return True
    else:
        return False

def inhand():
    for i in range(len(hand[turn])):
        if lastCard[0:3] in hand[turn][i] or 'Fun' in hand[turn][i] or lastCard[-1] == hand[turn][i][-1]:
            return True
    return False

def deckStatus(): 
    for i in range(5):
        for j in range(len(deck[i])):
            if deck[i][j] != []:
                return True
    return False

def Draw():
    if deckStatus():
        return False
    else:
        for i in hand:
            for j in i:
                if j[0:3] == lastCard[0:3] or j[0:3] == 'Fun' or j[-1] == lastCard[-1]:
                    return False
    return True

deckType = ['Green', 'Yellow', 'Blue', 'Red', 'Function']
functionCard = []
greenCard = [[0]]
yellowCard = [[0]]
blueCard = [[0]]
redCard = [[0]]
function = ['skip', 'draw two', 'reverse', 'wild', 'wild draw four']
for i in range(1, 13):
    if i >= 10:
        greenCard += [[function[i - 10], function[i - 10]]]
        yellowCard += [[function[i - 10], function[i - 10]]]
        blueCard += [[function[i - 10], function[i - 10]]]
        redCard += [[function[i - 10], function[i - 10]]]
    else:
        greenCard += [[i, i]]
        yellowCard += [[i, i]]
        blueCard += [[i, i]]
        redCard += [[i, i]]
for i in range(1, 3):
    functionCard += [[function[i + 2], function[i + 2]]]

deck = [greenCard, yellowCard, blueCard, redCard, functionCard]
NumOfPlayer = int(input('Number of players: '))
while NumOfPlayer < 2 or NumOfPlayer > 10:
    print('There should be at least two players and at most ten players. ')
    NumOfPlayer = int(input('Number of players: '))
turn = 0
hand = []
cardType = random.randint(0, 3)
cardDraw = random.randint(0, 9)
lastCard = f'{deckType[cardType]} {deck[cardType][cardDraw][0]}'
deck[cardType][cardDraw].remove(deck[cardType][cardDraw][0])

for i in range(NumOfPlayer):
    hand.append([])
    draw(i, 7)

while type(winner()) == bool and not Draw():
    while type(winner()) == bool and not Draw():
        time.sleep(1)
        print(f'This is the turn for player {turn + 1}')
        if skip():
            turn += 1
            lastCard = lastCard[0 : 3] + ' ' + lastCard[-1]
        elif drawtwo():
            draw(turn, 2)
            turn += 1
            lastCard = lastCard[0 : 3] + ' ' + lastCard[-1]
        elif reverse():
            turn -= 1
            lastCard = lastCard[0 : 3] + ' ' + lastCard[-1]
            break
        else:
            Cache = choice()
            if Cache != False:
                lastCard = Cache
                if wild():
                    colour = input('Enter a colour: ')
                    while colour not in deckType[0:4]:
                        colour = input('Enter a valid colour')
                    lastCard = f'{colour}'
                elif wildDrawFour():
                    colour = input('Enter a colour: ')
                    while colour not in deckType[0:4]:
                        colour = input('Enter a valid colour')
                    lastCard = f'{colour}'
                    turn += 1
                    if turn == NumOfPlayer:
                        turn = 0
                    draw(turn, 4)
                    print('Next player will be skipped. ')
                turn += 1
            elif Cache == False:
                turn += 1
        if turn == NumOfPlayer:
            turn = 0
        if turn == -1:
            turn = NumOfPlayer - 1
    if turn == -1:
        turn = NumOfPlayer - 1
    if turn == NumOfPlayer:
        turn = 0
    while type(winner()) == bool and not Draw():
        time.sleep(1)
        print(f'This is the turn for player {turn + 1}')
        if skip():
            turn -= 1
            lastCard = lastCard[0 : 3] + ' ' + lastCard[-1]
        elif drawtwo():
            draw(turn, 2)
            turn -= 1
            lastCard = lastCard[0 : 3] + ' ' + lastCard[-1]
        elif reverse():
            turn += 1
            lastCard = lastCard[0 : 3] + ' ' + lastCard[-1]
            break
        else:
            Cache = choice()
            if Cache != False:
                lastCard = Cache
                if wild():
                    colour = input('Enter a colour: ')
                    while colour not in deckType[0:4]:
                        colour = input('Enter a valid colour')
                    lastCard = f'{colour}'
                elif wildDrawFour():
                    colour = input('Enter a colour: ')
                    while colour not in deckType[0:4]:
                        colour = input('Enter a valid colour')
                    lastCard = f'{colour}'
                turn -= 1
                print(lastCard)
            elif Cache == False:
                turn -= 1
                print(lastCard)
        if turn == NumOfPlayer:
            turn = 0
        if turn == -1:
            turn = NumOfPlayer - 1
    if turn == -1:
        turn = NumOfPlayer - 1
    if turn == NumOfPlayer:
        turn = 0


if Draw():
    print('Draw!! Try another game. ')
else:
    print(f'Player {turn + 1} wins the game!! Congratulations!')
    time.sleep(1)
    print('Copy the link below into a browser to get your certificate!')
    print('https://rb.gy/enaq3a')
    





