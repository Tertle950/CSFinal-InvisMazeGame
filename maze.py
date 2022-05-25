import string
# Problem: My kids need a distraction, but all I have is a Linux terminal and a Python interpreter!

print("Terminal-based slippery maze game on Python - Sample create task")

def printMaze(maze):
    returner = [-1, -1]
    for dex,i in enumerate(maze):
        line = ""
        for ind,j in enumerate(i):
            line += j
            if j == "☺":
                returner = [dex, ind]
        print(line)
    return returner

def dontPrintMaze(maze):
    returner = [-1, -1]
    for dex,i in enumerate(maze):
        line = ""
        for ind,j in enumerate(i):
            if j == "☺":
                returner = [dex, ind]
                line += "☺"
            else:
                line += " "
        print(line)
    return returner

# def

# The maze itself is a constant.
mazeStrings = [
    "████████████",
    "█☺      █  █",
    "█ ██ ██ █ ██",
    "█  █ █     █",
    "██ █   ██ ██",
    "█    ██   ██",
    "█ ██ █     █",
    "█      █   █",
    "█ █ █████ ██",
    "█ █       ░█",
    "████████████"] # It's a lot easier to write it this way.

# ...but here's what I'm REALLY gonna use!
mazeChars = []
for i in mazeStrings:
    mCpart = []
    for j in i:
        mCpart.append(j)
    mazeChars.append(mCpart)

smileyCoord = printMaze(mazeChars)
goalCoord = [9, 10]

while True:
    # Ask for input from the player. UDLR accepted.
    print("☺  { Which way should I go? (U)p, (D)own, (L)eft, or (R)ight? )")
    direction = input("> ").lower()

    # Interpret the input.
    ch = [0, 0]
    try:
        if direction[0] == "r":
            ch = [0, 1]
        if direction[0] == "l":
            ch = [0, -1]
        if direction[0] == "d":
            ch = [1, 0]
        if direction[0] == "u":
            ch = [-1, 0]
    except(IndexError):
        print("☺  { Please type a direction for me to go. )")
        continue

    #print("ch is: {}".format(ch))

    # Move the character as much as possible.
    new = [smileyCoord[0],smileyCoord[1]]
    if (ch != [0, 0]): 
        while (mazeChars[new[0]][new[1]] != "█"): # This is a mess.
            new[0] += ch[0]
            new[1] += ch[1]
            #printMaze(mazeChars)
            #print(new)
            #print(mazeChars[new[0]][new[1]])
    else:
        print("☺  { Please type a direction for me to go. )")
        continue

    # Unmove the character before he crashes into a wall. This is a mess.
    new[0] -= ch[0]
    new[1] -= ch[1]
    #print(new)


    #print("smileyCoord was: {}".format(smileyCoord))
    mazeChars[smileyCoord[0]][smileyCoord[1]] = " "
    mazeChars[new[0]][new[1]] = "☺"

    # Print the maze again, and reinitialize the coordinates of the character.
    smileyCoord = dontPrintMaze(mazeChars)
    if smileyCoord == [-1, -1]:
        raise Exception("Smiley's gone?")
    #print("smileyCoord is: {}".format(smileyCoord))
    #print("smileyCoord is: {}".format(goalCoord))


    # Check for victory.
    if smileyCoord[0] == goalCoord[0] and smileyCoord[1] == goalCoord[1]:
        break

print("Congratulations! You won!")