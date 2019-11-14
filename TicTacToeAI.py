import numpy as np
def has_won(game):
    for g in range(0,6,3):
        if game[g] == game[g+1] == game[g+2] ==1:
            return "Player1"
        if game[g] == game[g+1] == game[g+2] ==2:
            return "Player2"
    for g in range(0,3):
        if game[g] == game[g+3] == game[g+6] ==1:
            return "Player1"
        if game[g] == game[g+3] == game[g+6] ==2:
            return "Player2"
    if game[0] == game[4] == game[8]==1 or game[2] == game[4] == game[6]==1:
        return "Player1"
    if game[0] == game[4] == game[8]==2 or game[2] == game[4] == game[6]==2:
        return "Player2"
    return "Tie"

def sigmoid(x,deriv):
    if deriv==False:
        return 1/(1+np.exp(-x))
    return np.exp(-x)/((1+np.exp(-x))**2)

def training(game, step, weight10, weight11, weight20, weight21):
    while 0 in game:
        second1 = sigmoid(np.dot(game, weight10), False)
        final1 = sigmoid(np.dot(second1, weight11), False)
        while game[np.argmax(final1)] != 0:
            final1[np.argmax(final1)] = -1
        game[np.argmax(final1)] = 1
        if has_won(game) != "Tie":
            return has_won(game)
        second2 = sigmoid(np.dot(game, weight20), False)
        final2 = sigmoid(np.dot(second2, weight21), False)
        while game[np.argmax(final2)] != 0 and 0 in game:
            final2[np.argmax(final2)] = -1
        game[np.argmax(final2)] = 2
        if has_won(game) != "Tie":
            return has_won(game)
    return "Tie"

def real_training(number):
    lis = list()
    game = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    step = [[.01], [.01], [.01], [.01], [.01], [.01], [.01], [.01], [.01]]
    weight10 = np.random.random((9, 9))
    weight11 = np.random.random((9, 9))
    weight20 = np.random.random((9, 9))
    weight21 = np.random.random((9, 9))
    for g in range(number):
        temp = training(game,step,weight10,weight11,weight20,weight21)
        lis.append(temp)
        if temp == "Player1":
            cross = weight10-weight20
            cross2 = weight11-weight21
            weight20 = weight20 + np.dot(.01,cross)
            weight21 = weight21 + np.dot(.01,cross2)
        if temp == "Player2" or temp == "Tie":
            cross = weight20-weight10
            cross2 = weight21-weight11
            weight10 = weight10 + np.dot(.01,cross)
            weight11 = weight11 + np.dot(.01,cross2)
        game = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    if temp == "Player1":
        print("Player1")
        return weight10,weight11
    if temp == "Player2" or temp == "Tie":
        print("Player2")
        return weight20,weight21
    return None

print(real_training(10000))
