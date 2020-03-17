import time
import queue
import heapq
from random import randrange
from copy import copy, deepcopy
import math
import sys

start_time = time.time()

f = open("input.txt","r")

white_initial_move_heuristic = [[30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,15],
[29,28,27,26,25,24,23,22,21,20,19,18,17,16,15,14],
[28,27,26,25,24,23,22,21,20,19,18,17,16,15,14,13],
[27,26,25,24,23,22,21,20,19,18,17,16,15,14,13,12],
[26,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11],
[25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10],
[24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9],
[23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8],
[22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7],
[21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6],
[20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5],
[19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4],
[18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3],
[17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2],
[16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1],
[15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]
]

black_initial_move_heuristic = [[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18],
[4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],
[5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
[6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21],
[7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22],
[8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
[9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],
[10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25],
[11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26],
[12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
[13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],
[14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29],
[15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]]


black_min_dist = [[21213, 20518, 19849, 19209, 18601, 18027, 17492, 17000, 16552, 16155, 15811, 15524, 15297, 15132, 15033, 15000], [20518, 19798, 19104, 18439, 17804, 17204, 16643, 16124, 15652, 15231, 14866, 14560, 14317, 14142, 14035, 14000], [19849, 19104, 18384, 17691, 17029, 16401, 15811, 15264, 14764, 14317, 13928, 13601, 13341, 13152, 13038, 13000], [19209, 18439, 17691, 16970, 16278, 15620, 15000, 14422, 13892, 13416, 13000, 12649, 12369, 12165, 12041, 12000], [18601, 17804, 17029, 16278, 15556, 14866, 14212, 13601, 13038, 12529, 12083, 11704, 11401, 11180, 11045, 11000], [18027, 17204, 16401, 15620, 14866, 14142, 13453, 12806, 12206, 11661, 11180, 10770, 10440, 10198, 10049, 10000], [17492, 16643, 15811, 15000, 14212, 13453, 12727, 12041, 11401, 10816, 10295, 9848, 9486, 9219, 9055, 9000], [17000, 16124, 15264, 14422, 13601, 12806, 12041, 11313, 10630, 10000, 9433, 8944, 8544, 8246, 8062, 8000], [16552, 15652, 14764, 13892, 13038, 12206, 11401, 10630, 9899, 9219, 8602, 8062, 7615, 7280, 7071, 7000], [16155, 15231, 14317, 13416, 12529, 11661, 10816, 10000, 9219, 8485, 7810, 7211, 6708, 6324, 6082, 6000], [15811, 14866, 13928, 13000, 12083, 11180, 10295, 9433, 8602, 7810, 7071, 6403, 5830, 5385, 5099, 5000], [15524, 14560, 13601, 12649, 11704, 10770, 9848, 8944, 8062, 7211, 6403, 5656, 5000, 4472, 4123, 4000], [15297, 14317, 13341, 12369, 11401, 10440, 9486, 8544, 7615, 6708, 5830, 5000, 4242, 3605, 3162, 3000], [15132, 14142, 13152, 12165, 11180, 10198, 9219, 8246, 7280, 6324, 5385, 4472, 3605, 2828, 2236, 2000], [15033, 14035, 13038, 12041, 11045, 10049, 9055, 8062, 7071, 6082, 5099, 4123, 3162, 2236, 1414, 1000], [15000, 14000, 13000, 12000, 11000, 10000, 9000, 8000, 7000, 6000, 5000, 4000, 3000, 2000, 1000, 0]]
white_min_dist = [[0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000], [1000, 1414, 2236, 3162, 4123, 5099, 6082, 7071, 8062, 9055, 10049, 11045, 12041, 13038, 14035, 15033], [2000, 2236, 2828, 3605, 4472, 5385, 6324, 7280, 8246, 9219, 10198, 11180, 12165, 13152, 14142, 15132], [3000, 3162, 3605, 4242, 5000, 5830, 6708, 7615, 8544, 9486, 10440, 11401, 12369, 13341, 14317, 15297], [4000, 4123, 4472, 5000, 5656, 6403, 7211, 8062, 8944, 9848, 10770, 11704, 12649, 13601, 14560, 15524], [5000, 5099, 5385, 5830, 6403, 7071, 7810, 8602, 9433, 10295, 11180, 12083, 13000, 13928, 14866, 15811], [6000, 6082, 6324, 6708, 7211, 7810, 8485, 9219, 10000, 10816, 11661, 12529, 13416, 14317, 15231, 16155], [7000, 7071, 7280, 7615, 8062, 8602, 9219, 9899, 10630, 11401, 12206, 13038, 13892, 14764, 15652, 16552], [8000, 8062, 8246, 8544, 8944, 9433, 10000, 10630, 11313, 12041, 12806, 13601, 14422, 15264, 16124, 17000], [9000, 9055, 9219, 9486, 9848, 10295, 10816, 11401, 12041, 12727, 13453, 14212, 15000, 15811, 16643, 17492], [10000, 10049, 10198, 10440, 10770, 11180, 11661, 12206, 12806, 13453, 14142, 14866, 15620, 16401, 17204, 18027], [11000, 11045, 11180, 11401, 11704, 12083, 12529, 13038, 13601, 14212, 14866, 15556, 16278, 17029, 17804, 18601], [12000, 12041, 12165, 12369, 12649, 13000, 13416, 13892, 14422, 15000, 15620, 16278, 16970, 17691, 18439, 19209], [13000, 13038, 13152, 13341, 13601, 13928, 14317, 14764, 15264, 15811, 16401, 17029, 17691, 18384, 19104, 19849], [14000, 14035, 14142, 14317, 14560, 14866, 15231, 15652, 16124, 16643, 17204, 17804, 18439, 19104, 19798, 20518], [15000, 15033, 15132, 15297, 15524, 15811, 16155, 16552, 17000, 17492, 18027, 18601, 19209, 19849, 20518, 21213]]


# making these 2 sets so that white and black ki territory pata rhe
# y pehle  hai then x
blackposition_Set = {(0,0),(1,0),(2,0),(3,0),(4,0),(0,1),(1,1),(2,1),(3,1),(4,1),(0,2),(1,2),(2,2),(3,2),(0,3),(1,3),(2,3),(0,4),(1,4)}
whiteposition_Set = {(15,15),(14,15),(13,15),(12,15),(11,15),(15,14),(14,14),(13,14),(12,14),(11,14),(15,13),(14,13),(13,13),(12,13),(15,12),(14,12),(13,12),(15,11),(14,11)}




heuristic_to_order_moves = black_min_dist
# arrays to look in all 8 directions
x_checker = [-1, -1, -1, 0, 0, 1, 1, 1]
y_checker = [-1, 0, 1, -1, 1, -1, 0, 1]

# Single or Game
gameType = ""
# my color of the pawn
yourColor = ""
# Time I have for the move
time_Remaining = 0

iterator = 0

stop_depth = 3

board = []

for line in f.readlines():
    if(iterator is 0):
        gameType = line.rstrip()
        iterator += 1
        continue
    if(iterator is 1):
        yourColor = str(line.rstrip())
        iterator += 1
        continue
    if(iterator is 2):
        time_Remaining = float(line)
        iterator += 1
        continue
    l = line.rstrip()
    temp = list(l)
    board.append(temp)

checking_Status = 'B'
if yourColor == "BLACK":
    checking_Status = 'B'
    heuristic_to_order_moves = black_min_dist
else:
    checking_Status = 'W'
    heuristic_to_order_moves = white_min_dist

# board universal reference hai
# can I move to the adjacent empty cell and then start the jumping sequence? NO

# preparing the visited matrix
tovelo = [False] *16
visited = []
for fillup in range (0,16):
    visited.append(deepcopy(tovelo))
    # visited.append(tovelo.copy())

# time_left = float(time_Remaining)

def calc_MD(refx,refy,givenx,giveny):
    return abs(refx-givenx)+abs(refy-giveny)

def check_If_Valid(old_x,old_y,new_x,new_y,refx,refy,set_Home):
    old_tup_coor = (old_y,old_x)
    new_tup_coor = (new_y,new_x)
    # old tuple coordinates are the ones of the initial position
    # new tuple coordinates are of new position
    opp_set = blackposition_Set
    if set_Home == blackposition_Set:
        opp_set = whiteposition_Set
    else:
        opp_set = blackposition_Set

    if(new_tup_coor not in set_Home and old_tup_coor in set_Home):
        return True
    elif (new_tup_coor in set_Home and old_tup_coor not in set_Home):
        return False
    elif (new_tup_coor in set_Home and old_tup_coor in set_Home):
        old_MD = calc_MD(refx,refy,old_x,old_y)
        new_MD = calc_MD(refx,refy,new_x,new_y)
        if(new_MD>old_MD):
            return True
        else:
            return False
    elif (new_tup_coor not in opp_set and old_tup_coor in opp_set):
        # print("aya")
        return False

    return True

def get_Jumpstates2(x,y,px,py,state_Q,addstart,boardco,in_pos,player_Color,refx,refy,set_home,check_redundant_state):


    if (addstart):
        if (boardco[x][y] == '.'and  check_If_Valid(in_pos[0],in_pos[1],x,y,refx,refy,set_home) and (x,y) not in check_redundant_state):
            state_to_go_inside = (x,y)

            diagnol = min(abs(x - in_pos[0]), abs(y - in_pos[1]))
            check_redundant_state.add(state_to_go_inside)
            sort_state_val = heuristic_to_order_moves[x][y] - 2*diagnol
            ans_tup = (sort_state_val,"J",in_pos,(x,y))

            heapq.heappush(state_Q,ans_tup)
        else:
            return


    for it in range(0,8):
        t_corx = x+x_checker[it]
        t_cory = y+y_checker[it]
        # if((t_corx>=0 and t_cory >=0 and t_cory<=15 and t_corx<=15) and (boardco[t_corx][t_cory]=='W' or boardco[t_corx][t_cory]=='B')):
        if ((t_corx >= 0 and t_cory >= 0 and t_cory <= 15 and t_corx <= 15) and (boardco[t_corx][t_cory] != '.')):
            new_corx = t_corx+x_checker[it]
            new_cory = t_cory+y_checker[it]

            if(new_corx<0 or new_cory<0 or new_corx >15 or new_cory>15 or visited[new_corx][new_cory]):
                continue
            else:
                visited[new_corx][new_cory] = True
                get_Jumpstates2(new_corx,new_cory,x,y,state_Q,True,boardco,in_pos,player_Color,refx,refy,set_home,check_redundant_state)
                visited[new_corx][new_cory] = False

# counting = 0

def get_NextStates2(States_q,boardC,x,y,player_Color):
    # global counting
    # States_q = []
    homeset_Copy = {}
    black = False
    white = False
    home_Top_corx = 0
    home_Top_cory = 0


    if player_Color == "B":
        homeset_Copy = blackposition_Set
        # heuristic_to_order_moves = black_min_dist
        black = True
    else:
        homeset_Copy = whiteposition_Set
        # heuristic_to_order_moves = white_min_dist
        white = True
        home_Top_corx = 15
        home_Top_cory = 15

    # this tupple needs to be passed everywhere to tell the starting point of the move
    inpos = (x,y)

    check_redundant = set()

    # checking the E moves
    for i in range(0,8):

        new_x = x+x_checker[i]
        new_y = y+y_checker[i]

        if(new_x<0 or new_y<0 or new_x>15 or new_y>15):
            continue
        else:
            if (boardC[new_x][new_y]=='.'):
                tu_to_add_state = (new_x,new_y)
                if(check_If_Valid(x,y,new_x,new_y,home_Top_corx,home_Top_cory,homeset_Copy)):
                    # list_Hardcoded_forE = ["TeeluBeelu"] this was fior the state for the jump states
                    diagnol = min(abs(new_x - x), abs(new_y - y))
                    sort_state_val = heuristic_to_order_moves[new_x][new_y] - 2*diagnol
                    check_redundant.add(tu_to_add_state)
                    sj_ans_tup = (sort_state_val,"E",inpos,tu_to_add_state)
                    heapq.heappush(States_q,(sj_ans_tup))

    visited[x][y] = True
    # check_redundant = set()
    # add the current state in input pos
    check_redundant.add(inpos)
    # print("jaa bhi rha h")
    get_Jumpstates2(x, y, -20, -20, States_q, False, boardC, inpos, player_Color,home_Top_corx,home_Top_cory,homeset_Copy,check_redundant)
    visited[x][y] = False
    # counting += len(States_q)
    # return States_q


def check_win(board_to_check):
    set_checker = {}
    if checking_Status == "B":
        set_checker = whiteposition_Set
    else:
        set_checker = blackposition_Set

    for points in set_checker:
        x_vl = points[1]
        y_vl = points[0]

        if board_to_check[x_vl][y_vl] != checking_Status:
            return False
    return True


def heuristic(bu,d,colour,status_symbol):
    temp = 0
    if not status_symbol:
        opp_lookuptable = white_min_dist
        opp_color = 'W'
        lookup_table = black_min_dist
        if colour == 'W':
            lookup_table = white_min_dist
            opp_lookuptable = black_min_dist
            opp_color = 'B'

        for x_i in range(0,16):
            for y_i in range(0,16):
                if (bu[x_i][y_i] == checking_Status):
                    temp -= lookup_table[x_i][y_i]
        for x_i in range(0,16):
            for y_i in range(0,16):
                if (bu[x_i][y_i] == opp_color):
                    temp += lookup_table[x_i][y_i]

        return (temp+(-1)*d,"no scene")
        # return (temp +  d, "no scene")
    else:
        tempnew = 0
        lookingTable = white_initial_move_heuristic
        # print(lookingTable)
        if checking_Status == "B":
            lookingTable = black_initial_move_heuristic

        for x_var in range(0,16):
            for y_var in range(0,16):
                if(bu[x_var][y_var] == checking_Status):
                    # tempnew += lookingTable[x_var][y_var]
                    tempnew += lookingTable[x_var][y_var]
        return (tempnew,"no scene")


max_Val = sys.maxsize
min_Val = -sys.maxsize -1

pruning_bitch = 0
total_times = 0


def get_All_States(board_used,move_out_feature,current_State_Color):
    # print("all")
    state_Q_All = []
    if move_out_feature:
        set_of_initial_home_loc = set()
        if (checking_Status == "B"):
            set_of_initial_home_loc = blackposition_Set
        else:
            set_of_initial_home_loc = whiteposition_Set

        for pointerz in set_of_initial_home_loc:
            x_i = pointerz[1]
            y_i = pointerz[0]
            if board_used[x_i][y_i] == current_State_Color:
                get_NextStates2(state_Q_All,board_used, x_i, y_i, current_State_Color)
    else:
        for x_loc in range(0, 16):
            for y_loc in range(0, 16):
                if (board_used[x_loc][y_loc] == current_State_Color):
                    get_NextStates2(state_Q_All,board_used, x_loc, y_loc, current_State_Color)

    return state_Q_All


def alpha_Beta(board_used,depth,maximizingPlayer,alpha,beta,current_State_Color,move_out_feature):
    global pruning_bitch
    global total_times
    total_times += 1

    action_best = ("nomovetoplay")

    if depth == stop_depth or check_win(board_used):
        return heuristic(board_used,depth,checking_Status,move_out_feature)

    allstates = []

    if maximizingPlayer:
        best = (-1)*sys.maxsize
        # next state jo min ko dena hai vo konsa color hoga

        next_State_color = ''
        if(current_State_Color == 'B'):
            next_State_color = "W"
        else:
            next_State_color = "B"

        allstates = get_All_States(board_used,move_out_feature,current_State_Color)

        for state_tuplesm in allstates:
            action_taken = state_tuplesm[1]
            parent_pos = state_tuplesm[2]
            new_posi = state_tuplesm[3]
            par_x = parent_pos[0]
            par_y = parent_pos[1]
            x_tojump = new_posi[0]
            y_tojump = new_posi[1]

            board_used[par_x][par_y] = '.'
            board_used[x_tojump][y_tojump] = current_State_Color


            val_actionT = alpha_Beta(board_used,depth+1,False,alpha,beta,next_State_color,move_out_feature)
            val_action = val_actionT[0]

            board_used[par_x][par_y] = current_State_Color
            board_used[x_tojump][y_tojump] = '.'
            # yaha I'll send the next state color as it will be next players turn
            # if(depth == 0 and x_tojump == 6 and y_tojump == 3):
            #     print("ye konsi value h",val_action)
            if (val_action > best):

                # tempo = (action_taken,(par_x,par_y),(x_tojump,y_tojump))
                # action_best = tempo
                action_best = (action_taken,(par_x,par_y),(x_tojump,y_tojump))

                # # new change
                # best_cpdict = pcdict

            best = max(val_action, best)
            alpha = max(alpha,best)

            if(beta<=alpha):
                pruning_bitch+=1
                break

        return (best,action_best)

    else:

        best = sys.maxsize

        # next state jo min ko dena hai vo konsa color hoga
        next_State_color = ""
        if (current_State_Color == "B"):
            next_State_color = "W"
        else:
            next_State_color = "B"

        allstates = get_All_States(board_used, move_out_feature, current_State_Color)

        for state_tuplesm in allstates:
            action_taken = state_tuplesm[1]
            parent_pos = state_tuplesm[2]
            new_posi = state_tuplesm[3]
            par_x = parent_pos[0]
            par_y = parent_pos[1]
            x_tojump = new_posi[0]
            y_tojump = new_posi[1]
            board_used[par_x][par_y] = '.'
            board_used[x_tojump][y_tojump] = current_State_Color

            val_actionT = alpha_Beta(board_used, depth + 1, True, alpha, beta, next_State_color,move_out_feature)
            val_action = val_actionT[0]

            board_used[par_x][par_y] = current_State_Color
            board_used[x_tojump][y_tojump] = '.'

            # if val_action < best:
            #     action_best = (action_taken, (par_x, par_y), (x_tojump, y_tojump))

            best = min(val_action, best)
            beta = min(beta, best)
            if (beta <= alpha):
                pruning_bitch+=1
                break

        return (best, action_best)

def getInFormat(ans):
    cost = ans[0]
    tupleans = ans[1]
    parent = tupleans[1]
    px = parent[0]
    py = parent[1]
    rp = (py, px)
    fin = tupleans[2]
    cx = fin[0]
    cy = fin[1]
    rc = (cy, cx)
    move = tupleans[0]
    returnin_tup = (cost, rc, rp, move)
    return returnin_tup

def dfs(px,py,x,y,fin_x,fin_y,set_of_visited,cp_dict,start_add):
    if(board[x][y]!='.' and start_add):
        return
    if ((x,y) in set_of_visited and start_add):
        return
    if ((x,y)==(fin_x,fin_y)):
        cp_dict[(fin_x,fin_y)] = (px,py)
        return
    set_of_visited.add((x,y))

    cp_dict[(x,y)]=(px,py)
    for i in range(0,8):
        new_x = x+x_checker[i]
        new_y = y+y_checker[i]
        if (new_x<0 or new_y<0 or new_x>15 or new_y>15):
            continue

        if(board[new_x][new_y] != '.'):
            next_x = new_x+x_checker[i]
            next_y = new_y+y_checker[i]
            if(next_x<0 or next_y<0 or next_x >15 or next_y>15):
                continue
            else:
                dfs(x,y,next_x,next_y,fin_x,fin_y,set_of_visited,cp_dict,True)

def get_Path_and_print(fin_tup):
    cp_dict = {}
    start_loc = fin_tup[1][1]
    end_loc = fin_tup[1][2]
    action = fin_tup[1][0]
    px = start_loc[0]
    py = start_loc[1]
    cx = end_loc[0]
    cy = end_loc[1]
    set_of_visited = set()
    set_of_visited.add((px,py))
    to_add = []


    if action == "J":
        dfs(-22,-22,px,py,cx,cy,set_of_visited,cp_dict,False)
    else:
        for i in range(0,8):
            tx = px+x_checker[i]
            ty = py+y_checker[i]
            if(tx>=0 and ty>=0 and tx<=15 and ty<=15):
                if(tx == cx and ty == cy):
                    to_add = "E "+str(py)+","+str(px)+" "+str(cy)+","+str(cx)
        file_writer(to_add,False)

    if action == "J":
        jumpx = cx
        jumpy = cy

        while(jumpx != -22 and jumpy != -22):
            childt = (jumpx,jumpy)
            tp = cp_dict[childt]
            tpx = tp[0]
            tpy = tp[1]
            app = "J "+str(tp[1])+","+str(tp[0])+" "+str(jumpy)+","+str(jumpx)
            jumpx = tpx
            jumpy = tpy
            if (tpx!=-22 and tpy!=-22):
                to_add.append(app)
        file_writer(to_add,True)

    print(to_add,"path")


def file_writer(main_print,revCheck):
    iceland = ""
    if revCheck:
        main_print.reverse()

        for path in main_print:
            iceland+=path
        # iceland+=" "
            iceland += "\n"
    else:
        iceland+=main_print
    with open("output.txt","w") as filo:
        filo.write(iceland)

def start_Game():
    global stop_depth

    if(gameType == "GAME"):
        # print("kolo")
        if (time_Remaining < 20):
            stop_depth = 2
        elif (time_Remaining < 15):
            stop_depth = 1
    elif(gameType == "SINGLE"):
        if(time_Remaining<15):
            stop_depth = 1

    set_to_refer = {}

    # check kr ghar me koi hai ya nahi
    if checking_Status == 'B':
        set_to_refer = blackposition_Set
    else:
        set_to_refer = whiteposition_Set

    move_out_feature = False

    for points in set_to_refer:
        x = points[1]
        y = points[0]
        if(board[x][y]==checking_Status):
            move_out_feature = True
            stop_depth = 1


    use_board = deepcopy(board)
    ans = alpha_Beta(use_board,0,True,min_Val,max_Val,checking_Status,move_out_feature)
    print(ans,"best move")
    # print("best move",ans[1])
    if ans[1] == "nomovetoplay":
        stop_depth = 3
        ans_new = alpha_Beta(use_board, 0, True, min_Val, max_Val, checking_Status, False)


        ans = ans_new

    get_Path_and_print(ans)

start_Game()

end_time = time.time()
print(end_time-start_time)
