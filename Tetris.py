import random
import time

board = [[" "]*10]*20
piece_dic = {"I":["-1,-2,-3","-10,-20,-30"],"O":["-1,-10,-11"],"T":["-1,-2,-11","-10,-9,-20","-9,-10,-11","-10,-11,-20"],"S":["-1,-9,-10","-10,-11,-21"],
             "Z":["-1,-11,-12","-9,-10,-19"],"J":["-1,-2,-12","-10,-20,-19","-10,-11,-12","-1,-10,-20"],"L":["-1,-2,-10","-1,-11,-21","-10,-9,-8","-10,-20,-21"]}

def print_game(game):
    for c in range(200):
        print(game[c],end="")
        if c%10==9:
            print()

def clear_rows(game):
    count=0
    count2 =0
    c=0
    points = 0
    while c<200:
        if game[c]=="#":
            count+=1
        else:
            c = ((c//10)+1)*10-1
            count=0
        if count==10:
            count2+=1
            for g in range((c//10)*10-1,-1,-1):
                game[g+10]=game[g]
            for g in range(10):
                game[g]=" "
        c+=1
    if count2==1:
        points=40
    elif count2==2:
        points = 100
    elif count2==3:
        points=300
    elif count2==4:
        points=1200
    return points

def check_possible(game,pos,piece):
    count=0
    for g in range(pos // 10):
        if game[pos-10*g]=="#":
            count+=1
            return False
    for c in piece:
        for g in range(pos//10):
            if game[(pos+c)-10*g]=="#":
                count+=1
                return False
    return True

def check_all(game):
    count=0
    for c in piece_dic:
        for g in piece_dic.get(c):
            s = g.split(",")
            s = [int(i) for i in s]
            for h in range(0,200):
                count = len(s) + 1
                for k in s:
                    if abs((h+k)%10-h%10)>4:#h+k<0 or abs((h+k)%10-h%10)>4 or game[h]!="." or game[h+k]!=".":
                        break
                    elif h+k<0 and game[h+10]=="#":
                        print("GAME OVER")
                        break
                    elif check_possible(game,h,s)==False:
                        break
                    elif game[h]!=" ":
                        break
                    elif game[h+k]!=" ":
                        break
                    else:
                        count-=1
                    if h+10>199 or (h<190 and game[h+10]=="#") or (h+k+10<200 and game[h+k+10]=="#"):
                        count-=1
                if count<=-1:
                    game2 = list(game)
                    game2[h]="#"
                    for p in s:
                        game2[h+p]="#"
                    game3 = list(game2)
                    clear_rows(game3)
                    while game3!=game2:
                        game2=game3
                        clear_rows(game3)
                    print_game(game2)
                    print()

def make_board():
    s=""
    for c in range(200):
        s+= " "
    return s

def get_children(board,piece,points):
        children = []
        for g in piece_dic.get(piece):
            s = g.split(",")
            s = [int(i) for i in s]
            for h in range(0,200):
                count = len(s) + 1
                for k in s:
                    if abs((h+k)%10-h%10)>4:#h+k<0 or abs((h+k)%10-h%10)>4 or game[h]!="." or game[h+k]!=".":
                        break
                    elif h+k<0 and board[h+10]=="#":
                        break
                    elif check_possible(board,h,s)==False:
                        break
                    elif board[h]!=" ":
                        break
                    elif board[h+k]!=" ":
                        break
                    else:
                        count-=1
                    if h+10>199 or (h<190 and board[h+10]=="#") or (h+k+10<200 and board[h+k+10]=="#"):
                        count-=1
                if count<=-1:
                    temp_points = points
                    game2 = list(board)
                    game2[h]="#"
                    for p in s:
                        game2[h+p]="#"
                    game3 = list(game2)
                    temp_points+=clear_rows(game3)
                    while game3!=game2:
                        game2=game3
                        temp_points+=clear_rows(game3)
                    children.append((game2,temp_points))
        return children

def score(board,strategy,points):
    a,b,c,d = strategy
    score = 0
    holes=0
    highest =0
    deepest =0
    for c in range(10,200):
        if board[c-10]=="#" and board[c]==" ":
            holes+=1
    for c in range(200):
        if board[c]=="#":
            highest=c
            break
    for c in range(10):
        temp=0
        for g in range(20):
            if board[10*g+c]==" ":
                temp+=1
            if board[10*g+c]=="#":
                if temp>deepest:
                    deepest=temp
                break
    score += a*holes
    score += b*highest
    score += c*deepest
    score += d*points
    return score



def get_best_child(strategy,piece,board,points):
    children = get_children(board,piece,points)
    if children==[]:
        return (0,points,0,0),"GAME OVER"
    children2 = []
    for c in children:
        children2.append((score(c[0],strategy,c[1]),c[1],random.random(),c[0]))
    children2 = sorted(children2,reverse=True)
    return children2[0], "Still Playing"

def play_game(strategy):
    board = make_board()
    points = 0
    status = "Still Playing"
    while 1==1:
        piece = random.choice(list(piece_dic.keys()))
        temp, status = get_best_child(strategy,piece,board,points)
        board = temp[3]
        points = temp[1]
        if status == "GAME OVER":
            break
    return points

def make_population(num):
    population = []
    for c in range(num):
        population.append((random.random()*2,random.random()*2,random.random()*2,random.random()*2))
    return population

def fitness_function(strategy):
    game_scores = []
    for count in range(5):
        game_scores.append(play_game(strategy))
    return sum(game_scores)/len(game_scores)

def swap_perm(parent1,parent2,mutation_rate):
    child = []
    for c in range(4):
        boo = random.random()
        if boo<.75:
            child.append(parent1[c])
        else:
            child.append(parent2[c])
    if random.random()<mutation_rate:
        child[random.randint(0,3)]=random.random()*2
    return tuple(child)

def reproduce(population,clones,size,parents,mutation_rate):
    children = []
    for c in range(clones):
        children.append(population[c][2])
    for c in range(0,parents,2):
        for g in range((size-clones)//(parents//2)):
            children.append(swap_perm(population[c][2],population[c+1][2],mutation_rate))
    return children

decision = input("NEW GENETIC PROCESS OR OLD GENETIC PROCESS? (TYPE O or N)")
if decision =="N":
    file_temp = input("WHAT FILE DO YOU WANT TO WRITE TO?")
    file1 = open(file_temp,"w+")
    POPULATION_SIZE = 500
    CLONES = 50
    PARENTS = 50
    #TOURNAMENT_SIZE = 20
    # TOURNAMENT_WIN = .95
    MUTATION_RATE = .8
    population = make_population(POPULATION_SIZE)
    population2=[[0,0]]
    while population2[0][0]<50000:
        population2 = []
        for g in population:
            population2.append((fitness_function(g),random.random(),g))
        population2 = sorted(population2,reverse=True)
        file1.truncate()
        file1.write(population2)
        population = reproduce(population2,CLONES,POPULATION_SIZE,PARENTS,MUTATION_RATE)



# s="                                                                                                                                                                                                        "
# # s3="                                                                                                                                                                                                        "
# s2 = ""
# for c in range(180):
#     s2+="."
# s2= "...........#########" + s2
# check_all(list(s2))
# start = time.perf_counter()
# for c in range(200):
#     print(play_game([1,2,3,4]))
# end = time.perf_counter()
# print(end-start)