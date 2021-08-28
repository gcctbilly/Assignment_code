def cleanup(s:str):
    states_list = []
    state = ''
    for i in range(len(s)):
        if s[i] != ' ' and s[i] != '>':
            state = state + s[i].upper()
        elif s[i] == '>':
            states_list.append(state)
            state = ''
        if i == len(s) - 1:
            states_list.append(state)
    return states_list

def islegal(state:str):
    position = 'west'
    state_west = ''
    state_east = ''
    for i in range(len(state)): # divide the state into west and east according to '|'
        if state[i] == '|':
            position = 'east'
            continue
        if position == 'west':
            state_west = state_west + state[i]
        elif position == 'east':
            state_east = state_east + state[i]
    if (('C' in state_west and 'G' in state_west) or ('W' in state_west and 'G' in state_west)) and 'M' not in state_west:
        return False
    elif (('C' in state_east and 'G' in state_east) or ('W' in state_east and 'G' in state_east)) and 'M' not in state_east:
        return False
    else:
        return True

def canmove(state_old:str, state_new:str):
    man_position_old = 'east' # assume that man is on the east of the river at first
    man_position_new = 'east'
    for i in range(len(state_old)): #find the index of |
        if state_old[i] == '|':
            divide_line_index_old = i
    for i in range(len(state_new)):
        if state_new[i] == '|':
            divide_line_index_new = i
    for i in range(divide_line_index_old): # find the actually place of man
        if state_old[i] == 'M':
            man_position_old = 'west'
            break
    for i in range(divide_line_index_new):
        if state_new[i] == 'M':
            man_position_new = 'west'
    if man_position_old != man_position_new: # man need to move
        if abs(divide_line_index_new - divide_line_index_old) <= 2: # the boat can only take two items
            return True
        else:
            return False
    else:
        return False

def check(states_list:list):
    test = True
    for i in range(len(states_list)): #check the states, start and end
        if i == 0 and ('M' not in states_list[i][1:5] or 'C' not in states_list[i][1:5] or 'G' not in states_list[i][1:5] or 'W' not in states_list[i][1:5]):
            print("Start state {} is incorrect".format(states_list[i]))
            test = False
        if not islegal(states_list[i]):
            print("The state {} is illegal".format(states_list[i]))
            test = False
        if i == len(states_list) - 1 and ('M' not in states_list[i][0:4] or 'C' not in states_list[i][0:4] or 'G' not in states_list[i][0:4] or 'W' not in states_list[i][0:4]):
            print("End state {} is incorrect".format(states_list[i]))
            test = False
    left_index = 0 # create two index of states list
    right_index = 1
    while right_index < len(states_list): #check the move
        if not canmove(states_list[left_index],states_list[right_index]):
            print("The move {0} -> {1} is not allowed".format(states_list[left_index],states_list[right_index]))
            test = False
        left_index += 1
        right_index += 1
    if test:
        return True
    else:
        return False

def print_solution(states_list):
    name_dict = {'M': 'man', 'C': 'cabbage', 'G': 'goat', 'W': 'wolf'}
    old_index = 0  # create index to located two steps
    new_index = 1
    while new_index < len(states_list):
        position = 'west'
        state_west_old = ''
        state_east_old = ''
        for i in range(len(states_list[old_index])):  # divide the old state into west and east according to '|'
            if states_list[old_index][i] == '|':
                position = 'east'
                continue
            if position == 'west':
                state_west_old = state_west_old + states_list[old_index][i]
            elif position == 'east':
                state_east_old = state_east_old + states_list[old_index][i]

        position = 'west'
        state_west_new = ''
        state_east_new = ''
        for i in range(len(states_list[new_index])):  # divide the new state into left and right according to '|'
            if states_list[new_index][i] == '|':
                position = 'east'
                continue
            if position == 'west':
                state_west_new = state_west_new + states_list[new_index][i]
            elif position == 'east':
                state_east_new = state_east_new + states_list[new_index][i]

        if len(state_west_old) > len(state_west_new): # move to the east
            state_east_old_set = set(state_east_old)
            state_east_new_set = set(state_east_new)
            new_item = list(state_east_old_set ^ state_east_new_set) # find the difference of east
            if len(new_item) == 1:
                print("man to East")
            else:
                for i in range(len(new_item)):
                    if new_item[i] != 'M': # get the other item with man
                        with_man = name_dict[new_item[i]]
                print("man and {} to East".format(with_man))
        else: # move to the west
            state_west_old_set = set(state_west_old)
            state_west_new_set = set(state_west_new)
            new_item = list(state_west_old_set ^ state_west_new_set)
            if len(new_item) == 1:
                print("man to West")
            else:
                for i in range(len(new_item)):
                    if new_item[i] != 'M': # get the other item with man
                        with_man = name_dict[new_item[i]]
                print("man and {} to West".format(with_man))
        old_index += 1
        new_index += 1

def main(cases:list):
    for case in cases:
        print("Input solution: ", case)
        if check(cleanup(case)):
            print("Input solution is correct")
            print("The solution:")
            print_solution(cleanup(case))
        else:
            print("Input solution is incorrect")


