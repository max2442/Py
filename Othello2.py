import time
#import numpy as np
import math
import random
import sys

class Othello_Player:
    number_rep = None
    string_rep = None
    weight1=None
    weight2=None
    weight3=None
    bias1 = None
    bias2 = None
    bias3 = None
    fitness = None
    fitness2=None

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

    def __init__(self):
        self.string_rep = ["?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", ".", ".", ".", ".", ".", ".", ".", ".", "?", "?",
                ".", ".", ".", ".", ".", ".", ".", ".", "?", "?", ".", ".", ".", ".", ".", ".", ".", ".", "?", "?", ".",
                ".", ".", "o", "@", ".", ".", ".", "?", "?", ".", ".", ".", "@",
                "o", ".", ".", ".", "?", "?", ".", ".", ".", ".", ".", ".", ".", ".", "?", "?", ".", ".", ".", ".", ".",
                ".", ".", ".", "?", "?", ".", ".", ".", ".", ".", ".", ".", ".", "?", "?", "?", "?", "?", "?", "?", "?",
                "?", "?", "?"]
        self.number_rep = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1,
                 -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 2, 1, 0, 0, 0, -1, -1, 0, 0, 0, 1, 2, 0, 0, 0, -1, -1, 0,
                 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1,
                 -1, -1, -1, -1, -1, -1, -1]
        self.weight1 = self.make_random(100)
        self.weight2 = self.make_random(100)
        self.weight3 = self.make_random(100)
        self.bias1 = self.make_random2(100)
        self.bias2 = self.make_random2(100)
        self.bias3 = self.make_random2(100)


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
                lis.append(1 / (1 + math.exp(-c)))
            return lis
        for c in x:
            lis.append(math.exp(-c) / ((1 + math.exp(-c)) ** 2))
        return lis

    def get_best_spot(self,final1,keys):
        spots = []
        values = []
        for c in keys:
            spots.append(c)
            values.append(final1[c])
        return spots[values.index(max(values))]

    def simulate(self):
        self.string_rep = ["?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", ".", ".", ".", ".", ".", ".", ".",
                           ".", "?", "?", ".", ".", ".", ".", ".", ".", ".", ".", "?", "?", ".", ".", ".", ".", ".",
                           ".", ".", ".",
                           "?", "?", ".", ".", ".", "o", "@", ".", ".", ".", "?", "?", ".", ".", ".", "@",
                           "o", ".", ".", ".", "?", "?", ".", ".", ".", ".", ".", ".", ".", ".", "?", "?", ".", ".",
                           ".", ".", ".",
                           ".", ".", ".", "?", "?", ".", ".", ".", ".", ".", ".", ".", ".", "?", "?", "?", "?", "?",
                           "?", "?", "?", "?", "?", "?"]
        self.number_rep = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0,
                           0, 0, -1,
                           -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 2, 1, 0, 0, 0, -1, -1, 0, 0, 0, 1, 2, 0, 0, 0,
                           -1, -1, 0,
                           0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1,
                           -1, -1, -1, -1, -1, -1, -1, -1, -1]
        count = 0
        open_spaces, p1spaces, p2spaces = self.make_board(self.string_rep)
        while "o" in self.string_rep and "@" in self.string_rep and "." in self.string_rep and count < 2:
            count = 0
            temp = self.available_moves(self.string_rep, open_spaces, p1spaces, p2spaces, 2)
            if len(temp.keys()) != 0:
                second1 = self.sigmoid(self.add_matrix(self.multiply_matrix(self.number_rep, self.weight1),self.bias1), False)
                third1 = self.sigmoid(self.add_matrix(self.multiply_matrix(second1, self.weight2),self.bias2), False)
                final1 = self.sigmoid(self.add_matrix(self.multiply_matrix(third1, self.weight3),self.bias3), False)
                play_position = self.get_best_spot(final1,temp.keys())
                # while final1.index(max(final1)) not in temp.keys():
                #     final1[final1.index(max(final1))] = -1
                self.string_rep[play_position] = "@"
                self.number_rep[play_position] = 1
                for c in temp.get(play_position):
                    self.number_rep[c] = 1
                    self.string_rep[c] = "@"
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
                    self.number_rep[index] = 2
                    for c in temp.get(index):
                        self.string_rep[c] = "o"
                        self.number_rep[c] = 2
                    open_spaces, p1spaces, p2spaces = self.make_board(self.string_rep)
                else:
                    count += 1
        open_spaces, p1spaces, p2spaces = self.make_board(self.string_rep)
        self.fitness = len(p1spaces)
        return self.fitness

    def simulate3(self):
        count = 0
        self.string_rep = ["?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", ".", ".", ".", ".", ".", ".", ".",
                           ".", "?", "?",".", ".", ".", ".", ".", ".", ".", ".", "?", "?", ".", ".", ".", ".", ".", ".", ".", ".",
                           "?", "?", ".",".", ".", "o", "@", ".", ".", ".", "?", "?", ".", ".", ".", "@",
                           "o", ".", ".", ".", "?", "?", ".", ".", ".", ".", ".", ".", ".", ".", "?", "?", ".", ".",".", ".", ".",
                           ".", ".", ".", "?", "?", ".", ".", ".", ".", ".", ".", ".", ".", "?", "?", "?", "?", "?","?", "?", "?","?", "?", "?"]
        self.number_rep = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0,0, 0, -1,
                           -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 2, 1, 0, 0, 0, -1, -1, 0, 0, 0, 1, 2, 0, 0, 0,-1, -1, 0,
                           0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1,
                           -1, -1,-1, -1, -1, -1, -1, -1, -1]
        open_spaces, p1spaces, p2spaces = self.make_board(self.string_rep)
        while "o" in self.string_rep and "@" in self.string_rep and "." in self.string_rep and count < 2:
            count=0
            temp = self.available_moves(self.string_rep, open_spaces, p1spaces, p2spaces, 2)
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
                self.string_rep[index] = "@"
                self.number_rep[index] = 1
                for c in temp.get(index):
                    self.string_rep[c] = "@"
                    self.number_rep[c] = 1
                open_spaces, p1spaces, p2spaces = self.make_board(self.string_rep)
            else:
                count += 1
            if "." in self.string_rep:
                temp = self.available_moves(self.string_rep, open_spaces, p1spaces, p2spaces, 1)
                if len(temp.keys()) != 0:
                    second1 = self.sigmoid(self.add_matrix(self.multiply_matrix(self.number_rep, self.weight1),self.bias1), False)
                    third1 = self.sigmoid(self.add_matrix(self.multiply_matrix(second1, self.weight2),self.bias2), False)
                    final1 = self.sigmoid(self.add_matrix(self.multiply_matrix(third1, self.weight3),self.bias3), False)
                    play_position = self.get_best_spot(final1, temp.keys())
                    # while final1.index(max(final1)) not in temp.keys():
                    #     final1[final1.index(max(final1))] = -1
                    self.string_rep[play_position] = "o"
                    self.number_rep[play_position] = 2
                    for c in temp.get(play_position):
                        self.number_rep[c] = 2
                        self.string_rep[c] = "o"
                    open_spaces, p1spaces, p2spaces = self.make_board(self.string_rep)
                else:
                    count += 1
        open_spaces, p1spaces, p2spaces = self.make_board(self.string_rep)
        self.fitness2 = len(p2spaces)
        return self.fitness2

    def simulate2(self,othello_player):
        count = 0
        open_spaces, p1spaces, p2spaces = self.make_board(self.string_rep)
        while "o" in self.string_rep and "@" in self.string_rep and "." in self.string_rep and count < 2:
            count = 0
            temp = self.available_moves(self.string_rep, open_spaces, p1spaces, p2spaces, 2)
            if len(temp.keys()) != 0:
                second1 = self.sigmoid(self.add_matrix(self.multiply_matrix(self.number_rep, self.weight1),self.bias1),False)
                third1 = self.sigmoid(self.add_matrix(self.multiply_matrix(second1, self.weight2),self.bias2), False)
                final1 = self.sigmoid(self.add_matrix(self.multiply_matrix(third1, self.weight3),self.bias3), False)
                while final1.index(max(final1)) not in temp.keys():
                    final1[final1.index(max(final1))] = -1
                self.string_rep[final1.index(max(final1))] = "@"
                self.number_rep[final1.index(max(final1))] = 1
                for c in temp.get(final1.index(max(final1))):
                    self.number_rep[c] = 1
                    self.string_rep[c] = "@"
                open_spaces, p1spaces, p2spaces = self.make_board(self.string_rep)
            else:
                count += 1
            if "." in self.string_rep:
                temp = self.available_moves(self.string_rep, open_spaces, p1spaces, p2spaces, 1)
                if len(temp.keys()) != 0:
                    second2 = self.sigmoid(self.multiply_matrix(self.number_rep, othello_player.weight1), False)
                    third2 = self.sigmoid(self.multiply_matrix(second2, othello_player.weight2), False)
                    final2 = self.sigmoid(self.multiply_matrix(third2, othello_player.weight3), False)
                    while final2.index(max(final2)) not in temp.keys():
                        final2[final2.index(max(final2))] = -1
                    self.string_rep[final2.index(max(final2))] = "o"
                    self.number_rep[final2.index(max(final2))] = 2
                    for c in temp.get(final2.index(max(final2))):
                        self.number_rep[c] = 2
                        self.string_rep[c] = "o"
                    open_spaces, p1spaces, p2spaces = self.make_board(self.string_rep)
                else:
                    count += 1
        open_spaces, p1spaces, p2spaces = self.make_board(self.string_rep)
        self.fitness = len(p1spaces)
        return self.fitness

def make_random3(size):
    temp = []
    lis = []
    for c in range(size):
        for g in range(size):
            lis.append(random.random())
        temp.append(lis)
        lis = []
    return temp

def make_random4(size):
    temp = []
    for c in range(size):
        temp.append(random.random())
    return temp

def reproduce(parent1,parent2):
    lis = []
    for c in range(8):
        temp = make_random3(100)
        temp2 = make_random3(100)
        temp3 = make_random3(100)
        temp11 = make_random4(100)
        temp22 = make_random4(100)
        temp33 = make_random4(100)
        for g in range(100):
            for h in range(100):
                n = random.randint(0,2)
                if n==0:
                    temp[g][h] = parent1.weight1[g][h]
                    temp2[g][h] = parent1.weight2[g][h]
                    temp3[g][h] = parent1.weight3[g][h]

                elif n==1:
                    temp[g][h] = parent2.weight1[g][h]
                    temp2[g][h] = parent2.weight2[g][h]
                    temp3[g][h] = parent2.weight3[g][h]
                else:
                    temp[g][h] = (parent1.weight1[g][h]+parent2.weight1[g][h])/2
                    temp2[g][h] = (parent1.weight2[g][h] + parent2.weight2[g][h])/2
                    temp3[g][h] = (parent1.weight3[g][h] + parent2.weight3[g][h])/2
            n = random.randint(0,2)
            if n == 0:
                temp11[g] = parent1.bias1[g]
                temp22[g] = parent1.bias2[g]
                temp33[g] = parent1.bias3[g]

            elif n == 1:
                temp11[g] = parent2.bias1[g]
                temp22[g] = parent2.bias2[g]
                temp33[g] = parent2.bias3[g]
            else:
                temp11[g] = (parent1.bias1[g] + parent2.bias1[g]) / 2
                temp22[g] = (parent1.bias2[g] + parent2.bias2[g]) / 2
                temp33[g] = (parent1.bias3[g] + parent2.bias3[g]) / 2
        oth = Othello_Player()
        oth.weight1 = temp
        oth.weight2 = temp2
        oth.weight3 = temp3
        oth.bias1 = temp11
        oth.bias2 = temp22
        oth.bias3 = temp33
        lis.append(oth)
    return lis

def evolve():
    player_list = []
    born_players =[]
    born_players2 =[]
    num = 0
    save = None
    for c in range(50):
        io = Othello_Player()
        io.simulate()
        io.simulate3()
        #print(io.fitness)
        player_list.append((io.fitness+io.fitness2,io.fitness,io.fitness2,random.random(),io))
    #print()
    while num<5:
        print(num)
        player_list = sorted(player_list,reverse=True)
        print(player_list[0][1])
        print(player_list[0][2])
        #if (num+1)%20 ==0:
            #save=player_list[0][2]
        for g in range(0,10,2):
            born_players2.append(player_list[g][4])
            born_players2.append(player_list[g+1][4])
            born_players = reproduce(player_list[g][4],player_list[g+1][4])
            for h in born_players:
                born_players2.append(h)
        player_list = []
        player_list.append((born_players2[0].fitness+born_players2[0].fitness2,born_players2[0].fitness,born_players2[0].fitness2,random.random(),born_players2[0]))
        player_list.append((born_players2[1].fitness + born_players2[1].fitness2, born_players2[1].fitness,born_players2[1].fitness2, random.random(), born_players2[1]))
        born_players2.remove(born_players2[1])
        born_players2.remove(born_players2[0])
        for h in born_players2:
            if save ==None:
                h.simulate()
                h.simulate3()
            else:
                h.simulate2(save)
            #print(h.fitness,end=" ")
            #print(h.fitness2)
            player_list.append((h.fitness+h.fitness2,h.fitness,h.fitness2,random.random(),h))
        print()
        # if (num+1)%10==0:
        #     print("New Village Head")
        num+=1
    player_list = sorted(player_list, reverse=True)
    # print(player_list[0][1])
    # print(player_list[0][2])
    print(player_list[0][4].weight1)
    print(player_list[0][4].weight2)
    print(player_list[0][4].weight3)
    print(player_list[0][4].bias1)
    print(player_list[0][4].bias2)
    print(player_list[0][4].bias3)

evolve(sys.argv[1])
