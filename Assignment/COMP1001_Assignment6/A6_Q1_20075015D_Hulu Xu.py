def main():
    # Create the 2D plane
    arr = []
    # Note x is row and y is column.
    x, y, direction = createMap(arr)

    printMap(arr)
    isDead = False
    while not isDead:
        print("Move forward (M)")
        print("Turn left by 90 degrees (L)")
        print("Turn right by 90 degress (R)")
        print("Save map (S)")
        command = input("Please enter your command: ")
        if command == "M":
            x, y, isDead = move(x, y, direction, arr)
        elif command == "L" or command == "R":
            direction = change_direction(x,y,command,arr)
        elif command == "S":
            out_file = open("gamesave.txt","a")
            map = arr_to_map(arr)
            out_file.write(map)
            out_file.close()
            print("Game saved in gamesave.txt")
        printMap(arr)

    print("Alpha crashes!")


def arr_to_map(arr):
    """I use a string to save the map. Because a txt file only receive a sting type. So this function will add all the
elements to a string and the format will save as the shape of the map"""
    map = '   ' # Two blank in txt file equal to one blank in python interface
    for i in range(10):
        map = map + ' ' + str(i)
    map = map + '\n'
    for x in range(10):
        map = map + str(x) + '  '
        for y in range(10):
            if arr[x][y] == ' ':
                map = map + '   '
            else:
                map = map + arr[x][y] + ' '
        map = map + '\n'
    return map







def change_direction(x,y,command,arr):
    if command == 'L':
        if arr[x][y] == "^":
            arr[x][y] = "<"
        elif arr[x][y] == "<":
            arr[x][y] = "v"
        elif arr[x][y] == "v":
            arr[x][y] = ">"
        elif arr[x][y] == ">":
            arr[x][y] = "^"
        direction = arr[x][y]
        return direction
    elif command == 'R':
        if arr[x][y] == "^":
            arr[x][y] = ">"
        elif arr[x][y] == ">":
            arr[x][y] = "v"
        elif arr[x][y] == "v":
            arr[x][y] = "<"
        elif arr[x][y] == "<":
            arr[x][y] = "^"
        direction = arr[x][y]
        return direction






def createMap(arr):
    direction_dict = {1: '^', 2: '>', 3: 'v', 4: '<'}
    for i in range(0, 10):
        row = []
        for j in range(0, 10):
            row.append(' ')
        arr.append(row)

    # Generate the spaceship
    import random
    x = random.randrange(0, 10)
    y = random.randrange(0, 10)
    direction = random.randrange(1,4)
    arr[x][y] = direction_dict[direction]
    direction = arr[x][y]
    alphaX = x
    alphaY = y

    # Generate the stars
    for i in range(0, 8):
        x = random.randrange(0, 10)
        y = random.randrange(0, 10)
        while arr[x][y] != ' ':
            x = random.randrange(0, 10)
            y = random.randrange(0, 10)
        arr[x][y] = '*'
    return alphaX, alphaY, direction  # return current position of Alpha and its direction


def printMap(arr):
    # Print the map
    print('  ', end='')
    for i in range(0, 10):
        print(i, '', end='')
    print()
    for i in range(0, 10):
        print(i, '', end='')
        for j in range(0, 10):
            print(arr[i][j], '', end='')
        print()


def move(x, y, direction, arr):
    direction_dict = {'^':'N', '>':'E', 'v':'S', '<':'W'}
    direction = direction_dict[direction]
    oldX = x
    oldY = y;
    if direction == 'N':
        x -= 1
    elif direction == 'E':
        y += 1
    elif direction == 'S':
        x += 1
    elif direction == 'W':
        y -= 1

    if x < 0:
        x = 0
    elif y < 0:
        y = 0
    elif x > 9:
        x = 9
    elif y > 9:
        y = 9

    # Update the map
    dead = (arr[x][y] == '*')
    if not dead:
        tempDirection = arr[x][y]
        arr[x][y] = arr[oldX][oldY]
        arr[oldX][oldY] = tempDirection
    else:
        arr[oldX][oldY] = ' '
        arr[x][y] = ' '

    return x, y, dead

main()