import time
import numpy as np
import math
import random
import copy
import threading
import sys

class Othello_Player:
    number_rep2 = None
    number_rep = None
    string_rep = None
    weight1=None
    weight2=None
    weight3=None
    bias1 = None
    bias2 = None
    bias3 = None
    fitness = 0
    fitness2=0
    stored_moves = set()
    battle_fitness = 0

    def make_random(self,size):
        temp = []
        lis = []
        for c in range(size):
            for g in range(size):
                lis.append(random.random())
            temp.append(lis)
            lis = []
        return temp

    def make_random2(self,size):
        temp = []
        for c in range(size):
            temp.append(random.random())
        return temp

    def make_numrep(self,rep):
        num_rep = list()
        for c in rep:
            if c==0:
                num_rep.append(0)
            if c==2:
                num_rep.append(-1)
            if c==1:
                num_rep.append(1)
        return num_rep

    def __init__(self):
        self.string_rep = ["?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", ".", ".", ".", ".", ".", ".", ".", ".", "?", "?",
                ".", ".", ".", ".", ".", ".", ".", ".", "?", "?", ".", ".", ".", ".", ".", ".", ".", ".", "?", "?", ".",
                ".", ".", "o", "@", ".", ".", ".", "?", "?", ".", ".", ".", "@",
                "o", ".", ".", ".", "?", "?", ".", ".", ".", ".", ".", ".", ".", ".", "?", "?", ".", ".", ".", ".", ".",
                ".", ".", ".", "?", "?", ".", ".", ".", ".", ".", ".", ".", ".", "?", "?", "?", "?", "?", "?", "?", "?",
                "?", "?", "?"]
        self.number_rep = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0]
        #self.number_rep = self.make_numrep(self.number_rep2)
        self.weight1 = self.make_random(100)
        self.weight2 = self.make_random(100)
        #self.weight3 = self.make_random(100)
        self.bias1 = self.make_random2(100)
        self.bias2 = self.make_random2(100)
       # self.bias3 = self.make_random2(100)


    def multiply_matrix(self,a, b):
        temp = 0
        lis = []
        for c in range(len(a)):
            if type(b[c]) == list:
                lis.append(self.multiply_matrix(a, b[c]))
            else:
                temp += a[c] * b[c]
        if temp != 0:
            return temp
        return lis

    def subtract(self,a, b):
        lis = []
        for c in b:
            if type(c) == list:
                lis.append(self.subtract(a, c))
            else:
                lis.append(a - c)
        return lis

    def subtract_matrix(self,a, b):
        lis = []
        for c in range(len(a)):
            if type(a[c]) == list:
                lis.append(self.subtract_matrix(a[c], b[c]))
            else:
                lis.append(a[c] - b[c])
        return lis

    def add_matrix(self,a, b):
        lis = []
        for c in range(len(a)):
            if type(a[c]) == list:
                lis.append(self.add_matrix(a[c], b[c]))
            else:
                lis.append(a[c] + b[c])
        return lis

    def multiply_single(self,a, b):
        lis = []
        for c in b:
            if type(c) == list:
                lis.append(self.multiply_single(a, c))
            else:
                lis.append(c * a)
        return lis

    def make_board(self,game):
        open_spaces = set()
        p1spaces = set()
        p2spaces = set()
        for g in range(100):
            if game[g] == ".":
                open_spaces.add(g)
            if game[g] == "@":
                p1spaces.add(g)
            if game[g] == "o":
                p2spaces.add(g)
        return open_spaces, p1spaces, p2spaces

    def search_directions(self,game, spot, num2):
        temp = set()
        se = set()
        num = 1
        # count = 0
        if num2 == 2:
            while game[spot + num] != "?" and game[spot + num] == "o":
                temp.add(spot + num)
                num += 1
                # count+=1
            if game[spot + num] == "@":
                se = se.union(temp)
            # count=0
            temp = set()
            num = 1
            while game[spot - num] != "?" and game[spot - num] == "o":
                temp.add(spot - num)
                num += 1
                # count+=1
            if game[spot - num] == "@":
                se = se.union(temp)
            # count = 0
            temp = set()
            num = 10
            while game[spot + num] != "?" and game[spot + num] == "o":
                temp.add(spot + num)
                num += 10
                # count += 1
            if game[spot + num] == "@":
                se = se.union(temp)
            # count = 0
            temp = set()
            num = 10
            while game[spot - num] != "?" and game[spot - num] == "o":
                temp.add(spot - num)
                num += 10
                # count += 1
            if game[spot - num] == "@":
                se = se.union(temp)
            # count = 0
            temp = set()
            num = 11
            while game[spot + num] != "?" and game[spot + num] == "o":
                temp.add(spot + num)
                num += 11
            if game[spot + num] == "@":
                se = se.union(temp)
            temp = set()
            num = 9
            while game[spot + num] != "?" and game[spot + num] == "o":
                temp.add(spot + num)
                num += 9
            if game[spot + num] == "@":
                se = se.union(temp)
            temp = set()
            num = 9
            while game[spot - num] != "?" and game[spot - num] == "o":
                temp.add(spot - num)
                num += 9
            if game[spot - num] == "@":
                se = se.union(temp)
            temp = set()
            num = 11
            while game[spot - num] != "?" and game[spot - num] == "o":
                temp.add(spot - num)
                num += 11
            if game[spot - num] == "@":
                se = se.union(temp)
        else:
            while game[spot + num] != "?" and game[spot + num] == "@":
                temp.add(spot + num)
                num += 1
                # count+=1
            if game[spot + num] == "o":
                se = se.union(temp)
            # count=0
            temp = set()
            num = 1
            while game[spot - num] != "?" and game[spot - num] == "@":
                temp.add(spot - num)
                num += 1
                # count+=1
            if game[spot - num] == "o":
                se = se.union(temp)
            # count = 0
            temp = set()
            num = 10
            while game[spot + num] != "?" and game[spot + num] == "@":
                temp.add(spot + num)
                num += 10
                # count += 1
            if game[spot + num] == "o":
                se = se.union(temp)
            # count = 0
            temp = set()
            num = 10
            while game[spot - num] != "?" and game[spot - num] == "@":
                temp.add(spot - num)
                num += 10
                # count += 1
            if game[spot - num] == "o":
                se = se.union(temp)
            # count = 0
            temp = set()
            num = 11
            while game[spot + num] != "?" and game[spot + num] == "@":
                temp.add(spot + num)
                num += 11
            if game[spot + num] == "o":
                se = se.union(temp)
            temp = set()
            num = 9
            while game[spot + num] != "?" and game[spot + num] == "@":
                temp.add(spot + num)
                num += 9
            if game[spot + num] == "o":
                se = se.union(temp)
            temp = set()
            num = 9
            while game[spot - num] != "?" and game[spot - num] == "@":
                temp.add(spot - num)
                num += 9
            if game[spot - num] == "o":
                se = se.union(temp)
            temp = set()
            num = 11
            while game[spot - num] != "?" and game[spot - num] == "@":
                temp.add(spot - num)
                num += 11
            if game[spot - num] == "o":
                se = se.union(temp)
        return se

    def available_moves(self,game, open_spaces, p1spaces, p2spaces, num):
        available = set()
        moves = dict()
        if num == 1:
            for g in p1spaces:
                if g + 1 in open_spaces:
                    available.add(g + 1)
                if g - 1 in open_spaces:
                    available.add(g - 1)
                if g - 10 in open_spaces:
                    available.add(g - 10)
                if g + 10 in open_spaces:
                    available.add(g + 10)
                if g + 11 in open_spaces:
                    available.add(g + 11)
                if g - 11 in open_spaces:
                    available.add(g - 11)
                if g + 9 in open_spaces:
                    available.add(g + 9)
                if g - 9 in open_spaces:
                    available.add(g - 9)
            for c in available:
                u = self.search_directions(game, c, num)
                if len(u) != 0:
                    moves.update({c: u})
        else:
            for g in p2spaces:
                if g + 1 in open_spaces:
                    available.add(g + 1)
                if g - 1 in open_spaces:
                    available.add(g - 1)
                if g - 10 in open_spaces:
                    available.add(g - 10)
                if g + 10 in open_spaces:
                    available.add(g + 10)
                if g + 11 in open_spaces:
                    available.add(g + 11)
                if g - 11 in open_spaces:
                    available.add(g - 11)
                if g + 9 in open_spaces:
                    available.add(g + 9)
                if g - 9 in open_spaces:
                    available.add(g - 9)
            for c in available:
                u = self.search_directions(game, c, num)
                if len(u) != 0:
                    moves.update({c: u})
        return moves

    def has_won(self,game):
        count1 = 0
        count2 = 0
        for g in game:
            if g == 1:
                count1 += 1
            if g == 2:
                count2 += 1
        # print(count1)
        # print(count2)
        if count1 > count2:
            return "Player1"
        if count2 > count1:
            return "Player2"
        return "Tie"

    def print_board(self):
        for g in range(10):
            for c in range(10):
                print(self.string_rep[10 * g + c], end=" ")
            print()

    def sigmoid(self,x, deriv):
        lis = []
        if deriv == False:
            for c in x:
                lis.append(1 / (1 + math.exp(-.01*c)))
            return lis
        for c in x:
            lis.append(math.exp(-.01*c) / ((1 + math.exp(-.01*c)) ** 2))
        return lis

    def sigmoid_single(self,x, deriv):
        lis = []
        if deriv == False:
            return 1 / (1 + math.exp(-.01*x))
        return math.exp(-.01*x) / ((1 + math.exp(-.01*x)) ** 2)

    def get_best_spot(self,final1,keys):
        spots = []
        values = []
        for c in keys:
            spots.append(c)
            values.append(final1[c])
        return spots[values.index(max(values))]

    def update_weights(self,avail_moves,play_position,layer1sum,layer1output,final1sum,final1output):
        self.string_rep[play_position] = "@"
        self.number_rep[play_position] = 1
        for c in avail_moves.get(play_position):
            self.number_rep[c] = 1
            self.string_rep[c] = "@"
        open_spaces, p1spaces, p2spaces = self.make_board(self.string_rep)
        temp = self.available_moves(self.string_rep, open_spaces, p1spaces, p2spaces, 2)
        if len(temp.keys())==0:
            return False
        layer2sum = np.add(np.dot(self.number_rep, self.weight1), self.bias1)
        layer2output = self.sigmoid(layer2sum, False)
        final2sum = np.add(np.dot(layer2output, self.weight2), self.bias2)
        final2output = self.sigmoid(final2sum, False)
        play_position2 = self.get_best_spot(final2output, temp.keys())
        error = len(avail_moves.get(play_position))+.1*final2output[play_position2]-final1output[play_position]
        outputsig = self.sigmoid_single(final1sum[play_position],True)*error
        middlesig = []
        tempweights2 = []
        tempweights = []
        for h in range(len(self.weight2)):
            for g in range(len(self.weight2)):
                tempweights.append(self.weight2[g][h])
            tempweights2.append(tempweights)
            tempweights = []
        for c in range(len(layer1sum)):
            middlesig.append(sum(tempweights2[c])*outputsig*self.sigmoid_single(layer1sum[c],True))
        # print(self.weight2[play_position])
        # print()
        self.weight2[play_position] = self.add_matrix(self.multiply_single(.1,(self.multiply_single(outputsig,layer1output))),self.weight2[play_position])
        # print(self.weight2[play_position])
        for c in range(len(self.weight1)):
            self.weight1[c] = self.add_matrix(self.multiply_single(.1,(self.multiply_single(middlesig[c],self.number_rep))),self.weight1[c])



    def simulate(self,we1,we2):
        mmmoves = []
        if we1!=None:
            self.weight1=we1
        if we2!=None:
            self.weight2 = we2
        self.string_rep = ["?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", ".", ".", ".", ".", ".", ".", ".",
                           ".", "?", "?", ".", ".", ".", ".", ".", ".", ".", ".", "?", "?", ".", ".", ".", ".", ".",
                           ".", ".", ".",
                           "?", "?", ".", ".", ".", "o", "@", ".", ".", ".", "?", "?", ".", ".", ".", "@",
                           "o", ".", ".", ".", "?", "?", ".", ".", ".", ".", ".", ".", ".", ".", "?", "?", ".", ".",
                           ".", ".", ".",
                           ".", ".", ".", "?", "?", ".", ".", ".", ".", ".", ".", ".", ".", "?", "?", "?", "?", "?",
                           "?", "?", "?", "?", "?", "?"]
        self.number_rep = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0,
                           0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0]
        count = 0
        open_spaces, p1spaces, p2spaces = self.make_board(self.string_rep)
        while "o" in self.string_rep and "@" in self.string_rep and "." in self.string_rep and count < 2:
            count = 0
            temp = self.available_moves(self.string_rep, open_spaces, p1spaces, p2spaces, 2)
            if len(temp.keys()) != 0:
                layer1sum = self.add_matrix(self.multiply_matrix(self.number_rep, self.weight1), self.bias1)
                layer1output = self.sigmoid(layer1sum,False)
                tyu = self.multiply_matrix(layer1output, self.weight2)
                final1sum = self.add_matrix(tyu, self.bias2)
                final1output = self.sigmoid(final1sum,False)
                #second1 = self.sigmoid(np.add(np.dot(self.number_rep, self.weight1),self.bias1), False)
                #third1 = self.sigmoid(np.add(np.dot(second1, self.weight2),self.bias2), False)
                #final1 = self.sigmoid(np.add(np.dot(third1, self.weight3),self.bias3), False)
                play_position = self.get_best_spot(final1output,temp.keys())
                mmmoves.append(play_position)
                # while final1.index(max(final1)) not in temp.keys():
                #     final1[final1.index(max(final1))] = -1
                yuy = self.update_weights(temp,play_position,layer1sum,layer1output,final1sum,final1output)
                # self.string_rep[play_position] = "@"
                # self.number_rep[play_position] = 1
                # for c in temp.get(play_position):
                #     self.number_rep[c] = 1
                #     self.string_rep[c] = "@"
                open_spaces, p1spaces, p2spaces = self.make_board(self.string_rep)
            else:
                count += 1
            if "." in self.string_rep:
                temp = self.available_moves(self.string_rep, open_spaces, p1spaces, p2spaces, 1)
                index = 0
                cou = 0
                for h in temp.keys():
                    if cou == 0:
                        index = h
                        cou += 1
                    if len(temp.get(h)) > len(temp.get(index)):
                        index = h
                cou = 0
                if len(temp.keys()) != 0:
                    self.string_rep[index] = "o"
                    self.number_rep[index] = -1
                    mmmoves.append(index)
                    for c in temp.get(index):
                        self.string_rep[c] = "o"
                        self.number_rep[c] = -1
                    open_spaces, p1spaces, p2spaces = self.make_board(self.string_rep)
                else:
                    count += 1
        open_spaces, p1spaces, p2spaces = self.make_board(self.string_rep)
        self.fitness = len(p1spaces)
        return self.fitness,mmmoves

#class Play:




oth = Othello_Player()
#op = copy.deepcopy(oth.weight1)
# print(op)
# print()
we1 = None
we2 = None
num=1
se = list()
for c in range(100000):
    print(num,end=" ")
    fit,moves = oth.simulate(we1,we2)
    if moves not in se:
        se.append(moves)
    print(fit)
    print()
    we1 = oth.weight1
    we2 = oth.weight2
    num+=1
sample = open('weightfile.txt', 'w')
print(we1,file=sample)
print(we2,file=sample)
print(oth.bias1,file=sample)
print(oth.bias2,file=sample)
# print(se)
# print(len(se))
#op2 = oth.weight1
# print(op2)
#print(oth.subtract_matrix(op2,op))
