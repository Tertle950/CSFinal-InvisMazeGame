#!/usr/bin/env python3

import string
#import keyboard
import curses
import libxmplite
#https://stackoverflow.com/questions/3523174/raw-input-without-pressing-enter

# Problem: My kids need a distraction, but all I have is a Linux terminal and a Python interpreter!

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
stdscr.clear()
stdscr.refresh()
curses.start_color()

cuLine = 0

def clear():
    stdscr.clear()
    global cuLine
    cuLine = 0

def cuPrint(x):
    global cuLine
    stdscr.addstr(cuLine+2, 1+2, x)
    cuLine += 1
    return

def printMaze(maze):
    clear()
    returner = [-1, -1]
    for dex,i in enumerate(maze):
        line = ""
        for ind,j in enumerate(i):
            if j == " ":
                line += "."
            else: line += j
            if j == "U":
                returner = [dex, ind]
        cuPrint(line)
    return returner

def dontPrintMaze(maze):
    clear()
    returner = [-1, -1]
    for dex,i in enumerate(maze):
        line = ""
        for ind,j in enumerate(i):
            if j == "U" or j == "░":
                if j == "U": returner = [dex, ind]
                line += j
            else:
                line += "."
        cuPrint(line)
    return returne

# The maze itself is a constant.
mazeStrings = [
    " █████████   ",
    "█U█       ██ ",
    "█     █     █",
    "█    █ █    █",
    " ██     █   █",
    "█    █   █  █",
    " █  █ █    █ ",
    "█   █ █   █  ",
    "█    ██  █ █ ",
    "█  █       ░█",
    " ███████████ "] # It's a lot easier to write it this way.

# ...but here's what I'm REALLY gonna use!
mazeChars = []
for i in mazeStrings:
    mCpart = []
    for j in i:
        mCpart.append(j)
    mazeChars.append(mCpart)

smileyCoord = printMaze(mazeChars)

goalCoord = 0
for dex,i in enumerate(mazeChars):
    if(goalCoord != 0): break
    for ind,j in enumerate(i):
        if(j == "░"):
            goalCoord = [dex, ind]
            break

def game(mazeChars):
    while True:
        chara = stdscr.getch()
        if goSmiley(chara) and smileyCoord[0] == goalCoord[0] and smileyCoord[1] == goalCoord[1]:
            return

def goSmiley(direction):
    global smileyCoord
    # Interpret the input.
    ch = [0, 0]
    try:
        if direction == 100: #d
            ch = [0, 1]
        if direction == 97: #a
            ch = [0, -1]
        if direction == 115: #s
            ch = [1, 0]
        if direction == 119: #w
            ch = [-1, 0]
    except(IndexError):
        #cuPrint("U  { Please type a direction for me to go. )")
        return False

    #cuPrint("ch is: {}".format(ch))

    if(ch[0] + ch[1] == 0):
        #cuPrint("U  { Please type a direction for me to go. )")
        return False
    new = [smileyCoord[0] + ch[0], smileyCoord[1] + ch[1]]
    if (mazeChars[new[0]][new[1]] == "█"): # This is a mess.
        #cuPrint("U  { Please type a direction for me to go. )")
        return False

    #cuPrint("smileyCoord was: {}".format(smileyCoord))
    mazeChars[smileyCoord[0]][smileyCoord[1]] = " "
    mazeChars[new[0]][new[1]] = "U"

    # Print the maze again, and reinitialize the coordinates of the character.
    smileyCoord = dontPrintMaze(mazeChars)
    if smileyCoord == [-1, -1]:
        raise Exception("Smiley's gone?")
    #cuPrint("smileyCoord is: {}".format(smileyCoord))
    #cuPrint("smileyCoord is: {}".format(goalCoord))
    return True

game(mazeChars)

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
print("U got to the end!")